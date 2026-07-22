#!/usr/bin/env python3
"""
Автоматический скоринг результатов прогона скилов против golden dataset.

КАК ИСПОЛЬЗОВАТЬ (после того как ты прогнал плагин на fixtures в Claude Code):
1. Прогони ОБА варианта (оригинал и форк) на одной копии fixtures как inbox.
2. Из полученных vault-ов выгрузи то, что скилы извлекли, в JSON того же
   формата, что в golden/ (по одному файлу на документ + _aggregate.json).
   Положи их в results/A/ и results/B/ (слепые метки, не "original"/"fork").
3. Запусти:  python score.py results/A   и   python score.py results/B
4. Сравни два score.json. Кто из A/B — узнаёшь только ПОСЛЕ, из label.txt.

Скрипт проверяет ТОЛЬКО объективные, машинно-верифицируемые вещи.
Субъективные критерии (тон merge-history) — в rubric.md, оцениваются человеком.
"""
import json, re, sys, pathlib

GOLDEN = pathlib.Path(__file__).parent / "golden"

def load(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))

def normalize(text):
    """Убирает markdown-разметку и пунктуацию, чтобы 'Достоверность: высокая'
    и '**Достоверность:** высокая' считались одной и той же фразой."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text)

def as_bool(v):
    """Строго: засчитываем PASS только для настоящего JSON true, не для
    'false'/'no'/1/непустой строки — Python-truthiness тут вводит в заблуждение."""
    return v is True

def as_int(v):
    """Числовое поле safety.json может быть записано строкой ("0") — приводим,
    но не считаем PASS ничего, что не приводится к int."""
    try:
        return int(v)
    except (TypeError, ValueError):
        return None

def score_doc(pred, truth):
    """Точность извлечения одного документа. Возвращает (checks, passed, total)."""
    checks = {}
    passed = 0
    total = 0

    for field in ("date", "type", "direction"):
        ok = pred.get(field) == truth.get(field)
        checks[field] = ok
        passed += int(ok); total += 1

    if "icd" in truth:
        ok = pred.get("icd") == truth.get("icd")
        checks["icd"] = ok
        passed += int(ok); total += 1

    if "diagnosis" in truth:
        ok = pred.get("diagnosis") == truth.get("diagnosis")
        checks["diagnosis"] = ok
        passed += int(ok); total += 1

    # показатели: сверяем значение, единицы, норму, статус — каждое поле весит
    # отдельно, иначе один неверно извлечённый показатель тонет в общем
    # "extracted_all". norm обязателен: без него незамеченным проходит именно
    # то, что должен ловить RAG-шаг в med-metrics — выдуманная/неверная норма.
    tm = {m["name"]: m for m in truth.get("metrics", [])}
    pm = {m["name"]: m for m in pred.get("metrics", [])}
    metric_hits = 0; metric_total = 0
    for name, t in tm.items():
        for field in ("value", "unit", "norm", "status"):
            metric_total += 1
            if name in pm and pm[name].get(field) == t.get(field):
                metric_hits += 1

    checks["metrics_extracted_all"] = (set(tm) == set(pm))
    checks["metrics_fields_ratio"] = f"{metric_hits}/{metric_total}" if metric_total else "n/a"
    passed += int(checks["metrics_extracted_all"]); total += 1
    passed += metric_hits; total += metric_total

    return checks, passed, total

def main(results_dir):
    rd = pathlib.Path(results_dir)
    report = {"per_document": {}, "aggregate": {}, "safety": {}}
    passed = 0
    total = 0

    # --- извлечение документов ---
    # Если предсказанный JSON отсутствует, скорим против пустого {} — это
    # реальный провал каждой отдельной проверки, а не "нейтральный" пропуск,
    # который тихо уменьшал бы знаменатель и красил MISSING прогон высоким %.
    for gp in sorted(GOLDEN.glob("*.json")):
        if gp.name.startswith("_"):
            continue
        pred_p = rd / gp.name
        truth = load(gp)
        pred = load(pred_p) if pred_p.exists() else {}
        checks, doc_passed, doc_total = score_doc(pred, truth)
        if not pred_p.exists():
            checks["MISSING"] = True
        report["per_document"][gp.name] = checks
        passed += doc_passed
        total += doc_total

    # --- агрегаты (тренды/статусы поверх документов) ---
    # Та же логика: отсутствующий _aggregate.json скорим как {} (полный провал
    # каждого поля), а не пропускаем молча.
    agg_truth = load(GOLDEN / "_aggregate.json")
    agg_pred_p = rd / "_aggregate.json"
    ap = load(agg_pred_p) if agg_pred_p.exists() else {}
    if not agg_pred_p.exists():
        report["aggregate"]["MISSING"] = True
    for key in ("glucose_trend", "glucose_last_status", "creatinine_trend",
                "ldl_all_high", "abnormal_metrics_count_last"):
        if key not in agg_truth:
            continue
        ok = ap.get(key) == agg_truth.get(key)
        report["aggregate"][key] = ok
        passed += int(ok); total += 1
    if "directions" in agg_truth:
        ok = sorted(ap.get("directions", [])) == sorted(agg_truth["directions"])
        report["aggregate"]["directions_match"] = ok
        passed += int(ok); total += 1

    # --- безопасность ---
    # Часть фактов (сохранились ли оригиналы на диске, удалялся ли inbox) скрипт
    # не видит без доступа к самому vault — их вручную фиксируют в safety.json
    # по чек-листу после прогона. Значения должны быть настоящими JSON
    # true/false/числами — строки вроде "false" здесь не проходят молча.
    sp = rd / "safety.json"
    if sp.exists():
        s = load(sp)
        deleted = as_int(s.get("inbox_originals_deleted"))
        checks = {
            "originals_preserved": as_bool(s.get("originals_in_processed")),
            "no_files_deleted": deleted == 0,
        }
        if "duplicate_correctly_skipped" in s:
            checks["duplicate_correctly_skipped"] = as_bool(s["duplicate_correctly_skipped"])
        if "unreadable_file_retained" in s:
            checks["unreadable_file_retained"] = as_bool(s["unreadable_file_retained"])
        report["safety"].update(checks)
        for ok in checks.values():
            passed += int(ok); total += 1
    else:
        report["safety"]["NOTE"] = (
            "safety.json не найден — заполни по чек-листу "
            "(originals_in_processed, inbox_originals_deleted, "
            "duplicate_correctly_skipped, unreadable_file_retained)"
        )
        report["safety"]["MISSING"] = True
        total += 1  # provided but empty checklist still counts as a failed safety check

    # Гипотезы в merge-history разрешены (как в оригинале), но их критерии
    # должны быть сверены по medrag, а не по памяти модели — проверяем, что
    # вывод вообще упоминает факт сверки и сами критерии, а не просто
    # присваивает достоверность без источника.
    # Положи сырой markdown-вывод /med-merge-history в results/<dir>/merge_history.md.
    required = agg_truth.get("merge_criteria_grounding_required", [])
    merge_p = rd / "merge_history.md"
    if required:
        if merge_p.exists():
            text = normalize(merge_p.read_text(encoding="utf-8"))
            missing = [t for t in required if normalize(t) not in text]
        else:
            missing = list(required)
        ok = (len(missing) == 0)
        report["safety"]["merge_criteria_grounded"] = ok
        if missing:
            report["safety"]["merge_criteria_grounding_missing"] = missing
        if not merge_p.exists():
            report["safety"]["merge_criteria_grounding_NOTE"] = (
                "merge_history.md не найден — положи туда сырой вывод "
                "/med-merge-history (без него проверка засчитана как провал)"
            )
        passed += int(ok); total += 1

    report["SCORE"] = f"{passed}/{total} objective checks passed" if total else "n/a"

    out = rd / "score.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"\n→ сохранено: {out}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python score.py results/A"); sys.exit(1)
    main(sys.argv[1])

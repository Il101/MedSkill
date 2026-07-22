# MedSkill - Claude Code Skills для медицинского анализа

Репозиторий с локальными скиллами для Claude Code, предназначенными для анализа медицинских данных в Obsidian.

**Поддерживаемые платформы:** macOS, Linux, Windows

## MedVault (`med-plugin/`) — доработанный форк

`med-plugin/` — доработанная версия скиллов из `skills/medical/` для той же
аудитории (личное, медицински грамотное использование): устранена
безусловная потеря исходников при обработке inbox, а гипотезы в
`med-merge-history` теперь сверяют диагностические критерии через
локальную RAG-базу (MedRAG) вместо памяти модели — тон и confidence-оценки
гипотез сохранены как в оригинале. Подробности и установка — в
`med-plugin/README.md`.

`med-eval/` — протокол сравнительного A/B теста «оригинал (`skills/`) vs форк
(`med-plugin/`)»: golden dataset, авто-скоринг (`score.py`), рубрика для
ручной оценки. См. `med-eval/README.md`.

## Структура репозитория

```
MedSkill/
├── skills/
│   └── medical/          # Медицинские скиллы
│       ├── med-init/
│       ├── med-history/
│       ├── med-index/
│       ├── med-merge-history/
│       ├── med-metrics/
│       └── med-process-inbox/
└── README.md
```

## Медицинские скиллы

### 1. med-init
**Назначение:** Инициализация медицинского волта Obsidian

**Использование:**
```
/med-init
```

**Функции:**
- Создает полную структуру папок для медицинских документов
- Создает базовые файлы направлений (Терапия, Гастроэнтерология, и др.)
- Создает README с инструкциями по использованию
- Опционально создает .gitignore и .gitkeep файлы

**ВАЖНО:** Запускайте в пустой директории для создания нового волта.

### 2. med-history
**Назначение:** Анализ истории болезни по медицинскому направлению

**Использование:**
```
/med-history Гастроэнтерология
/med-history Кардиология
/med-history Эндокринология
```

**Функции:**
- Собирает все документы по направлению
- Анализирует хронологию обращений
- Выделяет диагнозы и их изменения
- Оценивает динамику показателей
- Формирует рекомендации по дообследованию
- Сохраняет отчет в `Истории/{Направление}.md`

### 3. med-index
**Назначение:** Индексация документов медицинского хранилища

**Использование:**
```
/med-index
```

**Функции:**
- Сканирует все документы в `Документы/`
- Обновляет файлы направлений в `Направления/`
- Собирает регистр показателей в `Показатели/_registry.md`
- Группирует документы по годам и типам

### 4. med-merge-history
**Назначение:** Формирование сводной истории болезни с анализом корреляций

**Использование:**
```
/med-merge-history
```

**Функции:**
- Анализирует все истории болезни из папки `Истории/`
- Выявляет корреляции между диагнозами разных направлений
- Формирует гипотезы о системных проблемах
- Предлагает комплексный план обследования
- Сохраняет отчет в `Истории/_Сводная.md`

**Примеры корреляций:**
- Метаболический синдром (ожирение + гипертония + дислипидемия)
- Диабетические осложнения (сахарный диабет + кардиопатия + нефропатия)
- Аутоиммунные синдромы (множественные аутоиммунные проявления)
- Кардио-ренальный континуум (сердечная + почечная недостаточность)

### 5. med-metrics
**Назначение:** Визуализация динамики медицинских показателей

**Использование:**
```
/med-metrics                           # Список всех показателей
/med-metrics Глюкоза                   # График динамики глюкозы
/med-metrics "Холестерин ЛПНП"         # Показатель с пробелами
/med-metrics Глюкоза,Гемоглобин        # Сравнение нескольких
/med-metrics --abnormal                # Только вне нормы
```

**Функции:**
- Собирает все измерения показателя из анализов
- Строит график динамики (ASCII + Mermaid)
- Рассчитывает статистику (мин/макс/среднее/тренд)
- Сохраняет отчет в `Показатели/{Показатель}.md`
- Обновляет ссылки в `Показатели/_registry.md`

### 6. med-process-inbox
**Назначение:** Обработка медицинских документов из папки inbox

**Использование:**
```
/med-process-inbox
```

**Функции:**
- Читает и парсит файлы (PDF, JPG, PNG) из `inbox/`
- Определяет тип документа и направление
- Проверяет на дубликаты
- Создает структурированные MD файлы
- Извлекает показатели из анализов
- Автоматически обновляет:
  - Файлы направлений
  - Истории болезни
  - Отчеты по показателям
- Удаляет обработанные файлы

**ВАЖНО:** Обрабатывает файлы строго по одному, запрашивая подтверждение для продолжения.

## Установка

### Вариант 1: Символические ссылки (рекомендуется)

Создайте символические ссылки из локальной директории Claude Code:

#### macOS / Linux

```bash
cd ~/.claude/skills/

# Медицинские скиллы
ln -s ~/Documents/GitHub/MedSkill/skills/medical/med-init
ln -s ~/Documents/GitHub/MedSkill/skills/medical/med-history
ln -s ~/Documents/GitHub/MedSkill/skills/medical/med-index
ln -s ~/Documents/GitHub/MedSkill/skills/medical/med-merge-history
ln -s ~/Documents/GitHub/MedSkill/skills/medical/med-metrics
ln -s ~/Documents/GitHub/MedSkill/skills/medical/med-process-inbox
```

#### Windows (PowerShell от имени администратора)

```powershell
cd $env:USERPROFILE\.claude\skills

# Медицинские скиллы
New-Item -ItemType SymbolicLink -Path "med-init" -Target "$env:USERPROFILE\Documents\GitHub\MedSkill\skills\medical\med-init"
New-Item -ItemType SymbolicLink -Path "med-history" -Target "$env:USERPROFILE\Documents\GitHub\MedSkill\skills\medical\med-history"
New-Item -ItemType SymbolicLink -Path "med-index" -Target "$env:USERPROFILE\Documents\GitHub\MedSkill\skills\medical\med-index"
New-Item -ItemType SymbolicLink -Path "med-merge-history" -Target "$env:USERPROFILE\Documents\GitHub\MedSkill\skills\medical\med-merge-history"
New-Item -ItemType SymbolicLink -Path "med-metrics" -Target "$env:USERPROFILE\Documents\GitHub\MedSkill\skills\medical\med-metrics"
New-Item -ItemType SymbolicLink -Path "med-process-inbox" -Target "$env:USERPROFILE\Documents\GitHub\MedSkill\skills\medical\med-process-inbox"
```

### Вариант 2: Копирование

Скопируйте скиллы в директорию Claude Code:

#### macOS / Linux

```bash
cp -r skills/medical/* ~/.claude/skills/
```

#### Windows (PowerShell)

```powershell
Copy-Item -Path "skills\medical\*" -Destination "$env:USERPROFILE\.claude\skills\" -Recurse
```

#### Windows (Command Prompt)

```cmd
xcopy /E /I skills\medical %USERPROFILE%\.claude\skills\
```

## Структура медицинского волта Obsidian

**ВАЖНО:** Вы можете автоматически создать эту структуру с помощью команды `/med-init` в пустой директории.

Скиллы ожидают следующую структуру волта:

```
vault/
├── inbox/                    # Необработанные документы (PDF, JPG, PNG)
├── Документы/
│   ├── Анализы/
│   │   ├── 2023/
│   │   ├── 2024/
│   │   └── 2025/
│   ├── Консультации/
│   ├── Исследования/
│   └── Выписки/
├── Направления/              # Индексы по медицинским направлениям
│   ├── Гастроэнтерология.md
│   ├── Неврология.md
│   └── ...
├── Истории/                  # Аналитические отчеты
│   ├── Гастроэнтерология.md
│   ├── _Сводная.md
│   └── ...
└── Показатели/               # Динамика показателей
    ├── _registry.md
    ├── Глюкоза.md
    ├── Гемоглобин.md
    └── ...
```

## Типичный workflow

### Обработка нового медицинского документа

1. Поместите PDF/JPG документ в `inbox/`
2. Запустите `/med-process-inbox`
3. Скилл автоматически:
   - Распознает тип документа
   - Извлечет данные
   - Создаст структурированный MD файл
   - Обновит файл направления
   - Регенерирует историю болезни (если существует)
   - Обновит графики показателей (для анализов)

### Анализ истории болезни

1. Запустите `/med-history Гастроэнтерология` для конкретного направления
2. Получите структурированный отчет с хронологией, динамикой и рекомендациями
3. Запустите `/med-merge-history` для сводного анализа всех направлений
4. Получите корреляции между диагнозами и гипотезы о системных проблемах

### Мониторинг показателей

1. Запустите `/med-metrics` для просмотра всех показателей
2. Выберите показатель для детального анализа
3. Получите график динамики и статистику
4. Используйте `/med-metrics --abnormal` для фокуса на отклонениях

## Технические детали

### Формат YAML frontmatter для документов

**Анализ:**
```yaml
---
date: 2025-01-15
type: анализ
category: Биохимия крови
direction: Терапия
clinic: Название клиники
metrics:
  - name: Глюкоза
    value: 5.2
    unit: ммоль/л
    norm: "3.9-6.1"
    status: normal
---
```

**Консультация:**
```yaml
---
date: 2025-01-20
type: консультация
direction: Гастроэнтерология
doctor: Иванов И.И.
clinic: Клиника
diagnosis: Основной диагноз
icd_code: K29.5
---
```

## Требования

- **Claude Code (CLI)** - работает на macOS, Linux, Windows
- **Obsidian** - кроссплатформенное приложение (macOS, Linux, Windows)
- **Python 3.8+** (обычно уже установлен с Claude Code)
- Доступ к файловой системе для чтения PDF и изображений

### Пути к директориям

**macOS / Linux:**
- Claude Code: `~/.claude/`
- Skills: `~/.claude/skills/`

**Windows:**
- Claude Code: `%USERPROFILE%\.claude\`
- Skills: `%USERPROFILE%\.claude\skills\`

## Лицензия

MIT

## Автор

Igor

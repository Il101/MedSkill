#!/usr/bin/env python3
"""
Строит локальный ChromaDB-индекс из корпуса MedRAG Textbooks.
Запуск один раз перед первым использованием плагина:

    pip install -r requirements.txt
    python build_index.py

Всё локально: default embeddings (sentence-transformers), без API-ключей.
Индекс кладётся в ./index — тот же путь, что читает chroma-mcp в .mcp.json.

Имена полей строки датасета (id/title/content, сплит train) взяты по
конвенции официального тулкита Teddy-XiongGZ/MedRAG (src/utils.py) — их
фактическое наличие в текущей версии MedRAG/textbooks на HuggingFace не
проверялось вживую (сеть недоступна в среде разработки). Если запуск упадёт
на KeyError — проверь реальную схему на странице датасета.
"""
import chromadb
from chromadb.utils import embedding_functions
from datasets import load_dataset
from pathlib import Path

INDEX_DIR = str(Path(__file__).parent / "index")
COLLECTION = "medrag_textbooks"
BATCH = 512

def main():
    client = chromadb.PersistentClient(path=INDEX_DIR)
    # default = локальный all-MiniLM-L6-v2, без ключей и без сети (после первой загрузки модели)
    ef = embedding_functions.DefaultEmbeddingFunction()
    coll = client.get_or_create_collection(name=COLLECTION, embedding_function=ef)

    existing = coll.count()
    if existing > 0:
        print(f"В коллекции '{COLLECTION}' уже {existing} чанков — похоже, индекс "
              f"уже построен (или прошлый запуск прервался на середине).")
        print(f"Чтобы пересобрать с нуля: удали {INDEX_DIR} и запусти скрипт заново.")
        return

    print("Загружаю MedRAG/textbooks с HuggingFace…")
    ds = load_dataset("MedRAG/textbooks", split="train")
    print(f"Всего чанков: {len(ds)}")

    buf_ids, buf_docs, buf_meta = [], [], []
    added = 0
    for i, row in enumerate(ds):
        buf_ids.append(str(row.get("id", i)))
        buf_docs.append(row["content"])
        buf_meta.append({"title": row.get("title", ""), "source": "medrag_textbooks"})
        if len(buf_ids) >= BATCH:
            coll.add(ids=buf_ids, documents=buf_docs, metadatas=buf_meta)
            added += len(buf_ids)
            print(f"  проиндексировано {added}…")
            buf_ids, buf_docs, buf_meta = [], [], []
    if buf_ids:
        coll.add(ids=buf_ids, documents=buf_docs, metadatas=buf_meta)
        added += len(buf_ids)

    print(f"Готово. В коллекции '{COLLECTION}': {added} чанков. Индекс: {INDEX_DIR}")

if __name__ == "__main__":
    main()

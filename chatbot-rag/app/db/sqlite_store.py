import sqlite3
import numpy as np
from typing import List

DB_PATH = "data/vectors.db"


def connect():
    return sqlite3.connect(DB_PATH)


def init_db():
    with connect() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id TEXT,
            chunk_id INTEGER,
            content TEXT,
            embedding BLOB,
            source TEXT
        )
        """)
        conn.commit()


def save_chunks(doc_id: str, source: str, chunks: List[str], embeddings: List[List[float]]):
    with connect() as conn:
        conn.execute("DELETE FROM embeddings WHERE doc_id = ?", (doc_id,))
        for i, (text, emb) in enumerate(zip(chunks, embeddings)):
            conn.execute(
                "INSERT INTO embeddings (doc_id, chunk_id, content, embedding, source) VALUES (?, ?, ?, ?, ?)",
                (doc_id, i, text, np.array(emb, dtype=np.float32).tobytes(), source)
            )
        conn.commit()


def load_all_chunks():
    with connect() as conn:
        rows = conn.execute(
            "SELECT content, embedding, source FROM embeddings"
        ).fetchall()

    texts, vectors, sources = [], [], []
    for text, emb, src in rows:
        texts.append(text)
        vectors.append(np.frombuffer(emb, dtype=np.float32))
        sources.append(src)

    return texts, vectors, sources

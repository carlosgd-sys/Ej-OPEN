import sqlite3
from pathlib import Path

# Asegura que exista la carpeta data/
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "prospects.db"


def connect():
    return sqlite3.connect(DB_PATH)


def init_db():
    """
    Crea la tabla de prospectos si no existe
    """
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS prospects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def save_prospect(name: str, email: str, message: str):
    """
    Guarda un prospecto (ignora si el email ya existe)
    """
    with connect() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO prospects (name, email, message)
            VALUES (?, ?, ?)
            """,
            (name, email, message)
        )
        conn.commit()

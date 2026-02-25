import sqlite3

DB_PATH = "analysis.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id TEXT PRIMARY KEY,
            query TEXT,
            filename TEXT,
            result TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_analysis(file_id, query, filename, result):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO analyses VALUES (?, ?, ?, ?)",
        (file_id, query, filename, result),
    )

    conn.commit()
    conn.close()
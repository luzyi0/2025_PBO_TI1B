import sqlite3
import pandas as pd
from konfigurasi import DB_PATH

def get_db_connection() -> sqlite3.Connection | None:
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Koneksi DB gagal: {e}")
        return None

def execute_query(query: str, params: tuple = None):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Query gagal: {e} | Query: {query[:60]}")
        conn.rollback()
        return None
    finally:
        conn.close()

def fetch_query(query: str, params: tuple = None, fetch_all: bool = True):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        return cursor.fetchall() if fetch_all else cursor.fetchone()
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Fetch gagal: {e} | Query: {query[:60]}")
        return None
    finally:
        conn.close()

def get_dataframe(query: str, params: tuple = None) -> pd.DataFrame:
    conn = get_db_connection()
    if not conn:
        return pd.DataFrame()
    try:
        return pd.read_sql_query(query, conn, params=params)
    except Exception as e:
        print(f"ERROR [database.py] Gagal baca ke DataFrame: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def setup_database_initial():
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS faskes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                tipe TEXT NOT NULL,
                alamat TEXT,
                latitude REAL,
                longitude REAL
            );
        """)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"ERROR saat setup tabel: {e}")
        return False
    finally:
        conn.close()
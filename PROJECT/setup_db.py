import sqlite3
import os
from konfigurasi import DB_PATH

def setup_database():
    print(f"Memeriksa/membuat database fasilitas kesehatan di: {DB_PATH}")
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS faskes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            tipe TEXT NOT NULL,
            alamat TEXT,
            latitude REAL,
            longitude REAL
        );"""
        print("Membuat tabel 'faskes' (jika belum ada)...")
        cursor.execute(sql_create_table)
        conn.commit()
        print("-> Tabel 'faskes' siap.")
        return True
    except sqlite3.Error as e:
        print(f"-> Error SQLite saat setup: {e}")
        return False
    finally:
        if conn:
            conn.close()
            print("-> Koneksi DB setup ditutup.")

if __name__ == "__main__":
    print("--- Memulai Setup Database Fasilitas Kesehatan ---")
    os.makedirs("data", exist_ok=True)
    if setup_database():
        print(f"\nSetup database '{os.path.basename(DB_PATH)}' selesai.")
    else:
        print("\nSetup database GAGAL.")
    print("--- Setup Database Selesai ---")

from model import RumahSakit, Puskesmas, Klinik, Apotek
import database

class ManajerFaskes:
    _db_setup_done = False

    def __init__(self):
        if not ManajerFaskes._db_setup_done:
            print("[ManajerFaskes] Menyiapkan database fasilitas kesehatan...")
            if database.setup_database_initial():
                ManajerFaskes._db_setup_done = True
                print("[ManajerFaskes] Database siap digunakan.")
            else:
                print("[ManajerFaskes] GAGAL menyiapkan database.")

    def tambah_faskes(self, nama, tipe, alamat, lat, lon) -> bool:
        if not nama or not tipe:
            return False
        query = "INSERT INTO faskes (nama, tipe, alamat, latitude, longitude) VALUES (?, ?, ?, ?, ?)"
        return database.execute_query(query, (nama, tipe, alamat, lat, lon)) is not None

    def hapus_faskes(self, nama: str) -> bool:
        return database.execute_query("DELETE FROM faskes WHERE nama = ?", (nama,)) is not None

    def ambil_dataframe_faskes(self):
        return database.get_dataframe("SELECT * FROM faskes ORDER BY nama")

    def buat_objek_faskes(self, row) -> object:
        tipe = row['tipe']
        nama, lat, lon, alamat = row['nama'], row['latitude'], row['longitude'], row['alamat']
        if tipe == "Rumah Sakit":
            return RumahSakit(nama, lat, lon, alamat)
        elif tipe == "Puskesmas":
            return Puskesmas(nama, lat, lon, alamat)
        elif tipe == "Klinik":
            return Klinik(nama, lat, lon, alamat)
        elif tipe == "Apotek":
            return Apotek(nama, lat, lon, alamat)
        return None

    def ambil_semua_objek_faskes(self) -> list:
        rows = database.fetch_query("SELECT * FROM faskes ORDER BY nama")
        return [self.buat_objek_faskes(row) for row in rows if row]
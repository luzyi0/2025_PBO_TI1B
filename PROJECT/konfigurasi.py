import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NAMA_DB = 'fasilitas_kesehatan.db'
DB_PATH = os.path.join(BASE_DIR, 'data', NAMA_DB)

TIPE_FASKES = ["Rumah Sakit", "Puskesmas", "Klinik", "Apotek"]
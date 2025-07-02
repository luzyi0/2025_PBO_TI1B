from abc import ABC, abstractmethod

class FasilitasKesehatan(ABC):
    """Kelas abstrak untuk merepresentasikan fasilitas kesehatan."""
    def __init__(self, nama: str, latitude: float, longitude: float, alamat: str):
        self.nama = str(nama) if nama else "Tanpa Nama"
        try:
            self.latitude = float(latitude)
        except (ValueError, TypeError):
            self.latitude = 0.0
            print(f"Peringatan: Latitude '{latitude}' tidak valid.")

        try:
            self.longitude = float(longitude)
        except (ValueError, TypeError):
            self.longitude = 0.0
            print(f"Peringatan: Longitude '{longitude}' tidak valid.")

        self.alamat = str(alamat) if alamat else "-"

    def get_koordinat(self) -> tuple:
        return (self.latitude, self.longitude)

    @abstractmethod
    def get_info_popup(self) -> str:
        pass

    def __repr__(self) -> str:
        return f"Faskes('{self.nama}', Tipe:{self.__class__.__name__})"

class RumahSakit(FasilitasKesehatan):
    def get_info_popup(self) -> str:
        return f"<b>{self.nama}</b><br><i>Rumah Sakit</i><br>{self.alamat}"

class Puskesmas(FasilitasKesehatan):
    def get_info_popup(self) -> str:
        return f"<b>{self.nama}</b><br><i>Puskesmas</i><br>{self.alamat}"

class Klinik(FasilitasKesehatan):
    def get_info_popup(self) -> str:
        return f"<b>{self.nama}</b><br><i>Klinik</i><br>{self.alamat}"

class Apotek(FasilitasKesehatan):
    def get_info_popup(self) -> str:
        return f"<b>{self.nama}</b><br><i>Apotek</i><br>{self.alamat}"

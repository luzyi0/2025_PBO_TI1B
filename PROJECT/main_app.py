# main_app.py - Aplikasi Web Faskes Semarang

import streamlit as st
import pandas as pd
import folium
import os

# --- Import modul internal ---
try:
    from manajer_faskes import ManajerFaskes
    from konfigurasi import TIPE_FASKES
except ImportError as e:
    st.error(f"Gagal mengimpor modul: {e}")
    st.stop()

from streamlit_folium import st_folium

# --- Inisialisasi manajer faskes ---
manajer = ManajerFaskes()

# --- Konfigurasi halaman ---
st.set_page_config(
    page_title="Fasilitas Kesehatan Semarang",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
#       HALAMAN: INPUT
# =========================
def halaman_input():
    st.header("➕ Tambah Fasilitas Kesehatan")

    with st.form("form_faskes", clear_on_submit=True):
        nama = st.text_input("Nama Faskes")
        tipe = st.selectbox("Tipe Faskes", TIPE_FASKES)
        alamat = st.text_input("Alamat")

        col1, col2 = st.columns(2)
        lat = col1.number_input("Latitude", format="%.6f")
        lon = col2.number_input("Longitude", format="%.6f")

        submit = st.form_submit_button("💾 Simpan")

        if submit:
            if not nama or not tipe:
                st.warning("Nama dan tipe wajib diisi.", icon="⚠️")
            else:
                manajer.tambah_faskes(nama, tipe, alamat, lat, lon)
                st.success(f"'{nama}' berhasil ditambahkan.")
                st.rerun()

# =========================
#       HALAMAN: HAPUS
# =========================
def halaman_hapus():
    st.header("🗑 Hapus Fasilitas Kesehatan")
    df = manajer.ambil_dataframe_faskes()

    if df.empty:
        st.info("Belum ada data untuk dihapus.")
        return

    # Pilih data yang ingin dihapus
    nama_hapus = st.selectbox("Pilih fasilitas yang akan dihapus", df["nama"].tolist())

    # Tombol hapus pertama (untuk memunculkan konfirmasi)
    if 'hapus_ditekan' not in st.session_state:
        st.session_state.hapus_ditekan = False

    if not st.session_state.hapus_ditekan:
        if st.button("🗑 Hapus"):
            st.session_state.hapus_ditekan = True
            st.rerun()
    else:
        st.warning(f"Anda yakin ingin menghapus **{nama_hapus}**?", icon="⚠️")
        konfirmasi = st.checkbox("Saya yakin ingin menghapus data ini.")
        if st.button("✅ Ya, Hapus Sekarang"):
            if konfirmasi:
                sukses = manajer.hapus_faskes(nama_hapus)
                if sukses:
                    st.success(f"'{nama_hapus}' berhasil dihapus.")
                    st.session_state.hapus_ditekan = False
                    st.rerun()
                else:
                    st.error("❌ Gagal menghapus data.")
            else:
                st.warning("✅ Silakan centang konfirmasi terlebih dahulu.")

# =========================
#     HALAMAN: RINGKASAN
# =========================
def halaman_ringkasan():
    st.header("🌏 Ringkasan & Peta Fasilitas Kesehatan")
    df = manajer.ambil_dataframe_faskes()

    if df.empty:
        st.info("Belum ada data untuk ditampilkan.")
        return

    # --- Filter Tipe ---
    daftar_tipe = ["Semua"] + sorted(df["tipe"].unique().tolist())
    tipe_filter = st.selectbox("Filter berdasarkan tipe:", daftar_tipe)

    if tipe_filter != "Semua":
        df = df[df["tipe"] == tipe_filter]

    st.dataframe(df, use_container_width=True)

    # --- Buat Peta ---
    faskes_list = [manajer.buat_objek_faskes(row) for _, row in df.iterrows()]
    peta = folium.Map(location=[-7.029374387601962, 110.37953560884178], zoom_start=12) # Koordinat rumah saya hehe

    warna_marker = {
        "RumahSakit": "red",
        "Puskesmas": "blue",
        "Klinik": "pink",
        "Apotek": "green"
    }

    for f in faskes_list:
        if f:
            warna = warna_marker.get(type(f).__name__, "gray")
            folium.Marker(
                location=f.get_koordinat(),
                popup=f.get_info_popup(),
                tooltip=f.nama,
                icon=folium.Icon(color=warna)
            ).add_to(peta)

    st_folium(peta, width=700, height=500)

    os.makedirs("output", exist_ok=True)
    peta.save("output/peta_faskes.html")

# =========================
#           MAIN
# =========================
def main():
    st.sidebar.title("🏥 Faskes Semarang")
    menu = st.sidebar.radio("Pilih Menu:", ["Tambah", "Hapus", "Ringkasan"])

    if menu == "Tambah":
        halaman_input()
    elif menu == "Hapus":
        halaman_hapus()
    elif menu == "Ringkasan":
        halaman_ringkasan()

    st.sidebar.markdown("---")
    st.sidebar.caption("Sistem Informasi Fasilitas Kesehatan di Semarang")
    st.sidebar.caption("Septia Isnaeni Salsabila😼")

if __name__ == "__main__":
    main()
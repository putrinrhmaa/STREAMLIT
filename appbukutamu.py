import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# Class untuk mengelola data tamu
class BukuTamu:
    def __init__(self):
        # Inisialisasi data tamu di session_state
        if "data_tamu" not in st.session_state:
            st.session_state.data_tamu = []

    def tambah_tamu(self, nama, alamat, umur, jenis_kelamin, hadiah, pesan):
        # Tambahkan data tamu ke session_state
        st.session_state.data_tamu.append({
            "Nama": nama,
            "Alamat": alamat,
            "Umur": umur,
            "Jenis Kelamin": jenis_kelamin,
            "Hadiah": hadiah,
            "Pesan": pesan,
        })

    def semua_tamu(self):
        # Kembalikan data tamu sebagai DataFrame
        return pd.DataFrame(st.session_state.data_tamu)

    def filter_tamu(self, key, value):
        # Filter data tamu berdasarkan kunci dan nilai tertentu
        df = pd.DataFrame(st.session_state.data_tamu)
        return df[df[key] == value]

    def filter_umur(self, min_umur, max_umur):
        # Filter data tamu berdasarkan rentang umur
        df = pd.DataFrame(st.session_state.data_tamu)
        return df[(df["Umur"] >= min_umur) & (df["Umur"] <= max_umur)]


# Fungsi untuk menampilkan form input data
def input_data(buku_tamu):
    st.header("Input Data Tamu Baru")
    with st.form("form_tamu"):
        nama = st.text_input("Nama Lengkap", "")
        alamat = st.text_input("Alamat", "")
        umur = st.slider("Umur", 1, 50, 25)
        jenis_kelamin = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        hadiah = st.selectbox("Hadiah yang Dibawa", ["Money", "Gift"])
        pesan = st.text_area("Pesan atau Kesan", "")
        submit = st.form_submit_button("Simpan")

    if submit:
        if nama and alamat and pesan:
            buku_tamu.tambah_tamu(nama, alamat, umur, jenis_kelamin, hadiah, pesan)
            st.success(f"Data tamu '{nama}' berhasil disimpan!")
        else:
            st.error("Semua field harus diisi!")


# Fungsi untuk menampilkan data tamu
def tampilkan_data(buku_tamu, filter_type=None):
    if filter_type == "umur":
        st.header("Rekapitulasi Berdasarkan Rentang Usia")
        if st.session_state.data_tamu:
            min_umur, max_umur = st.slider("Pilih Rentang Umur", 1, 50, (1, 50))
            df_filtered = buku_tamu.filter_umur(min_umur, max_umur)
            if not df_filtered.empty:
                st.dataframe(df_filtered[["Nama", "Umur"]])
            else:
                st.info("Tidak ada tamu dalam rentang umur ini.")
        else:
            st.info("Belum ada data tamu.")
    elif filter_type in ["Jenis Kelamin", "Hadiah"]:
        st.header(f"Rekapitulasi Berdasarkan {filter_type}")
        if st.session_state.data_tamu:
            filter_value = st.radio(f"Pilih {filter_type}", ["Laki-laki", "Perempuan"] if filter_type == "Jenis Kelamin" else ["Money", "Gift"])
            df_filtered = buku_tamu.filter_tamu(filter_type, filter_value)
            if not df_filtered.empty:
                st.dataframe(df_filtered[["Nama", filter_type]])
            else:
                st.info(f"Tidak ada tamu dengan {filter_type} ini.")
        else:
            st.info("Belum ada data tamu.")
    else:
        st.header("Rekapitulasi Tamu Keseluruhan")
        df = buku_tamu.semua_tamu()
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("Belum ada tamu yang tercatat.")


# Sidebar navigation
with st.sidebar:
    st.title("Navigasi Aplikasi")
    selected = option_menu(
        menu_title="Rekapitulasi",
        options=["Input Data", "Tamu Keseluruhan", "Tamu Rentan Usia", "Tamu Jenis Kelamin", "Tamu Hadiah"],
        icons=["plus-circle", "list", "person", "gender-male", "gift"],
        default_index=0,
    )

# Judul Aplikasi
st.title("Buku Tamu Digital")

# Membuat objek BukuTamu
buku_tamu = BukuTamu()

# Konten berdasarkan menu yang dipilih
if selected == "Input Data":
    input_data(buku_tamu)
elif selected == "Tamu Keseluruhan":
    tampilkan_data(buku_tamu)
elif selected == "Tamu Rentan Usia":
    tampilkan_data(buku_tamu, filter_type="umur")
elif selected == "Tamu Jenis Kelamin":
    tampilkan_data(buku_tamu, filter_type="Jenis Kelamin")
elif selected == "Tamu Hadiah":
    tampilkan_data(buku_tamu, filter_type="Hadiah")

# Ekspor Data
if st.session_state.data_tamu:
    st.sidebar.download_button(
        label="Unduh Data Tamu",
        data=buku_tamu.semua_tamu().to_csv(index=False),
        file_name="data_tamu_digital.csv",
        mime="text/csv",
    )

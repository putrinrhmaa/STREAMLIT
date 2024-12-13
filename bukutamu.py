import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import os

# navigasi sidebar
with st.sidebar :
    selected = option_menu ('Rekaputasi',  ['Tamu Keseluruhan','Tamu Rentan Usia', 'Tamu Jenis kelamin', 'Tamu Hadiah'], default_index=0)

# fungsi validasi input
def validasi_input(Nama, Alamat, Email, Pesan):
    if not Nama or not Alamat or not Email or not Pesan:
        raise ValueError("semua kolom harus diisi")

# fungsi  kelas tamu
class Guest:
    def __init__(self, Nama, Alamat, Email, Pesan):
        self.Nama = Nama
        self.Alamat = Alamat
        self.Email = Email
        self.Pesan = Pesan

    def display_info(self):
        return f"Nama: {self.Nama}, {self.Alamat},{self.Email}, {self.Pesan}"

# fungsi menyimpan tamu
def save_guests_to_file(guests_list, filename='guests.pkl'):
    with open (filename, 'wb') as file:
        pickle.dump(guests_list, file)

# fungsi memuat tamu dari file
def load_guests_from_file(filename= 'guests.pkl'):
    if os.path.exists(filename):
        with open (filename= 'rb') as file:
            return pickle.load(file)
        return[]

# fungsi muat daftar tamu dari file
guests_list = load_guests_from_file()

# fungsi untuk menambahkan tamu
def add_guest(Nama, Alamat, Email, Pesan): 
    new_guest = Guest(Nama, Alamat, Email, Pesan)
    guests_list.append(new_guest)
    save_guests_to_file(guests_list)

# fungsi untuk menampilkan tamu
def display_guests():
    if guests_list:
        for guest in guests_list:
            st.write(guest.display_info())
    else:
        st.write("Belum Ada Tamu")
    
def handle_input(Nama, Alamat, Email, Pesan):
        try:
            validasi_input(Nama, Alamat, Email, Pesan)
            add_guest(Nama, Alamat, Email, Pesan)
            st.success("Tamu berhasil ditambahkan.")
        except ValueError as e:
            st.error(f"error: {e}")

# streamlit UI
st.title("Buku Tamu Digital")
st.subheader("Isi Data Tamu")

Nama = st.text_input("Nama")
Alamat = st.text_input("Alamat")
Email = st.text_input("Email")
Pesan = st.text_input("Pesan")


if st.button("Kirim"):
    handle_input(Nama, Alamat, Email, Pesan)

    st.subheader("Daftar Tamu")
    display_guests()

# Add a footer
footer = """
    <div class="footer">
        Made with Streamlit | © 2024 by Putri Nurrahmah
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)

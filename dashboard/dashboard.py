import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Konfigurasi Halaman
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# Judul Dashboard
st.title("🚲 Dashboard Analisis Data: Bike Sharing")
st.markdown("Dashboard interaktif ini menyajikan visualisasi data penyewaan sepeda berdasarkan musim dan pola waktu harian.")

# Memuat Data (Fungsi Caching untuk optimasi performa)
@st.cache_data
def load_data():
    # Menggunakan path dinamis agar aman dari error FileNotFoundError saat di-deploy
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "main_data.csv")
    
    df = pd.read_csv(file_path)
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

# Cek ketersediaan file biar kagak nge-crash
try:
    day_df = load_data()
except FileNotFoundError:
    st.error("Error: Berkas 'main_data.csv' kagak ketemu, bro. Pastikan berkas tersebut ada di folder yang sama dengan 'dashboard.py'.")
    st.stop()

# Menyiapkan Sidebar untuk Filter
st.sidebar.header("Filter Data")

# Menggunakan kolom 'season' yang valid biar bebas KeyError
season_options = day_df['season'].unique()
selected_season = st.sidebar.multiselect(
    "Pilih Musim (*Season*):",
    options=season_options,
    default=season_options
)

# Menerapkan filter pada dataset
filtered_df = day_df[day_df['season'].isin(selected_season)]

# Menampilkan Metrik Utama (Baris 1)
col1, col2 = st.columns(2)
with col1:
    total_rentals = filtered_df['cnt'].sum()
    st.metric("Total Penyewaan Sepeda (Filtered)", value=f"{total_rentals:,}")
with col2:
    avg_rentals = filtered_df['cnt'].mean()
    st.metric("Rata-rata Penyewaan Harian (Filtered)", value=f"{avg_rentals:,.2f}")

# Menampilkan Visualisasi 1: Pengaruh Musim (Baris 2)
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='season', y='cnt', data=filtered_df, errorbar=None, palette="viridis", ax=ax)
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_xlabel("Musim")
st.pyplot(fig)

# Menampilkan Visualisasi 2: Kategori Permintaan / Clustering (Baris 3)
st.subheader("Distribusi Kategori Permintaan Harian (Clustering Binning)")

# Bikin safety check: Pastiin kolom demand_category udah ke-generate di Colab
if 'demand_category' in filtered_df.columns:
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.countplot(x='demand_category', data=filtered_df, palette="coolwarm", ax=ax2)
    ax2.set_ylabel("Jumlah Hari")
    ax2.set_xlabel("Kategori Permintaan")
    st.pyplot(fig2)
else:
    st.warning("⚠️ Peringatan: Kolom 'demand_category' kagak ada di dataset lu. Pastiin proses Binning di Notebook udah dieksekusi dan di-save ke main_data.csv ya homie!")

# Informasi Tambahan di Bagian Bawah
st.caption("Proyek Submission Dicoding - Analisis Data dengan Python | Abdi Fhilipus Tampubolon")

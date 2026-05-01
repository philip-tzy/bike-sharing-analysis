import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Setup Page
st.title("Bike Sharing Analytics Dashboard")
st.markdown("Pantau tren penyewaan sepeda disini.")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

day_df = load_data()

# Setup Sidebar buat Filter Interaktif
st.sidebar.header("Filter Data")
season_filter = st.sidebar.multiselect(
    "Pilih Musim (*Season*):",
    options=day_df['season'].unique(),
    default=day_df['season'].unique()
)

# Apply Filter
filtered_df = day_df[day_df['season'].isin(season_filter)]

# Row 1: Metrics
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Penyewaan Sepeda (Filtered)", value=f"{filtered_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Sewa Harian (Filtered)", value=f"{round(filtered_df['cnt'].mean(), 2):,}")

# Row 2: Chart Bar Musim
st.subheader("Distribusi Rata-rata Penyewaan per Musim")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='season', y='cnt', data=filtered_df, errorbar=None, palette="coolwarm", ax=ax)
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_xlabel("Musim")
st.pyplot(fig)

# Row 3: Clustering (Binning) Chart
st.subheader("Kategori Tingkat Permintaan (Clustering Binning)")
fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.countplot(x='demand_category', data=filtered_df, palette="viridis", ax=ax2)
ax2.set_ylabel("Jumlah Hari")
ax2.set_xlabel("Kategori Demand")
st.pyplot(fig2)
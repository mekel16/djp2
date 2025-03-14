import streamlit as st
import pymysql
import pandas as pd
import plotly.express as px

# ---- Koneksi Database ----
db_config = {
    "host": "localhost",
    "user": "root",
    "database": "internship"
}


def get_connection():
    return pymysql.connect(**db_config)

def get_data():
    """Ambil data dari database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data_dashboard")
    
    column_names = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    
    conn.close()
    return pd.DataFrame(data, columns=column_names)

df = get_data()

if "Tahun Pajak" in df.columns:
    df["Tahun Pajak"] = df["Tahun Pajak"].fillna(0).astype(int)

# ---- Judul Dashboard ----
st.markdown("<h2 style='text-align: left; font-size: 24px; color: white; font-weight: bold;'>📊 Dashboard Data SP2DK OutStanding</h2>", 
            unsafe_allow_html=True)

st.sidebar.header("🔍 Filter Data")

if "Tahun Pajak" in df.columns and "Semester" in df.columns and "Lokasi" in df.columns:
    tahun_list = sorted(df["Tahun Pajak"].unique())  
    semester_list = sorted(df["Semester"].dropna().unique())  
    lokasi_list = sorted(df["Lokasi"].dropna().unique())  

    selected_tahun = st.sidebar.selectbox("📅 Pilih Tahun Pajak", ["Semua"] + list(map(str, tahun_list)))
    selected_semester = st.sidebar.selectbox("📖 Pilih Semester", ["Semua"] + list(semester_list))
    selected_lokasi = st.sidebar.selectbox("📍 Pilih Lokasi", ["Semua"] + list(lokasi_list))

    df_filtered = df.copy()
    if selected_tahun != "Semua":
        df_filtered = df_filtered[df_filtered["Tahun Pajak"] == int(selected_tahun)]

    if selected_semester != "Semua":
        df_filtered = df_filtered[df_filtered["Semester"] == selected_semester]

    if selected_lokasi != "Semua":
        df_filtered = df_filtered[df_filtered["Lokasi"] == selected_lokasi]

st.markdown(
    "<h3 style='text-align: left; font-size: 20px; color: white; font-weight: bold; margin-bottom: 10px;'>Total Potensi DPP</h3>", 
    unsafe_allow_html=True
)

def card_box(title, value, color="#4CAF50"):
    """Menampilkan card dengan jumlah total suatu kolom."""
    st.markdown(
        f"""
        <div style="
            background-color: {color}; 
            padding: 10px; 
            border-radius: 10px; 
            text-align: center;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            color: white;
            font-size: 18px;
            margin-bottom: 10px;
        ">
            <h4 style="margin: 5px 0px;">{title}</h4>
            <h2 style="margin: 5px 0px;">{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

col1 = st.columns(1)[0]  

if "Total Estimasi Potensi DPP" in df_filtered.columns:
    with col1:
        total_potensi = df_filtered["Total Estimasi Potensi DPP"].sum()
        card_box("Total Estimasi Potensi", f"Rp {total_potensi:,.0f}", "#4CAF50")

tampilkan_tabel = st.checkbox("📋 Tampilkan DataFrame")

if tampilkan_tabel:
    st.write(df_filtered)

def hist(df, column, row):
    """Menampilkan histogram dengan Plotly"""
    if column in df.columns and row in df.columns:
        df = df.dropna(subset=[column, row])  
        fig = px.histogram(df, x=column, y=row, nbins=20, title=f"{row} / {column}", text_auto=True)
        st.plotly_chart(fig)

if "Tahun Pajak" in df_filtered.columns and "Total Estimasi Potensi DPP" in df_filtered.columns:
    hist(df_filtered, "Tahun Pajak", "Total Estimasi Potensi DPP")

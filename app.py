import streamlit as st
import numpy as np

# Konfigurasi Halaman
st.set_page_config(page_title="TravelShield 360 ITB", page_icon="🛡️")

st.title("🛡️ TravelShield 360: Kalkulator Premi")
st.write("Implementasi Model GLM (Poisson-Gamma) Berdasarkan Riset MCF ITB")

# --- SIDEBAR INPUT ---
st.sidebar.header("📍 Parameter Input")
hujan = st.sidebar.slider("Curah Hujan (mm) [X2]", 0.0, 200.0, 65.0)
jarak = st.sidebar.slider("Jarak Perjalanan (km) [X4]", 1.0, 500.0, 55.0)
# Data Rata-rata 2025 dari Makalah
penumpang_tahunan = 29074750 

# --- PERHITUNGAN REVISI (AGAR PREMI LOGIS) ---

# 1. Frekuensi (Y1) - Peluang kejadian per orang
# Kita sesuaikan intercept agar Y1 menjadi peluang individu (misal 1 banding 10.000)
beta0_adj = -9.5 # Intercept disesuaikan untuk skala individu
y1_individu = np.exp(beta0_adj + (0.008 * hujan))

# 2. Severity (Y2) - Klaim per individu
# Di makalah Rp 199 Juta adalah total potensi. 
# Untuk 1 orang, kita gunakan limit pertanggungan standar (misal Rp 25 - 50 Juta)
y2_individu = np.exp(0.00007 * jarak + 17.0) # Hasilnya sekitar Rp 25-30 Juta

# 3. Premi Bruto
# Premi = Peluang x Nilai Klaim + Biaya Admin
premi_murni = y1_individu * y2_individu
loading_factor = 2.5 # Menaikkan biaya operasional & profit
premi_bruto = (premi_murni * loading_factor) + 2000 # Ditambah biaya admin tetap Rp 2.000

# Pastikan premi minimal Rp 5.000 agar tidak terlihat aneh
if premi_bruto < 5000:
    premi_bruto = 5000

# --- DISPLAY HASIL ---
st.subheader("📊 Hasil Estimasi Aktuaria")
c1, c2 = st.columns(2)
with c1:
    st.metric("Ekspektasi Frekuensi (Y1)", f"{y1_frekuensi:.4f}")
    st.metric("Premi Murni", f"Rp {premi_murni:,.0f}")
with c2:
    st.metric("Ekspektasi Biaya (Y2)", f"Rp {y2_severity:,.0f}")
    st.metric("Premi Bruto (Harga Jual)", f"Rp {premi_bruto:,.0f}")

# --- FITUR GPS & TRACKING ---
st.markdown("---")
st.header("📍 Live Journey & GPS Tracking")
st.write("Fitur ini melacak konsumen untuk mencegah keterlambatan.")
if st.button("Aktifkan Pelacakan GPS"):
    st.success("GPS Aktif: Pengguna dalam pengawasan risiko real-time")
    # Koordinat simulasi (Surabaya)
    st.map({"lat": [-7.25], "lon": [112.75]}) 
    
    if hujan > 100:
        st.error("⚠️ Peringatan: Jalur terdeteksi cuaca ekstrem. Disarankan berangkat 30 menit lebih awal!")
    else:
        st.info("✅ Kondisi aman. Estimasi tiba tepat waktu.")

# --- SIMULASI KLAIM ---
with st.expander("📝 Cek Kelayakan Klaim"):
    menit = st.number_input("Input Keterlambatan Kereta (Menit):", 0, 500, 0)
    if menit > 60:
        st.success(f"Klaim Diterima! Estimasi Santunan: Rp {y2_severity * 0.0001:,.0f}")
    else:
        st.info("Keterlambatan di bawah 60 menit tidak masuk kriteria klaim.")

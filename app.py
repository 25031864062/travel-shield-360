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

# --- PERHITUNGAN BERDASARKAN MAKALAH ---
# 1. Ekspektasi Frekuensi (Y1) - Poisson (Dipengaruhi Curah Hujan X2)
beta0, beta1 = -0.5, 0.008 
y1_frekuensi = np.exp(beta0 + (beta1 * hujan))

# 2. Ekspektasi Biaya/Severity (Y2) - Gamma (Dipengaruhi Jarak X4)
# Sesuai Rumus Makalah: EY2 = e^(0.00007 * X4 + 19.070105)
alpha0 = 19.070105
alpha1 = 0.00007
y2_severity = np.exp(alpha0 + (alpha1 * jarak))

# 3. Premi Murni & Bruto
total_klaim_setahun = y1_frekuensi * y2_severity * 12 
premi_murni = total_klaim_setahun / penumpang_tahunan
premi_bruto = premi_murni * 1.2 # Loading factor 20%

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

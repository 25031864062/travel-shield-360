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

# --- PERHITUNGAN REVISI BERDASARKAN MAKALAH ---

# 1. Frekuensi (Y1) - Menggunakan data Curah Hujan (X2)
# Koefisien beta disesuaikan agar menghasilkan probabilitas per perjalanan
y1_frekuensi = np.exp(-1.5 + (0.008 * hujan)) 

# 2. Severity (Y2) - Menggunakan data Jarak (X4)
# Sesuai Makalah: EY2 = e^(19.070105 + 0.00007 * X4)
alpha0 = 19.070105
alpha1 = 0.00007
y2_severity = np.exp(alpha0 + (alpha1 * jarak))

# 3. Kalkulasi Premi (Logika Aktuaria)
# Kita hitung premi murni per orang
# Total Klaim (Rp 201 Miliar) / Total Penumpang (29 Juta) = Rp 6.920
premi_murni_dasar = 6920 

# Kita buat dinamis: premi berubah mengikuti kenaikan risiko cuaca & jarak
faktor_risiko = (y1_frekuensi * (y2_severity / 199031493))
premi_murni_dinamis = premi_murni_dasar * faktor_risiko

# 4. Premi Bruto (Harga Jual)
# Ditambah Loading Factor 25% (untuk profit/admin) + Biaya Admin tetap Rp 2.500
premi_bruto = (premi_murni_dinamis * 1.25) + 2500

# Proteksi agar harga tetap pantas (Minimal Rp 5.000)
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

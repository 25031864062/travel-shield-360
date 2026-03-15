import streamlit as st
import numpy as np

# 1. Konfigurasi Tampilan
st.set_page_config(page_title="TravelShield 360 - ITB", page_icon="🛡️", layout="wide")

# Custom CSS agar tampilan lebih profesional
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_stdio=True)

st.title("🛡️ TravelShield 360: Kalkulator Premi Aktuaria")
st.write("Implementasi Model GLM (Poisson-Gamma) - Case Study: Kereta Api Indonesia 2025")

# --- SIDEBAR INPUT ---
st.sidebar.header("📍 Parameter Risiko")
hujan = st.sidebar.slider("Curah Hujan (mm) [X2]", 0.0, 250.0, 65.0)
jarak = st.sidebar.slider("Jarak Perjalanan (km) [X4]", 1.0, 800.0, 55.0)

st.sidebar.markdown("---")
st.sidebar.info("Data ini terhubung langsung dengan model regresi pada Makalah MCF ITB.")

# --- PERHITUNGAN INTI (LOGIKA MAKALAH) ---

# 1. Konstanta dari Makalah
total_penumpang_2025 = 29074750
biaya_klaim_tahunan = 201213297219  # Rp 201 Miliar
# Premi Murni Dasar (Hasil bagi total klaim / total penumpang)
premi_murni_dasar = biaya_klaim_tahunan / total_penumpang_2025 # Rp 6.920

# 2. Faktor Pengali Frekuensi (Y1 - Poisson)
# Kita bandingkan kondisi 'Hujan Saat Ini' dengan 'Rata-rata Hujan (65mm)'
# Menggunakan koefisien beta1 = 0.008 dari model
y1_faktor = np.exp(0.008 * (hujan - 65.0))

# 3. Faktor Pengali Keparahan (Y2 - Gamma)
# Menggunakan koefisien alpha1 = 0.00007 dari model
# Kita bandingkan 'Jarak Saat Ini' dengan 'Jarak Rata-rata (55km)'
y2_faktor = np.exp(0.00007 * (jarak - 55.0))

# 4. Kalkulasi Akhir
# Premi Murni menjadi dinamis mengikuti variabel X2 dan X4
premi_murni_dinamis = premi_murni_dasar * y1_faktor * y2_faktor

# Premi Bruto (Ditambah Loading Factor 20% untuk Profit & Admin + Biaya Flat Rp 2.500)
premi_bruto = (premi_murni_dinamis * 1.2) + 2500

# Proteksi agar tidak muncul angka aneh/terlalu kecil
if premi_bruto < 5000:
    premi_bruto = 5000

# --- DISPLAY HASIL ---
st.subheader("📊 Hasil Perhitungan Premi Per Penumpang")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Peluang Risiko (Y1 Factor)", f"{y1_faktor:.4f}x")
    st.caption("Kenaikan frekuensi akibat cuaca")

with col2:
    st.metric("Premi Murni", f"Rp {premi_murni_dinamis:,.0f}")
    st.caption("Beban risiko dasar per orang")

with col3:
    st.metric("Premi Bruto (Harga Jual)", f"Rp {premi_bruto:,.0f}")
    st.caption("Harga final termasuk biaya admin")

# --- FITUR GPS & MITIGASI ---
st.markdown("---")
col_a, col_b = st.columns([1, 2])

with col_a:
    st.header("📍 Live Tracking")
    if st.button("Cek Lokasi & Jalur Sekarang"):
        st.success("GPS Berhasil Terhubung")
        if hujan > 100:
            st.error("⚠️ Jalur Berisiko: Hujan Lebat Terdeteksi!")
            st.write("Saran: Gunakan perlindungan refund 100%.")
        else:
            st.info("✅ Jalur Aman: Perjalanan diprediksi lancar.")

with col_b:
    # Menampilkan Map Sederhana
    st.map({"lat": [-7.2504], "lon": [112.7508]}) # Koordinat Surabaya sebagai contoh

# --- SIMULASI KLAIM ---
st.markdown("---")
with st.expander("📝 Simulasi Klaim Keterlambatan"):
    menit = st.number_input("Input Menit Keterlambatan Kereta:", 0, 480, 0)
    if menit > 60:
        santunan = 500000 # Contoh santunan flat Rp 500rb
        st.balloons()
        st.success(f"Anda Berhak Klaim! Estimasi Santunan: Rp {santunan:,.0f}")
    else:
        st.write("Keterlambatan di bawah 60 menit belum memenuhi syarat klaim.")

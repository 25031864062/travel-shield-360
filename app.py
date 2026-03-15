import streamlit as st
import numpy as np
import pandas as pd

# 1. Konfigurasi Tampilan
st.set_page_config(
    page_title="TravelShield 360 - ITB",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS agar tampilan lebih profesional
st.markdown("""
<style>
.main {
    background-color: #f5f7f9;
}
div[data-testid="metric-container"] {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# Judul
st.title("🛡️ TravelShield 360: Kalkulator Premi Aktuaria")
st.write("Implementasi Model GLM (Poisson-Gamma) - Case Study: Kereta Api Indonesia 2025")

# ===============================
# SIDEBAR INPUT
# ===============================

st.sidebar.header("📍 Parameter Risiko")

hujan = st.sidebar.slider(
    "Curah Hujan (mm) [X2]",
    min_value=0.0,
    max_value=250.0,
    value=65.0
)

jarak = st.sidebar.slider(
    "Jarak Perjalanan (km) [X4]",
    min_value=1.0,
    max_value=800.0,
    value=55.0
)

st.sidebar.markdown("---")
st.sidebar.info("Data ini terhubung langsung dengan model regresi pada Makalah MCF ITB.")

# ===============================
# PERHITUNGAN AKTUARIA
# ===============================

# Konstanta dari Makalah
total_penumpang_2025 = 29074750
biaya_klaim_tahunan = 201213297219  # Rp 201 Miliar

# Premi Murni Dasar
premi_murni_dasar = biaya_klaim_tahunan / total_penumpang_2025

# Model Frekuensi (Poisson)
y1_faktor = np.exp(0.008 * (hujan - 65))

# Model Severity (Gamma)
y2_faktor = np.exp(0.00007 * (jarak - 55))

# Premi Murni Dinamis
premi_murni_dinamis = premi_murni_dasar * y1_faktor * y2_faktor

# Premi Bruto
premi_bruto = (premi_murni_dinamis * 1.2) + 2500

# Minimum premi
premi_bruto = max(premi_bruto, 5000)

# ===============================
# DISPLAY HASIL
# ===============================

st.subheader("📊 Hasil Perhitungan Premi Per Penumpang")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Peluang Risiko (Y1 Factor)",
        f"{y1_faktor:.4f}x"
    )
    st.caption("Kenaikan frekuensi akibat cuaca")

with col2:
    st.metric(
        "Premi Murni",
        f"Rp {premi_murni_dinamis:,.0f}".replace(",", ".")
    )
    st.caption("Beban risiko dasar per orang")

with col3:
    st.metric(
        "Premi Bruto (Harga Jual)",
        f"Rp {premi_bruto:,.0f}".replace(",", ".")
    )
    st.caption("Harga final termasuk biaya admin")

# ===============================
# GRAFIK PREMI
# ===============================

st.markdown("---")
st.subheader("📈 Visualisasi Premi")

chart_data = pd.DataFrame({
    "Jenis Premi": ["Premi Murni", "Premi Bruto"],
    "Nilai": [premi_murni_dinamis, premi_bruto]
})

st.bar_chart(chart_data.set_index("Jenis Premi"))

# ===============================
# GPS & MITIGASI RISIKO
# ===============================

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

    st.header("🗺️ Lokasi Kereta (Simulasi)")

    map_data = pd.DataFrame({
        "lat": [-7.2504],
        "lon": [112.7508]
    })

    st.map(map_data)

# ===============================
# SIMULASI KLAIM
# ===============================

st.markdown("---")

with st.expander("📝 Simulasi Klaim Keterlambatan"):

    menit = st.number_input(
        "Input Menit Keterlambatan Kereta:",
        min_value=0,
        max_value=480,
        value=0
    )

    if menit > 60:

        santunan = 500000

        st.balloons()

        st.success(
            f"Anda Berhak Klaim! Estimasi Santunan: Rp {santunan:,.0f}".replace(",", ".")
        )

    else:

        st.write("Keterlambatan di bawah 60 menit belum memenuhi syarat klaim.")

import streamlit as st
import numpy as np
import pandas as pd

# ===============================
# KONFIGURASI HALAMAN
# ===============================

st.set_page_config(
    page_title="TravelShield 360",
    page_icon="🛡️",
    layout="wide"
)

# ===============================
# CSS TAMPILAN
# ===============================

st.markdown("""
<style>
.main {
    background-color: #f5f7f9;
}
div[data-testid="metric-container"] {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# JUDUL
# ===============================

st.title("🛡️ TravelShield 360")
st.subheader("Kalkulator Premi Aktuaria Kereta Api")

st.write(
"Model menggunakan pendekatan **GLM Poisson-Gamma** untuk menghitung premi perjalanan."
)

# ===============================
# SIDEBAR INPUT
# ===============================

st.sidebar.header("Parameter Risiko")

hujan = st.sidebar.slider(
    "Curah Hujan (mm)",
    0.0, 250.0, 65.0
)

jarak = st.sidebar.slider(
    "Jarak Perjalanan (km)",
    1.0, 800.0, 55.0
)

harga_tiket = st.sidebar.slider(
    "Harga Tiket (Rp)",
    20000, 600000, 150000, step=5000
)

# ===============================
# PERHITUNGAN AKTUARIA
# ===============================

total_penumpang = 29074750
biaya_klaim_tahunan = 201213297219

premi_dasar = biaya_klaim_tahunan / total_penumpang

# Faktor risiko
y1 = np.exp(0.008 * (hujan - 65))
y2 = np.exp(0.00007 * (jarak - 55))

harga_rata = 150000
y3 = np.exp(0.000002 * (harga_tiket - harga_rata))

# Premi murni
premi_murni = premi_dasar * y1 * y2 * y3

# Premi bruto
premi_bruto = (premi_murni * 1.2) + 2500
premi_bruto = max(premi_bruto, 5000)

# ===============================
# HASIL PERHITUNGAN
# ===============================

st.subheader("Hasil Perhitungan Premi")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Faktor Cuaca", f"{y1:.3f}x")
col2.metric("Faktor Jarak", f"{y2:.3f}x")
col3.metric("Faktor Harga Tiket", f"{y3:.3f}x")
col4.metric(
    "Premi Bruto",
    f"Rp {premi_bruto:,.0f}".replace(",", ".")
)

# ===============================
# GRAFIK PREMI
# ===============================

st.markdown("---")

st.subheader("Visualisasi Premi")

data_chart = pd.DataFrame({
    "Jenis Premi": ["Premi Murni", "Premi Bruto"],
    "Nilai": [premi_murni, premi_bruto]
})

st.bar_chart(data_chart.set_index("Jenis Premi"))

# ===============================
# PETA LOKASI
# ===============================

st.markdown("---")

st.subheader("Lokasi Kereta (Simulasi)")

map_data = pd.DataFrame({
    "lat": [-7.2504],
    "lon": [112.7508]
})

st.map(map_data)

# ===============================
# SIMULASI KLAIM
# ===============================

st.markdown("---")

st.subheader("Simulasi Klaim")

jenis_klaim = st.selectbox(
    "Pilih Jenis Klaim",
    [
        "Keterlambatan Kereta",
        "Pembatalan Perjalanan"
    ]
)

# ===============================
# KLAIM DELAY
# ===============================

if jenis_klaim == "Keterlambatan Kereta":

    menit = st.number_input(
        "Masukkan keterlambatan (menit)",
        0, 480, 0
    )

    if menit >= 60:

        santunan = harga_tiket

        st.balloons()

        st.success(
            f"Klaim Disetujui! Refund 100% Tiket: Rp {santunan:,.0f}".replace(",", ".")
        )

    else:

        st.warning(
            "Keterlambatan kurang dari 60 menit tidak memenuhi syarat klaim."
        )

# ===============================
# KLAIM PEMBATALAN
# ===============================

if jenis_klaim == "Pembatalan Perjalanan":

    alasan = st.selectbox(
        "Alasan Pembatalan",
        [
            "Sakit / Darurat",
            "Cuaca Ekstrem",
            "Gangguan Operasional",
            "Perubahan Rencana"
        ]
    )

    if st.button("Ajukan Klaim"):

        santunan = harga_tiket

        st.balloons()

        st.success(
            f"Klaim Pembatalan Disetujui! Refund 100% Tiket: Rp {santunan:,.0f}".replace(",", ".")
        )

        st.info(f"Alasan pembatalan: {alasan}")

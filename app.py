import streamlit as st
import numpy as np
import pandas as pd

# ===============================
# KONFIGURASI HALAMAN
# ===============================

st.set_page_config(
    page_title="TravelShield 360 - ITB",
    page_icon="🛡️",
    layout="wide"
)

# CSS tampilan
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

# ===============================
# JUDUL
# ===============================

st.title("🛡️ TravelShield 360: Kalkulator Premi Aktuaria")
st.write("Implementasi Model GLM (Poisson-Gamma) - Case Study: Kereta Api Indonesia")

# ===============================
# SIDEBAR INPUT
# ===============================

st.sidebar.header("📍 Parameter Risiko")

hujan = st.sidebar.slider(
    "Curah Hujan (mm) [X2]",
    0.0, 250.0, 65.0
)

jarak = st.sidebar.slider(
    "Jarak Perjalanan (km) [X4]",
    1.0, 800.0, 55.0
)

harga_tiket = st.sidebar.slider(
    "Harga Tiket (Rp) [X5]",
    20000, 600000, 150000, step=5000
)

st.sidebar.markdown("---")
st.sidebar.info("Model ini menggunakan pendekatan GLM Poisson-Gamma.")

# ===============================
# PERHITUNGAN AKTUARIA
# ===============================

total_penumpang = 29074750
biaya_klaim_tahunan = 201213297219

premi_murni_dasar = biaya_klaim_tahunan / total_penumpang

# Faktor Frekuensi (Poisson)
y1_faktor = np.exp(0.008 * (hujan - 65))

# Faktor Severity (Jarak)
y2_faktor = np.exp(0.00007 * (jarak - 55))

# Faktor Harga Tiket
harga_rata = 150000
y3_faktor = np.exp(0.000002 * (harga_tiket - harga_rata))

# Premi Murni Dinamis
premi_murni_dinamis = premi_murni_dasar * y1_faktor * y2_faktor * y3_faktor

# Premi Bruto
premi_bruto = (premi_murni_dinamis * 1.2) + 2500
premi_bruto = max(premi_bruto, 5000)

# ===============================
# HASIL PERHITUNGAN
# ===============================

st.subheader("📊 Hasil Perhitungan Premi")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Faktor Risiko Cuaca", f"{y1_faktor:.3f}x")

with col2:
    st.metric("Faktor Risiko Jarak", f"{y2_faktor:.3f}x")

with col3:
    st.metric("Faktor Harga Tiket", f"{y3_faktor:.3f}x")

with col4:
    st.metric(
        "Premi Bruto",
        f"Rp {premi_bruto:,.0f}".replace(",", ".")
    )

# ===============================
# VISUALISASI
# ===============================

st.markdown("---")
st.subheader("📈 Komponen Premi")

chart_data = pd.DataFrame({
    "Komponen": ["Premi Murni", "Premi Bruto"],
    "Nilai": [premi_murni_dinamis, premi_bruto]
})

st.bar_chart(chart_data.set_index("Komponen"))

# ===============================
# LIVE TRACKING
# ===============================

st.markdown("---")

col_a, col_b = st.columns([1,2])

with col_a:

    st.header("📍 Live Tracking")

    if st.button("Cek Lokasi & Jalur Sekarang"):

        st.success("GPS Berhasil Terhubung")

        if hujan > 100:
            st.error("⚠️ Jalur Berisiko: Hujan Lebat!")
        else:
            st.info("✅ Jalur Aman")

with col_b:

    map_data = pd.DataFrame({
        "lat":[-7.2504],
        "lon":[112.7508]
    })

    st.map(map_data)

# ===============================
# SIMULASI KLAIM
# ===============================

st.markdown("---")

with st.expander("📝 Simulasi Klaim Keterlambatan"):

    menit = st.number_input(
        "Input Menit Keterlambatan Kereta",
        0, 480, 0
    )

    if menit > 60:

        santunan = harga_tiket * 2

        st.balloons()

        st.success(
            f"Anda Berhak Klaim! Estimasi Santunan: Rp {santunan:,.0f}".replace(",", ".")
        )

    else:

        st.write("Keterlambatan di bawah 60 menit belum memenuhi syarat klaim.")

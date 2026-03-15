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

st.title("🛡️ TravelShield 360")
st.subheader("Dashboard Aktuaria Risiko Perjalanan Kereta")

st.write(
"Model ini menggunakan pendekatan **Poisson Frequency Model** untuk estimasi klaim."
)

# ===============================
# SIDEBAR INPUT VARIABEL RISIKO
# ===============================

st.sidebar.header("Parameter Risiko")

hujan = st.sidebar.slider(
"Curah Hujan (mm)",0,200,60
)

jarak = st.sidebar.slider(
"Jarak Perjalanan (km)",10,500,100
)

harga = st.sidebar.slider(
"Harga Tiket (Rp)",50000,400000,150000
)

kepadatan = st.sidebar.slider(
"Kepadatan Penumpang",0.3,1.0,0.6
)

jam = st.sidebar.slider(
"Jam Perjalanan",0,23,12
)

jenis = st.sidebar.selectbox(
"Jenis Kereta",
["Ekonomi","Bisnis","Eksekutif"]
)

# encoding jenis kereta
jenis_map = {
"Ekonomi":0,
"Bisnis":1,
"Eksekutif":2
}

jenis_val = jenis_map[jenis]

# ===============================
# MODEL POISSON (MANUAL GLM)
# ===============================

lambda_claim = np.exp(
-3
+0.01*hujan
+0.002*jarak
+0.000002*harga
+1.2*kepadatan
+0.03*jam
+0.2*jenis_val
)

# severity (nilai klaim)
severity = harga

# premi aktuaria
premi = lambda_claim * severity

# ===============================
# DASHBOARD METRIC
# ===============================

st.markdown("---")

col1,col2,col3 = st.columns(3)

col1.metric(
"Expected Claim Frequency",
round(lambda_claim,4)
)

col2.metric(
"Severity",
f"Rp {severity:,.0f}".replace(",",".")
)

col3.metric(
"Premi Aktuaria",
f"Rp {premi:,.0f}".replace(",",".")
)

# ===============================
# SIMULASI DISTRIBUSI KLAIM
# ===============================

st.markdown("---")
st.subheader("Simulasi Distribusi Klaim")

np.random.seed(42)

sim_claim = np.random.poisson(lambda_claim,1000)

df_chart = pd.DataFrame(sim_claim,columns=["klaim"])

st.bar_chart(df_chart.value_counts())

# ===============================
# PETA SIMULASI LOKASI
# ===============================

st.markdown("---")
st.subheader("Simulasi Lokasi Kereta")

map_data = pd.DataFrame({
"lat":[-7.2504],
"lon":[112.7508]
})

st.map(map_data)

# ===============================
# SIMULASI KLAIM
# ===============================

st.markdown("---")
st.subheader("Simulasi Klaim")

jenis_klaim = st.selectbox(
"Pilih Jenis Klaim",
["Delay Kereta","Pembatalan Perjalanan"]
)

if jenis_klaim == "Delay Kereta":

    delay = st.number_input(
    "Keterlambatan (menit)",0,300
    )

    if delay >= 60:

        santunan = harga

        st.success(
        f"Refund 100% Tiket: Rp {santunan:,.0f}".replace(",",".")
        )

    else:

        st.warning(
        "Delay kurang dari 60 menit tidak memenuhi syarat klaim"
        )

if jenis_klaim == "Pembatalan Perjalanan":

    if st.button("Ajukan Refund"):

        santunan = harga

        st.success(
        f"Refund 100% Tiket: Rp {santunan:,.0f}".replace(",",".")
        )
    

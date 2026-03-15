import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import PoissonRegressor

# ===============================
# KONFIGURASI HALAMAN
# ===============================

st.set_page_config(
    page_title="TravelShield 360 Dashboard",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ TravelShield 360")
st.subheader("Dashboard Aktuaria Risiko Perjalanan Kereta")

# ===============================
# GENERATE DATA SIMULASI
# ===============================

np.random.seed(42)

n = 1000

data = pd.DataFrame({
    "hujan": np.random.uniform(0,200,n),
    "jarak": np.random.uniform(10,500,n),
    "harga_tiket": np.random.uniform(50000,400000,n),
    "kepadatan": np.random.uniform(0.3,1.0,n),
    "jam": np.random.randint(0,24,n)
})

data["jenis_kereta"] = np.random.choice([0,1,2],n)

lambda_claim = np.exp(
    -3
    +0.01*data["hujan"]
    +0.002*data["jarak"]
    +0.000002*data["harga_tiket"]
    +1.2*data["kepadatan"]
    +0.03*data["jam"]
    +0.2*data["jenis_kereta"]
)

data["klaim"] = np.random.poisson(lambda_claim)

# ===============================
# TRAIN MODEL
# ===============================

X = data[[
"hujan",
"jarak",
"harga_tiket",
"kepadatan",
"jam",
"jenis_kereta"
]]

y = data["klaim"]

model = PoissonRegressor()
model.fit(X,y)

# ===============================
# SIDEBAR INPUT
# ===============================

st.sidebar.header("Parameter Risiko")

hujan = st.sidebar.slider("Curah Hujan (mm)",0,200,60)

jarak = st.sidebar.slider("Jarak Perjalanan (km)",10,500,100)

harga = st.sidebar.slider("Harga Tiket (Rp)",50000,400000,150000)

kepadatan = st.sidebar.slider(
"Kepadatan Penumpang",
0.3,1.0,0.6
)

jam = st.sidebar.slider(
"Jam Perjalanan",
0,23,12
)

jenis = st.sidebar.selectbox(
"Jenis Kereta",
["Ekonomi","Bisnis","Eksekutif"]
)

jenis_map = {
"Ekonomi":0,
"Bisnis":1,
"Eksekutif":2
}

jenis_val = jenis_map[jenis]

# ===============================
# PREDIKSI MODEL
# ===============================

input_df = pd.DataFrame({
"hujan":[hujan],
"jarak":[jarak],
"harga_tiket":[harga],
"kepadatan":[kepadatan],
"jam":[jam],
"jenis_kereta":[jenis_val]
})

freq = model.predict(input_df)[0]

severity = harga

premi = freq * severity

# ===============================
# DASHBOARD METRIC
# ===============================

col1,col2,col3 = st.columns(3)

col1.metric("Expected Claim Frequency",round(freq,4))

col2.metric(
"Severity",
f"Rp {severity:,.0f}".replace(",",".")
)

col3.metric(
"Premi Aktuaria",
f"Rp {premi:,.0f}".replace(",",".")
)

# ===============================
# GRAFIK DISTRIBUSI KLAIM
# ===============================

st.markdown("---")
st.subheader("Distribusi Klaim")

chart_data = data["klaim"].value_counts().sort_index()

st.bar_chart(chart_data)

# ===============================
# PETA SIMULASI
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

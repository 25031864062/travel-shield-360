import streamlit as st
import math

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="TravelShield 360", page_icon="🛡️", layout="centered")

# --- FUNGSI INTI AKTUARIA (DARI KODE SEBELUMNYA) ---
def hitung_layanan_travelshield(jarak_km, curah_hujan_mm, tipe_asuransi):
    # Parameter GLM
    beta_0, beta_1, alpha_1 = -10.12, 0.005, 0.000777
    alpha_0 = 15.5 if tipe_asuransi == "Ekonomi" else 17.7 if tipe_asuransi == "Premium" else 19.07
    
    # Kalkulasi Aktuaria
    peluang_y1 = (jarak_km / 59.47) * math.exp(beta_0 + (beta_1 * curah_hujan_mm))
    biaya_y2 = math.exp(alpha_0 + (alpha_1 * curah_hujan_mm))
    
    # Pricing
    tarif_tiket = jarak_km * 1500
    premi = round((peluang_y1 * biaya_y2 / 0.70) / 500) * 500
    if premi < 2000: premi = 2000
    
    return tarif_tiket, premi, peluang_y1, biaya_y2

# --- TAMPILAN WEBSITE ---
st.title("🛡️ TravelShield 360")
st.subheader("Sistem Proteksi Perjalanan Berbasis Risiko Cuaca")
st.markdown("---")

# --- SIDEBAR INPUT ---
st.sidebar.header("Konfigurasi Perjalanan")
jarak = st.sidebar.slider("Jarak Tempuh (KM)", 10, 500, 100)
hujan = st.sidebar.number_input("Curah Hujan (mm)", min_value=0, max_value=300, value=50)
tipe = st.sidebar.selectbox("Tipe Perlindungan", ["Ekonomi", "Premium", "Luxury"])

# --- PROSES DATA ---
tiket, premi, prob, limit = hitung_layanan_travelshield(jarak, hujan, tipe)

# --- PANEL UTAMA ---
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Harga Tiket Dasar", value=f"Rp {tiket:,.0f}")
    st.metric(label="Premi Asuransi", value=f"Rp {premi:,.0f}")

with col2:
    st.metric(label="Peluang Risiko", value=f"{prob*100:.4f}%")
    st.metric(label="Limit Santunan", value=f"Rp {limit:,.0f}")

st.info(f"**Total Pembayaran: Rp {tiket + premi:,.0f}**")

# --- FITUR REFUND & KLAIM ---
st.markdown("### 📋 Simulasi Klaim & Refund")
tab1, tab2 = st.tabs(["Klaim Keterlambatan", "Pembatalan Tiket"])

with tab1:
    menit = st.number_input("Menit Keterlambatan Kereta", 0, 300, 0)
    if menit > 30:
        refund_val = tiket * (0.25 if menit <= 60 else 0.5 if menit <= 120 else 1.0)
        st.success(f"Anda Berhak Klaim Refund: **Rp {refund_val:,.0f}**")
    else:
        st.write("Keterlambatan di bawah 30 menit tidak mendapatkan kompensasi.")

with tab2:
    alasan = st.selectbox("Alasan Pembatalan", ["Pribadi", "Sakit/Darurat"])
    if st.button("Proses Refund Tiket"):
        persen = 1.0 if alasan == "Sakit/Darurat" else 0.75
        st.warning(f"Dana Refund dikembalikan: **Rp {tiket * persen:,.0f}** ({int(persen*100)}%)")

st.markdown("---")
st.caption("© 2026 TravelShield 360 - Aktuaria Digital untuk Moda Kereta Api")
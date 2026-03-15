# ===============================
# SIMULASI KLAIM
# ===============================

st.markdown("---")

with st.expander("📝 Simulasi Klaim Perjalanan"):

    jenis_klaim = st.selectbox(
        "Pilih Jenis Klaim",
        ["Keterlambatan Kereta", "Pembatalan Perjalanan"]
    )

    if jenis_klaim == "Keterlambatan Kereta":

        menit = st.number_input(
            "Input Menit Keterlambatan",
            min_value=0,
            max_value=480,
            value=0
        )

        if menit >= 60:

            santunan = harga_tiket

            st.balloons()

            st.success(
                f"Anda Berhak Klaim 100% Tiket!\n"
                f"Refund: Rp {santunan:,.0f}".replace(",", ".")
            )

        else:

            st.warning(
                "Keterlambatan di bawah 60 menit belum memenuhi syarat klaim."
            )

    elif jenis_klaim == "Pembatalan Perjalanan":

        alasan = st.selectbox(
            "Pilih Alasan Pembatalan",
            [
                "Sakit / Darurat",
                "Cuaca Ekstrem",
                "Gangguan Operasional",
                "Perubahan Rencana Perjalanan"
            ]
        )

        if st.button("Ajukan Klaim Pembatalan"):

            santunan = harga_tiket

            st.balloons()

            st.success(
                f"Klaim Pembatalan Disetujui!\n"
                f"Refund 100% Tiket: Rp {santunan:,.0f}".replace(",", ".")
            )

            st.info(f"Alasan Pembatalan: {alasan}")

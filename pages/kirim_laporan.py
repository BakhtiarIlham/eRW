import streamlit as st
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds

from datetime import date


def render():
    user = st.session_state.get("user", {})
    nama = user.get("nama", "")

    st.markdown(
        '<div class="page-title">📩 Kirim Laporan / Pengaduan</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Sampaikan keluhan atau pengaduan kepada pengurus RW</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">📝 Form Pengaduan</div><br>',
        unsafe_allow_html=True
    )

    judul = st.text_input(
        "Judul Laporan *",
        placeholder="Contoh: Lampu jalan mati di RT 02"
    )

    deskripsi = st.text_area(
        "Deskripsi Lengkap *",
        height=150,
        placeholder="Jelaskan masalah yang Anda alami secara detail: lokasi, waktu kejadian, dampak yang dirasakan..."
    )

    lampiran = st.file_uploader(
        "📎 Upload Lampiran Bukti",
        type=["jpg", "jpeg", "png", "pdf"]
    )

    if lampiran:
        st.success(f"File dipilih: {lampiran.name}")

    st.markdown(
        """
        <div class="info-box">
            ℹ️ Laporan Anda akan diverifikasi oleh Pengurus RT/RW terlebih dahulu sebelum diteruskan ke Petugas Operasional.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_b, _ = st.columns([2, 4])

    with col_b:
        if st.button(
            "📤 Kirim Laporan",
            type="primary",
            use_container_width=True
        ):

            if not judul:
                st.error("Judul laporan wajib diisi.")
                return

            if not deskripsi:
                st.error("Deskripsi laporan wajib diisi.")
                return

            warga_list = ds.get("warga")

            w = next(
                (x for x in warga_list if x["nama"] == nama),
                {"id": 1}
            )

            current = ds.get("laporan")

            new_id = max(
                (l["id"] for l in current),
                default=0
            ) + 1

            current.append({
                "id": new_id,
                "id_warga": w["id"],
                "nama": nama,
                "judul": judul,
                "deskripsi": deskripsi,
                "tanggal": str(date.today()),
                "status": "Menunggu",
                "petugas": "",
                "catatan": "",
                "lampiran": lampiran.name if lampiran else "-"
            })

            ds.set_data("laporan", current)

            st.success(
                "✅ Laporan berhasil dikirim. Silakan cek menu Status Laporan untuk melihat perkembangan laporan Anda."
            )

            st.balloons()

    st.markdown('</div>', unsafe_allow_html=True)
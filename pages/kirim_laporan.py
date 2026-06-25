import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds
from app import render_section_header, html_block
from datetime import date


def render():
    user = st.session_state.get("user", {})
    nama = user.get("nama", "")

    render_section_header(
        "📩 Kirim Laporan / Pengaduan",
        "Sampaikan keluhan atau pengaduan kepada pengurus RW",
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📝 Form Pengaduan</div><br>', unsafe_allow_html=True)

    judul = st.text_input("Judul Laporan *", placeholder="Contoh: Lampu jalan mati di RT 02")
    deskripsi = st.text_area(
        "Deskripsi Lengkap *",
        height=150,
        placeholder="Jelaskan masalah yang Anda alami secara detail: lokasi, waktu kejadian, dampak yang dirasakan..."
    )

    uploaded_file = st.file_uploader(
        "📎 Lampirkan Foto/Dokumen Bukti (opsional)",
        type=["jpg", "jpeg", "png", "pdf"],
        help="Unggah foto kondisi lapangan atau dokumen pendukung lainnya untuk memperkuat laporan Anda.",
    )
    if uploaded_file is not None:
        size_kb = round(uploaded_file.size / 1024, 1)
        icon = "📄" if uploaded_file.type == "application/pdf" else "🖼️"
        html_block(
            f"""<div class="file-chip">
              <div class="fi">{icon}</div>
              <div>
                <div class="fn">{uploaded_file.name}</div>
                <div class="fs">{size_kb} KB · {uploaded_file.type}</div>
              </div>
            </div>"""
        )
        if uploaded_file.type in ["image/jpeg", "image/png"]:
            st.image(uploaded_file, caption="Pratinjau lampiran", width=260)

    html_block(
        """<div class="info-box">
          ℹ️ Laporan Anda akan diverifikasi oleh Pengurus RT/RW terlebih dahulu sebelum diteruskan ke Petugas Operasional.
        </div>"""
    )

    col_b, _ = st.columns([2, 4])
    with col_b:
        if st.button("📤 Kirim Laporan", type="primary", use_container_width=True):
            if judul and deskripsi:
                warga_list = ds.get("warga")
                w = next((x for x in warga_list if x["nama"] == nama), {"id": 1})
                current = ds.get("laporan")
                new_id  = max((l["id"] for l in current), default=0) + 1
                lampiran = None
                if uploaded_file is not None:
                    lampiran = {
                        "nama_file": uploaded_file.name,
                        "ukuran_kb": round(uploaded_file.size / 1024, 1),
                        "tipe": uploaded_file.type,
                    }
                current.append({
                    "id": new_id, "id_warga": w["id"], "nama": nama,
                    "judul": judul, "deskripsi": deskripsi,
                    "tanggal": str(date.today()), "status": "Menunggu",
                    "petugas": "", "catatan": "", "lampiran": lampiran,
                    "riwayat": [{"status": "Menunggu", "tanggal": str(date.today()), "oleh": nama}],
                })
                ds.set_data("laporan", current)
                st.success("✅ Laporan Anda berhasil dikirim! Silakan pantau statusnya di menu Status Laporan.")
                st.balloons()
            else:
                st.error("Judul dan deskripsi wajib diisi.")

    st.markdown('</div>', unsafe_allow_html=True)

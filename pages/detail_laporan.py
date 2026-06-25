"""detail_laporan.py — Halaman detail satu laporan warga (klik dari mana saja).
Menampilkan kronologi/timeline status, lampiran (simulasi file upload), dan
aksi lanjutan sesuai peran yang sedang login.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds
from app import render_section_header, html_block
from datetime import date

BADGE = {"Menunggu": "badge-gray", "Diverifikasi": "badge-yellow", "Diproses": "badge-blue", "Selesai": "badge-green", "Ditolak": "badge-red"}
ICON  = {"Menunggu": "🕓", "Diverifikasi": "✅", "Diproses": "🔧", "Selesai": "🏁", "Ditolak": "✖"}
FILE_ICON = {"image/jpeg": "🖼️", "image/png": "🖼️", "application/pdf": "📄"}


def render():
    user = st.session_state.get("user", {})
    role = user.get("role", "")
    nama = user.get("nama", "")

    laporan_id = st.session_state.get("detail_laporan_id")
    laporan_list = ds.get("laporan")
    l = next((x for x in laporan_list if x["id"] == laporan_id), None)

    render_section_header(
        "📋 Detail Laporan",
        "Kronologi penanganan dan lampiran laporan",
    )

    back_to = st.session_state.get("detail_laporan_back", "laporan")
    if st.button("⬅ Kembali"):
        st.session_state["current_page"] = back_to
        st.rerun()

    if not l:
        st.warning("Laporan tidak ditemukan.")
        return

    # Akses: warga hanya boleh lihat laporan miliknya sendiri
    if role == "Warga" and l["nama"] != nama:
        st.error("🚫 Anda tidak memiliki akses untuk melihat laporan ini.")
        return

    badge_cls = BADGE.get(l["status"], "badge-gray")

    # ── Header laporan ──────────────────────────────────────────────────────
    html_block(
        f"""<div class="card">
          <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
              <span style="font-weight:700; font-size:1.1rem; color:#1E3A8A;">{l['judul']}</span>
              <span class="badge {badge_cls}" style="margin-left:10px;">{l['status']}</span>
              <div style="font-size:0.82rem; color:#6B7280; margin:6px 0 10px;">
                👤 Pelapor: <b>{l['nama']}</b> &nbsp;·&nbsp; 📅 {l['tanggal']}
                {f"&nbsp;·&nbsp; 🔧 Ditangani: {l['petugas']}" if l.get('petugas') else ''}
              </div>
              <div style="font-size:0.9rem; color:#374151; line-height:1.6;">{l['deskripsi']}</div>
            </div>
          </div>
        </div>"""
    )

    # ── Lampiran file (simulasi) ────────────────────────────────────────────
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📎 Lampiran</div>', unsafe_allow_html=True)
    lampiran = l.get("lampiran")
    if lampiran:
        fi = FILE_ICON.get(lampiran.get("tipe"), "📎")
        html_block(
            f"""<div class="file-chip">
              <div class="fi">{fi}</div>
              <div>
                <div class="fn">{lampiran['nama_file']}</div>
                <div class="fs">{lampiran['ukuran_kb']} KB · {lampiran['tipe']}</div>
              </div>
            </div>"""
        )
        st.caption("ℹ️ Ini adalah simulasi metadata file pada demo — pratinjau/unduh file sungguhan tidak tersedia di mode demo ini.")
        st.button("👁️ Pratinjau Lampiran (demo)", key=f"preview_{l['id']}", disabled=True)
    else:
        st.markdown('<p style="color:#9CA3AF; font-size:0.85rem;">Laporan ini tidak memiliki lampiran file.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Timeline status ──────────────────────────────────────────────────────
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🕒 Kronologi Status</div><br>', unsafe_allow_html=True)
    riwayat = l.get("riwayat", [])
    if riwayat:
        tl_html = ""
        for r in riwayat:
            icon = ICON.get(r["status"], "•")
            tl_html += (
                f'<div class="tl-item">'
                f'<div class="tl-dot">{icon}</div>'
                f'<div>'
                f'<div class="tl-text">{r["status"]}</div>'
                f'<div class="tl-meta">{r["tanggal"]} · oleh {r["oleh"]}</div>'
                f'</div>'
                f'</div>'
            )
        html_block(tl_html)
    else:
        st.markdown('<p style="color:#9CA3AF; font-size:0.85rem;">Belum ada riwayat status.</p>', unsafe_allow_html=True)

    if l.get("catatan"):
        html_block(
            f"""<div style='margin-top:8px; background:#ECFDF5; border-radius:8px; padding:10px 14px; font-size:0.85rem; color:#065F46;'>
              📝 <b>Catatan Petugas:</b> {l['catatan']}
            </div>"""
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Aksi sesuai peran ────────────────────────────────────────────────────
    def _update_status(new_status, extra=None):
        current = ds.get("laporan")
        for item in current:
            if item["id"] == l["id"]:
                item["status"] = new_status
                item.setdefault("riwayat", []).append({
                    "status": new_status,
                    "tanggal": str(date.today()),
                    "oleh": nama,
                })
                if extra:
                    item.update(extra)
        ds.set_data("laporan", current)

    if role in ["Pengurus RW", "Pengurus RT"] and l["status"] == "Menunggu":
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⚙️ Aksi Verifikasi</div><br>', unsafe_allow_html=True)
        cb1, cb2, _ = st.columns([1.5, 1.5, 5])
        with cb1:
            if st.button("✅ Verifikasi", key=f"d_ver_{l['id']}", type="primary"):
                _update_status("Diverifikasi")
                st.success("Laporan diverifikasi.")
                st.rerun()
        with cb2:
            if st.button("❌ Tolak", key=f"d_tol_{l['id']}"):
                _update_status("Ditolak")
                st.warning("Laporan ditolak.")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if role == "Petugas Operasional" and l["status"] == "Diverifikasi":
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⚙️ Aksi Petugas</div><br>', unsafe_allow_html=True)
        if st.button("🔧 Ambil & Proses", key=f"d_proses_{l['id']}", type="primary"):
            _update_status("Diproses", {"petugas": nama})
            st.success("Laporan diambil dan mulai diproses.")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if role == "Petugas Operasional" and l["status"] in ["Diproses"]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📝 Update Penanganan</div><br>', unsafe_allow_html=True)
        catatan = st.text_area("Catatan Penanganan", value=l.get("catatan", ""), key=f"d_cat_{l['id']}")
        new_stat = st.selectbox("Update Status", ["Diproses", "Selesai", "Ditolak"], key=f"d_st_{l['id']}")
        if st.button("💾 Simpan Update", type="primary", key=f"d_upd_{l['id']}"):
            _update_status(new_stat, {"catatan": catatan})
            st.success(f"Status laporan diperbarui menjadi {new_stat}.")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

"""detail_warga.py — Halaman detail satu warga (klik dari Kelola Warga / Validasi Warga).
Menampilkan profil lengkap + riwayat kas, bansos, dan laporan milik warga tersebut.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds
from app import render_section_header, render_empty_state


def render():
    id_warga = st.session_state.get("detail_warga_id")
    w = ds.get_warga_by_id(id_warga)

    render_section_header(
        "👤 Detail Warga",
        "Profil lengkap dan riwayat aktivitas warga",
    )

    if st.button("⬅ Kembali ke Daftar Warga"):
        st.session_state["current_page"] = "warga" if st.session_state.get("user", {}).get("role") == "Pengurus RW" else "validasi_warga"
        st.rerun()

    if not w:
        st.warning("Data warga tidak ditemukan. Silakan pilih warga dari daftar.")
        return

    riwayat = ds.get_riwayat_warga(w["id"])

    val_cls  = "badge-green" if w["validasi"] == "Terverifikasi" else "badge-yellow"
    stat_cls = {"Aktif": "badge-green", "Pindah": "badge-gray", "Meninggal": "badge-red"}.get(w["status"], "badge-gray")

    # ── Header profil ───────────────────────────────────────────────────────
    st.markdown(
        f"""<div class="card">
          <div class="detail-header">
            <div class="detail-avatar">👤</div>
            <div>
              <div style="font-weight:700; font-size:1.15rem; color:#1E3A8A;">{w['nama']}</div>
              <div style="font-size:0.8rem; color:#6B7280;">{w['nik']}</div>
              <div style="margin-top:5px;">
                <span class="badge {stat_cls}">{w['status']}</span>
                <span class="badge {val_cls}" style="margin-left:5px;">{w['validasi']}</span>
              </div>
            </div>
          </div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem;">
            <div><div class="detail-label">Nomor KK</div><div class="detail-value">{w['no_kk']}</div></div>
            <div><div class="detail-label">No. HP</div><div class="detail-value">{w['no_hp']}</div></div>
            <div><div class="detail-label">Alamat</div><div class="detail-value">{w['alamat']}</div></div>
          </div>
        </div>""",
        unsafe_allow_html=True,
    )

    # ── Ringkasan cepat ──────────────────────────────────────────────────────
    total_lunas = sum(k["nominal"] for k in riwayat["kas"] if k["status"] == "Lunas")
    bansos_aktif = sum(1 for b in riwayat["bansos"] if b["status"] == "Aktif")
    lap_aktif = sum(1 for l in riwayat["laporan"] if l["status"] not in ["Selesai", "Ditolak"])

    c1, c2, c3 = st.columns(3)
    c1.markdown(f"""<div class="metric-card"><div class="metric-icon" style="background:#A7F3D0;">💰</div>
        <div><div class="metric-label">Kas Terbayar</div><div class="metric-value" style="color:#065F46;">Rp {total_lunas:,}</div></div></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="metric-card"><div class="metric-icon" style="background:#FDE68A;">🎁</div>
        <div><div class="metric-label">Bansos Aktif</div><div class="metric-value" style="color:#92400E;">{bansos_aktif}</div></div></div>""", unsafe_allow_html=True)
    c3.markdown(f"""<div class="metric-card"><div class="metric-icon" style="background:#FECACA;">📋</div>
        <div><div class="metric-label">Laporan Berjalan</div><div class="metric-value" style="color:#991B1B;">{lap_aktif}</div></div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab_kas, tab_bansos, tab_laporan = st.tabs(["💰 Riwayat Kas", "🎁 Riwayat Bansos", "📋 Riwayat Laporan"])

    with tab_kas:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if riwayat["kas"]:
            rows = ""
            for k in riwayat["kas"][::-1]:
                cls = {"Lunas": "badge-green", "Belum Lunas": "badge-red", "Menunggu Verifikasi": "badge-yellow"}.get(k["status"], "badge-gray")
                rows += f"<tr><td>Rp {k['nominal']:,}</td><td>{k['tanggal']}</td><td><span class='badge {cls}'>{k['status']}</span></td></tr>"
            st.markdown(f"""<table class="styled-table"><thead><tr><th>Nominal</th><th>Tanggal</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table>""", unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#9CA3AF; font-size:0.85rem;">Belum ada riwayat kas.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_bansos:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if riwayat["bansos"]:
            rows = ""
            for b in riwayat["bansos"]:
                cls = "badge-green" if b["status"] == "Aktif" else "badge-gray"
                rows += f"<tr><td>{b['jenis']}</td><td><span class='badge {cls}'>{b['status']}</span></td></tr>"
            st.markdown(f"""<table class="styled-table"><thead><tr><th>Jenis Bansos</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table>""", unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#9CA3AF; font-size:0.85rem;">Warga ini belum terdaftar sebagai penerima bansos.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_laporan:
        if riwayat["laporan"]:
            BADGE = {"Menunggu": "badge-gray", "Diverifikasi": "badge-yellow", "Diproses": "badge-blue", "Selesai": "badge-green", "Ditolak": "badge-red"}
            for l in riwayat["laporan"][::-1]:
                badge_cls = BADGE.get(l["status"], "badge-gray")
                st.markdown(
                    f"""<div class="card">
                      <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <div>
                          <span style="font-weight:700; color:#1E3A8A;">{l['judul']}</span>
                          <span class="badge {badge_cls}" style="margin-left:8px;">{l['status']}</span>
                          <div style="font-size:0.78rem; color:#9CA3AF; margin-top:3px;">📅 {l['tanggal']}</div>
                        </div>
                      </div>
                    </div>""",
                    unsafe_allow_html=True,
                )
                if st.button("🔍 Lihat Detail Laporan", key=f"dl_{l['id']}"):
                    st.session_state["detail_laporan_id"] = l["id"]
                    st.session_state["detail_laporan_back"] = "detail_warga"
                    st.session_state["current_page"] = "detail_laporan"
                    st.rerun()
        else:
            st.markdown('<p style="color:#9CA3AF; font-size:0.85rem;">Warga ini belum pernah mengirim laporan.</p>', unsafe_allow_html=True)

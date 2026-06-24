import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds
from app import render_section_header, render_empty_state
from datetime import date


STATUS_FLOW = {
    "Pengurus RW": ("Menunggu", "Diverifikasi"),
    "Pengurus RT": ("Menunggu", "Diverifikasi"),
    "Petugas Operasional": ("Diverifikasi", "Diproses"),
}

BADGE = {
    "Menunggu":    "badge-gray",
    "Diverifikasi":"badge-yellow",
    "Diproses":    "badge-blue",
    "Selesai":     "badge-green",
    "Ditolak":     "badge-red",
}


def render():
    user = st.session_state.get("user", {})
    role = user.get("role", "")

    render_section_header(
        "📋 Kelola Laporan Warga",
        "Verifikasi dan tindaklanjuti laporan pengaduan warga",
    )

    laporan_list = ds.get("laporan")

    # Filter
    col_f, _ = st.columns([2, 4])
    with col_f:
        f_stat = st.selectbox("Filter Status", ["Semua", "Menunggu", "Diverifikasi", "Diproses", "Selesai", "Ditolak"])

    filtered = laporan_list if f_stat == "Semua" else [l for l in laporan_list if l["status"] == f_stat]

    if not filtered:
        render_empty_state("📋", "Tidak ada laporan untuk filter ini", "Coba ubah filter status di atas.")
        return

    st.markdown('<div class="card">', unsafe_allow_html=True)
    for l in filtered[::-1]:
        badge_cls = BADGE.get(l["status"], "badge-gray")
        st.markdown(
            f"""<div style="padding:12px 0; border-bottom:1px solid #F3F4F6;">
              <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div style="flex:1;">
                  <span style="font-weight:700; color:#1E3A8A;">{l['judul']}</span>
                  <span class="badge {badge_cls}" style="margin-left:10px;">{l['status']}</span>
                  {f'<span class="badge badge-blue" style="margin-left:6px;">📎 Ada Lampiran</span>' if l.get('lampiran') else ''}
                  <div style="font-size:0.8rem; color:#6B7280; margin:4px 0 6px;">
                    👤 {l['nama']} &nbsp;·&nbsp; 📅 {l['tanggal']}
                    {f"&nbsp;·&nbsp; 🔧 {l['petugas']}" if l.get('petugas') else ''}
                  </div>
                  <div style="font-size:0.87rem; color:#374151;">{l['deskripsi']}</div>
                  {f"<div style='margin-top:6px; font-size:0.83rem; color:#059669; background:#ECFDF5; padding:4px 8px; border-radius:6px; display:inline-block;'>📝 {l['catatan']}</div>" if l.get('catatan') else ''}
                </div>
              </div>
            </div>""",
            unsafe_allow_html=True,
        )

        # Action buttons
        col_btn1, col_btn2, col_btn3, _ = st.columns([1.4, 1.4, 1.4, 4.8])
        with col_btn1:
            if st.button("🔍 Lihat Detail", key=f"detail_l_{l['id']}"):
                st.session_state["detail_laporan_id"] = l["id"]
                st.session_state["detail_laporan_back"] = "laporan"
                st.session_state["current_page"] = "detail_laporan"
                st.rerun()

        if role in ["Pengurus RW", "Pengurus RT"] and l["status"] == "Menunggu":
            with col_btn2:
                if st.button("✅ Verifikasi", key=f"ver_l_{l['id']}"):
                    current = ds.get("laporan")
                    for item in current:
                        if item["id"] == l["id"]:
                            item["status"] = "Diverifikasi"
                            item.setdefault("riwayat", []).append({"status": "Diverifikasi", "tanggal": str(date.today()), "oleh": user.get("nama", "")})
                    ds.set_data("laporan", current)
                    st.rerun()
            with col_btn3:
                if st.button("❌ Tolak", key=f"tol_l_{l['id']}"):
                    current = ds.get("laporan")
                    for item in current:
                        if item["id"] == l["id"]:
                            item["status"] = "Ditolak"
                            item.setdefault("riwayat", []).append({"status": "Ditolak", "tanggal": str(date.today()), "oleh": user.get("nama", "")})
                    ds.set_data("laporan", current)
                    st.rerun()

        if role == "Petugas Operasional" and l["status"] == "Diverifikasi":
            with col_btn2:
                if st.button("🔧 Ambil & Proses", key=f"proses_{l['id']}"):
                    current = ds.get("laporan")
                    for item in current:
                        if item["id"] == l["id"]:
                            item["status"]   = "Diproses"
                            item["petugas"]  = user.get("nama", "")
                            item.setdefault("riwayat", []).append({"status": "Diproses", "tanggal": str(date.today()), "oleh": user.get("nama", "")})
                    ds.set_data("laporan", current)
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds
from app import render_section_header, render_empty_state, html_block


def render():
    user = st.session_state.get("user", {})
    nama = user.get("nama", "")

    render_section_header(
        "📊 Status Laporan Saya",
        "Pantau perkembangan laporan yang telah Anda kirimkan",
    )

    laporan_list = ds.get("laporan")
    my_laporan   = [l for l in laporan_list if l["nama"] == nama]

    if not my_laporan:
        render_empty_state("📭", "Anda belum memiliki laporan", "Kirim laporan pertama Anda melalui menu Kirim Laporan.")
        return

    BADGE = {"Menunggu":"badge-gray","Diverifikasi":"badge-yellow","Diproses":"badge-blue","Selesai":"badge-green","Ditolak":"badge-red"}
    STEPS = ["Menunggu","Diverifikasi","Diproses","Selesai"]

    for l in my_laporan[::-1]:
        badge_cls = BADGE.get(l["status"], "badge-gray")
        try:
            step_idx = STEPS.index(l["status"])
        except ValueError:
            step_idx = -1

        # Progress bar visual
        progress_html = ""
        for i, s in enumerate(STEPS):
            done   = i <= step_idx and l["status"] != "Ditolak"
            active = i == step_idx and l["status"] != "Ditolak"
            bg     = "#1D4ED8" if done else "#E5E7EB"
            txt    = "white" if done else "#9CA3AF"
            progress_html += f"""
            <div style="display:flex; flex-direction:column; align-items:center; flex:1;">
              <div style="width:28px; height:28px; border-radius:50%; background:{bg};
                          color:{txt}; display:flex; align-items:center; justify-content:center;
                          font-size:0.75rem; font-weight:700; border:2px solid {'#1D4ED8' if done else '#E5E7EB'};">
                {'✓' if done and not active else i+1}
              </div>
              <div style="font-size:0.68rem; color:{'#1E3A8A' if done else '#9CA3AF'}; margin-top:4px; text-align:center;">{s}</div>
            </div>
            {'<div style="height:2px; background:' + ('#1D4ED8' if i < step_idx and l["status"] != "Ditolak" else '#E5E7EB') + '; flex:1; margin-top:14px;"></div>' if i < len(STEPS)-1 else ''}
            """

        html_block(
            f"""<div class="card">
              <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
                <div>
                  <span style="font-weight:700; color:#1E3A8A; font-size:1rem;">{l['judul']}</span>
                  <span class="badge {badge_cls}" style="margin-left:8px;">{l['status']}</span>
                  {f'<span class="badge badge-blue" style="margin-left:6px;">📎 Ada Lampiran</span>' if l.get('lampiran') else ''}
                </div>
                <div style="font-size:0.78rem; color:#9CA3AF;">📅 {l['tanggal']}</div>
              </div>
              <div style="font-size:0.85rem; color:#6B7280; margin-bottom:14px;">{l['deskripsi']}</div>
              <div style="display:flex; align-items:center; margin-bottom:12px;">{progress_html}</div>
              {f"<div style='background:#ECFDF5; border-radius:8px; padding:8px 12px; font-size:0.83rem; color:#065F46;'>📝 Catatan Petugas: {l['catatan']}</div>" if l.get('catatan') else ''}
              {f"<div style='font-size:0.8rem; color:#6B7280; margin-top:6px;'>🔧 Ditangani oleh: {l['petugas']}</div>" if l.get('petugas') else ''}
            </div>"""
        )
        col_d, _ = st.columns([1.6, 5])
        with col_d:
            if st.button("🔍 Lihat Detail & Kronologi", key=f"detail_sl_{l['id']}"):
                st.session_state["detail_laporan_id"] = l["id"]
                st.session_state["detail_laporan_back"] = "status_laporan"
                st.session_state["current_page"] = "detail_laporan"
                st.rerun()

import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds
from app import render_section_header, render_empty_state


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
        progress_html = "<div style='display:flex;align-items:center;width:100%;'>"
        for i, s in enumerate(STEPS):
            done = i <= step_idx and l["status"] != "Ditolak"

            progress_html += f"""
            <div style="text-align:center;">
                <div style="
                    width:28px;
                    height:28px;
                    border-radius:50%;
                    background:{'#1D4ED8' if done else '#E5E7EB'};
                    color:white;
                    line-height:28px;
                    margin:auto;">
                    {'✓' if done else i+1}
                </div>
                <small>{s}</small>
            </div>
            """
            if i < len(STEPS)-1:
                progress_html += """
                <div style="
                    flex:1;
                    height:2px;
                    background:#1D4ED8;
                    margin:0 8px;">
                </div>
                """
progress_html += "</div>"

st.markdown(
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
    </div>""",
    unsafe_allow_html=True,
)
col_d, _ = st.columns([1.6, 5])
with col_d:
    if st.button("🔍 Lihat Detail & Kronologi", key=f"detail_sl_{l['id']}"):
        st.session_state["detail_laporan_id"] = l["id"]
        st.session_state["detail_laporan_back"] = "status_laporan"
        st.session_state["current_page"] = "detail_laporan"
        st.rerun()

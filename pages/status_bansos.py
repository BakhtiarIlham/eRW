import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds
from app import render_section_header, render_empty_state


def render():
    user = st.session_state.get("user", {})
    nama = user.get("nama", "")

    render_section_header(
        "🎁 Status Bantuan Sosial",
        "Informasi bantuan sosial yang Anda terima",
    )

    bansos_list = ds.get("bansos")
    warga_list  = ds.get("warga")
    w = next((x for x in warga_list if x["nama"] == nama), {"id": 1})
    my_bansos = [b for b in bansos_list if b["id_warga"] == w["id"]]

    if not my_bansos:
        render_empty_state(
            "📭",
            "Anda tidak terdaftar sebagai penerima bantuan sosial saat ini",
            "Hubungi pengurus RW untuk informasi lebih lanjut.",
        )
        return

    for b in my_bansos:
        cls = "badge-green" if b["status"] == "Aktif" else "badge-gray"
        icon = {"PKH":"🏠","BPNT":"🛒","BLT":"💵","KIS":"🏥"}.get(b["jenis"],"🎁")
        st.markdown(
            f"""<div class="card" style="border-left:4px solid {'#10B981' if b['status']=='Aktif' else '#9CA3AF'};">
              <div style="display:flex; align-items:center; gap:1rem;">
                <div style="font-size:2.5rem;">{icon}</div>
                <div>
                  <div style="font-weight:700; font-size:1.1rem; color:#1E3A8A;">{b['jenis']}</div>
                  <div style="font-size:0.82rem; color:#6B7280; margin-top:2px;">Program Bantuan Sosial Pemerintah</div>
                  <div style="margin-top:8px;"><span class="badge {cls}">{b['status']}</span></div>
                </div>
              </div>
            </div>""",
            unsafe_allow_html=True,
        )

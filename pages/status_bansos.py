import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds


def render():
    user = st.session_state.get("user", {})
    nama = user.get("nama", "")

    st.markdown('<div class="page-title">🎁 Status Bantuan Sosial</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Informasi bantuan sosial yang Anda terima</div>', unsafe_allow_html=True)

    bansos_list = ds.get("bansos")
    warga_list  = ds.get("warga")
    w = next((x for x in warga_list if x["nama"] == nama), {"id": 1})
    my_bansos = [b for b in bansos_list if b["id_warga"] == w["id"]]

    if not my_bansos:
        st.markdown(
            """<div class="card" style="text-align:center; padding:3rem;">
              <div style="font-size:3rem; margin-bottom:1rem;">📭</div>
              <div style="color:#6B7280; font-size:0.95rem;">Anda tidak terdaftar sebagai penerima bantuan sosial saat ini.</div>
              <div style="color:#9CA3AF; font-size:0.82rem; margin-top:8px;">Hubungi pengurus RW untuk informasi lebih lanjut.</div>
            </div>""",
            unsafe_allow_html=True,
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

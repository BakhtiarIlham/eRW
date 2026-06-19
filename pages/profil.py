"""profil.py — Data Pribadi Warga"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds


def render():
    user = st.session_state.get("user", {})
    nama = user.get("nama", "")

    st.markdown('<div class="page-title">👤 Data Pribadi</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Informasi profil dan data keluarga Anda</div>', unsafe_allow_html=True)

    warga_list = ds.get("warga")
    w = next((x for x in warga_list if x["nama"] == nama), None)

    if not w:
        st.warning("Data profil belum tersedia.")
        return

    val_cls = "badge-green" if w["validasi"] == "Terverifikasi" else "badge-yellow"

    st.markdown(
        f"""<div class="card">
          <div style="display:flex; align-items:center; gap:1.5rem; margin-bottom:1.2rem;">
            <div style="width:64px; height:64px; background:linear-gradient(135deg,#1D4ED8,#3B82F6);
                        border-radius:50%; display:flex; align-items:center; justify-content:center;
                        font-size:1.8rem; color:white;">👤</div>
            <div>
              <div style="font-weight:700; font-size:1.2rem; color:#1E3A8A;">{w['nama']}</div>
              <div style="font-size:0.83rem; color:#6B7280;">{user.get('email','')}</div>
              <div style="margin-top:6px;">
                <span class="badge badge-blue">{user.get('role','')}</span>
                <span class="badge {val_cls}" style="margin-left:6px;">{w['validasi']}</span>
              </div>
            </div>
          </div>
          <hr style="border-color:#F3F4F6; margin:1rem 0;">
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem;">
            <div>
              <div style="font-size:0.78rem; color:#9CA3AF; margin-bottom:2px;">NIK</div>
              <div style="font-weight:500; color:#1F2937;">{w['nik']}</div>
            </div>
            <div>
              <div style="font-size:0.78rem; color:#9CA3AF; margin-bottom:2px;">No. KK</div>
              <div style="font-weight:500; color:#1F2937;">{w['no_kk']}</div>
            </div>
            <div>
              <div style="font-size:0.78rem; color:#9CA3AF; margin-bottom:2px;">Alamat</div>
              <div style="font-weight:500; color:#1F2937;">{w['alamat']}</div>
            </div>
            <div>
              <div style="font-size:0.78rem; color:#9CA3AF; margin-bottom:2px;">No. HP</div>
              <div style="font-weight:500; color:#1F2937;">{w['no_hp']}</div>
            </div>
            <div>
              <div style="font-size:0.78rem; color:#9CA3AF; margin-bottom:2px;">Status Warga</div>
              <div><span class="badge badge-green">{w['status']}</span></div>
            </div>
          </div>
        </div>""",
        unsafe_allow_html=True,
    )

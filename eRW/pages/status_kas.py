import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds


def render():
    user = st.session_state.get("user", {})
    nama = user.get("nama", "")

    st.markdown('<div class="page-title">💳 Status Pembayaran Kas</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Riwayat pembayaran kas warga Anda</div>', unsafe_allow_html=True)

    kas_list  = ds.get("kas")
    warga_list = ds.get("warga")
    w = next((x for x in warga_list if x["nama"] == nama), {"id": 1})
    my_kas = [k for k in kas_list if k["id_warga"] == w["id"]]

    total_lunas = sum(k["nominal"] for k in my_kas if k["status"] == "Lunas")
    total_belum = sum(k["nominal"] for k in my_kas if k["status"] == "Belum Lunas")

    c1, c2 = st.columns(2)
    c1.markdown(f"""<div class="metric-card"><div class="metric-icon" style="background:#A7F3D0;">✅</div>
        <div><div class="metric-label">Total Terbayar</div><div class="metric-value" style="color:#065F46;">Rp {total_lunas:,}</div></div></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="metric-card"><div class="metric-icon" style="background:#FECACA;">⚠️</div>
        <div><div class="metric-label">Belum Lunas</div><div class="metric-value" style="color:#991B1B;">Rp {total_belum:,}</div></div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 Riwayat Pembayaran</div><br>', unsafe_allow_html=True)

    if my_kas:
        rows = ""
        for k in my_kas[::-1]:
            cls = {"Lunas":"badge-green","Belum Lunas":"badge-red","Menunggu Verifikasi":"badge-yellow"}.get(k["status"],"badge-gray")
            rows += f"<tr><td>Rp {k['nominal']:,}</td><td>{k['tanggal']}</td><td><span class='badge {cls}'>{k['status']}</span></td></tr>"
        st.markdown(
            f"""<table class="styled-table"><thead><tr><th>Nominal</th><th>Tanggal</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table>""",
            unsafe_allow_html=True,
        )
    else:
        st.info("Belum ada riwayat pembayaran kas.")
    st.markdown('</div>', unsafe_allow_html=True)

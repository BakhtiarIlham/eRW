import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds


def render():
    st.markdown('<div class="page-title">✅ Validasi Data Warga</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Verifikasi data warga baru atau perubahan data di wilayah RT</div>', unsafe_allow_html=True)

    warga_list = ds.get("warga")
    pending    = [w for w in warga_list if w["validasi"] == "Menunggu"]
    verified   = [w for w in warga_list if w["validasi"] == "Terverifikasi"]

    # Summary
    c1, c2 = st.columns(2)
    c1.markdown(f"""<div class="metric-card"><div class="metric-icon" style="background:#FDE68A;">⏳</div>
        <div><div class="metric-label">Menunggu Validasi</div><div class="metric-value" style="color:#92400E;">{len(pending)}</div></div></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="metric-card"><div class="metric-icon" style="background:#A7F3D0;">✅</div>
        <div><div class="metric-label">Terverifikasi</div><div class="metric-value" style="color:#065F46;">{len(verified)}</div></div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if pending:
        st.markdown("#### ⏳ Perlu Divalidasi")
        for w in pending:
            st.markdown(
                f"""<div class="card" style="border-left:4px solid #F59E0B;">
                  <div style="font-weight:700; color:#1E3A8A;">{w['nama']}</div>
                  <div style="font-size:0.82rem; color:#6B7280; margin:4px 0;">
                    🪪 NIK: {w['nik']} &nbsp;·&nbsp; 🏠 {w['alamat']} &nbsp;·&nbsp; 📱 {w['no_hp']}
                  </div>
                  <span class="badge badge-yellow">Menunggu Validasi</span>
                </div>""",
                unsafe_allow_html=True,
            )
            col_a, col_r, _ = st.columns([1.5, 1.5, 5])
            with col_a:
                if st.button("✅ Setujui", key=f"app_{w['id']}", type="primary"):
                    current = ds.get("warga")
                    for item in current:
                        if item["id"] == w["id"]:
                            item["validasi"] = "Terverifikasi"
                    ds.set_data("warga", current)
                    st.success(f"Data {w['nama']} disetujui!")
                    st.rerun()
            with col_r:
                if st.button("❌ Tolak", key=f"rej_{w['id']}"):
                    current = ds.get("warga")
                    ds.set_data("warga", [x for x in current if x["id"] != w["id"]])
                    st.warning(f"Data {w['nama']} ditolak dan dihapus.")
                    st.rerun()
    else:
        st.success("🎉 Semua data warga sudah terverifikasi!")

    st.markdown("<br>")
    st.markdown("#### ✅ Warga Terverifikasi")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    rows = "".join(
        f"<tr><td>{w['nik']}</td><td>{w['nama']}</td><td>{w['alamat']}</td><td><span class='badge badge-green'>Terverifikasi</span></td></tr>"
        for w in verified
    )
    st.markdown(
        f"""<table class="styled-table"><thead><tr><th>NIK</th><th>Nama</th><th>Alamat</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table>""",
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

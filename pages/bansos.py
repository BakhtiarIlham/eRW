import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds


def render():
    st.markdown('<div class="page-title">🎁 Kelola Bantuan Sosial (Bansos)</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Kelola data penerima bantuan sosial warga</div>', unsafe_allow_html=True)

    bansos_list = ds.get("bansos")
    role = st.session_state.get("user", {}).get("role", "")

    aktif = sum(1 for b in bansos_list if b["status"] == "Aktif")
    nonaktif = len(bansos_list) - aktif

    c1, c2 = st.columns(2)
    c1.markdown(f"""<div class="metric-card"><div class="metric-icon" style="background:#A7F3D0;">✅</div>
        <div><div class="metric-label">Penerima Aktif</div><div class="metric-value" style="color:#065F46;">{aktif}</div></div></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="metric-card"><div class="metric-icon" style="background:#E5E7EB;">⭕</div>
        <div><div class="metric-label">Nonaktif</div><div class="metric-value" style="color:#374151;">{nonaktif}</div></div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Add bansos
    if role == "Pengurus RW":
        with st.expander("➕ Tambah Penerima Bansos"):
            warga_list = ds.get("warga")
            nama_opt   = {w["nama"]: w["id"] for w in warga_list if w["status"] == "Aktif"}
            cc1, cc2, cc3 = st.columns(3)
            with cc1: pilih = st.selectbox("Warga", list(nama_opt.keys()))
            with cc2: jenis = st.selectbox("Jenis Bansos", ["PKH", "BPNT", "BLT", "KIS", "Lainnya"])
            with cc3: stat  = st.selectbox("Status", ["Aktif", "Nonaktif"])
            if st.button("💾 Simpan", type="primary"):
                current = ds.get("bansos")
                new_id  = max((b["id"] for b in current), default=0) + 1
                current.append({"id": new_id, "id_warga": nama_opt[pilih], "nama": pilih, "jenis": jenis, "status": stat})
                ds.set_data("bansos", current)
                st.success("✅ Data bansos ditambahkan!")
                st.rerun()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    rows = ""
    for b in bansos_list:
        cls = "badge-green" if b["status"] == "Aktif" else "badge-gray"
        rows += f"<tr><td>{b['nama']}</td><td>{b['jenis']}</td><td><span class='badge {cls}'>{b['status']}</span></td></tr>"
    st.markdown(
        f"""<table class="styled-table"><thead><tr><th>Nama Warga</th><th>Jenis Bansos</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table>""",
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

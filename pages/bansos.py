import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds
from app import render_section_header, render_empty_state, confirm_delete_button, html_block


def render():
    render_section_header(
        "🎁 Kelola Bantuan Sosial (Bansos)",
        "Kelola data penerima bantuan sosial warga",
    )

    bansos_list = ds.get("bansos")
    role = st.session_state.get("user", {}).get("role", "")

    aktif = sum(1 for b in bansos_list if b["status"] == "Aktif")
    nonaktif = len(bansos_list) - aktif

    c1, c2 = st.columns(2)
    with c1:
        html_block(f"""<div class="metric-card"><div class="metric-icon" style="background:#A7F3D0;">✅</div>
        <div><div class="metric-label">Penerima Aktif</div><div class="metric-value" style="color:#065F46;">{aktif}</div></div></div>""")
    with c2:
        html_block(f"""<div class="metric-card"><div class="metric-icon" style="background:#E5E7EB;">⭕</div>
        <div><div class="metric-label">Nonaktif</div><div class="metric-value" style="color:#374151;">{nonaktif}</div></div></div>""")

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

    if not bansos_list:
        render_empty_state("🎁", "Belum ada data penerima bansos", "Tambahkan penerima bansos baru melalui form di atas.")
        return

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Daftar Penerima Bansos</div><br>', unsafe_allow_html=True)

    header = st.columns([3, 2, 2, 1])
    header[0].markdown("**Nama**")
    header[1].markdown("**Jenis Bansos**")
    header[2].markdown("**Status**")
    header[3].markdown("**Hapus**")
    st.divider()

    for b in bansos_list:
        cls = "badge-green" if b["status"] == "Aktif" else "badge-gray"
        cols = st.columns([3, 2, 2, 1])
        cols[0].write(b["nama"])
        cols[1].write(b["jenis"])
        cols[2].markdown(f'<span class="badge {cls}">{b["status"]}</span>', unsafe_allow_html=True)
        if role == "Pengurus RW":
            with cols[3]:
                if confirm_delete_button(
                    f"bansos_{b['id']}",
                    confirm_text=f"Hapus data bansos {b['nama']} ({b['jenis']})?",
                ):
                    current = ds.get("bansos")
                    ds.set_data("bansos", [x for x in current if x["id"] != b["id"]])
                    st.success("Data bansos dihapus.")
                    st.rerun()
        st.divider()
    st.markdown('</div>', unsafe_allow_html=True)

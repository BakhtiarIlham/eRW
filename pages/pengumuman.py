import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds
from app import render_section_header, render_empty_state, confirm_delete_button, html_block
from datetime import date


def render():
    user = st.session_state.get("user", {})
    role = user.get("role", "")
    nama = user.get("nama", "")

    render_section_header(
        "📢 Pengumuman",
        "Informasi dan pengumuman lingkungan RW",
    )

    pengumuman = ds.get("pengumuman")

    # Tambah (hanya RW & RT)
    if role in ["Pengurus RW", "Pengurus RT"]:
        with st.expander("➕ Buat Pengumuman Baru"):
            judul = st.text_input("Judul Pengumuman")
            isi   = st.text_area("Isi Pengumuman", height=120)
            if st.button("📤 Publikasikan", type="primary"):
                if judul and isi:
                    current = ds.get("pengumuman")
                    new_id  = max((p["id"] for p in current), default=0) + 1
                    current.insert(0, {"id": new_id, "judul": judul, "isi": isi, "tanggal": str(date.today()), "oleh": nama})
                    ds.set_data("pengumuman", current)
                    st.success("✅ Pengumuman dipublikasikan!")
                    st.rerun()
                else:
                    st.warning("Judul dan isi wajib diisi.")

    st.markdown("<br>", unsafe_allow_html=True)

    if not pengumuman:
        render_empty_state("📢", "Belum ada pengumuman", "Pengumuman baru akan muncul di sini setelah dipublikasikan.")
        return

    for p in pengumuman:
        with st.container():
            html_block(
                f"""<div class="card" style="border-left:4px solid #3B82F6;">
                  <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                      <div style="font-weight:700; font-size:1rem; color:#1E3A8A;">{p['judul']}</div>
                      <div style="font-size:0.78rem; color:#9CA3AF; margin:4px 0 10px;">
                        📅 {p['tanggal']} &nbsp;·&nbsp; 👤 {p['oleh']}
                      </div>
                      <div style="color:#374151; font-size:0.88rem; line-height:1.6;">{p['isi']}</div>
                    </div>
                  </div>
                </div>"""
            )
            if role in ["Pengurus RW", "Pengurus RT"]:
                col_d, col_sp = st.columns([1, 6])
                with col_d:
                    if confirm_delete_button(
                        f"pengumuman_{p['id']}",
                        trigger_label="🗑️ Hapus",
                        confirm_text=f"Hapus pengumuman \"{p['judul']}\"?",
                    ):
                        current = ds.get("pengumuman")
                        ds.set_data("pengumuman", [x for x in current if x["id"] != p["id"]])
                        st.success("Pengumuman dihapus.")
                        st.rerun()

import streamlit as st
import sys, os
import textwrap

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds
from app import render_section_header, render_empty_state, confirm_delete_button
from datetime import date, timedelta


def render():
    user = st.session_state.get("user", {})
    role = user.get("role", "")
    nama = user.get("nama", "")

    render_section_header(
        "📅 Kegiatan Lingkungan",
        "Jadwal dan pendaftaran kegiatan warga",
    )

    kegiatan_list = ds.get("kegiatan")
    today = date.today()

    # Tambah kegiatan
    if role in ["Pengurus RW", "Pengurus RT"]:
        with st.expander("➕ Buat Kegiatan Baru"):
            c1, c2 = st.columns(2)
            with c1:
                k_nama = st.text_input("Nama Kegiatan")
                k_lokasi = st.text_input("Lokasi")
            with c2:
                k_tgl = st.date_input("Tanggal Kegiatan", value=today + timedelta(days=7))
            if st.button("💾 Simpan Kegiatan", type="primary"):
                if k_nama and k_lokasi:
                    current = ds.get("kegiatan")
                    new_id  = max((k["id"] for k in current), default=0) + 1
                    current.append({"id": new_id, "nama": k_nama, "tanggal": str(k_tgl), "lokasi": k_lokasi, "oleh": nama, "peserta": []})
                    ds.set_data("kegiatan", current)
                    st.success("✅ Kegiatan dibuat!")
                    st.rerun()
                else:
                    st.warning("Nama kegiatan dan lokasi wajib diisi.")

    st.markdown("<br>", unsafe_allow_html=True)

    if not kegiatan_list:
        render_empty_state("📅", "Belum ada kegiatan terjadwal", "Buat kegiatan baru melalui form di atas.")
        return

    # ── Kegiatan cards ────────────────────────────────────────────────────────
    upcoming = sorted(kegiatan_list, key=lambda x: x["tanggal"])
    for k in upcoming:
        tgl = date.fromisoformat(k["tanggal"])
        is_past  = tgl < today
        sudah_daftar = nama in k.get("peserta", [])
        jml_peserta  = len(k.get("peserta", []))

        border_col = "#9CA3AF" if is_past else "#3B82F6"
        badge_html = f"""<span class="badge {'badge-gray' if is_past else 'badge-blue'}">{'Selesai' if is_past else 'Mendatang'}</span>"""
        status_html = []
        status_html.append(badge_html)
        status_html.append(f"<span class=\"badge badge-blue\" style=\"margin-left:6px;\">👥 {jml_peserta} peserta</span>")
        if sudah_daftar:
            status_html.append('<span class="badge badge-green" style="margin-left:6px;">✅ Sudah Daftar</span>')

        html_lines = [
            f'<div class="card" style="border-left:4px solid {border_col};">',
            '<div style="display:flex; justify-content:space-between; align-items:center;">',
            '<div>',
            f'<div style="font-weight:700; font-size:1rem; color:#1E3A8A;">{k["nama"]}</div>',
            f'<div style="font-size:0.8rem; color:#6B7280; margin-top:4px;">',
            f'📅 {k["tanggal"]} &nbsp;·&nbsp; 📍 {k["lokasi"]} &nbsp;·&nbsp; 👤 {k["oleh"]}',
            '</div>',
            '<div style="margin-top:8px;">',
        ]
        html_lines.extend(status_html)
        html_lines.extend([
            '</div>',
            '</div>',
            '</div>',
            '</div>',
        ])

        card_html = ''.join(html_lines)
        st.markdown(card_html, unsafe_allow_html=True)

        col_d, col_del, col_sp = st.columns([2, 1, 5])
        with col_d:
            if not is_past and not sudah_daftar and role == "Warga":
                if st.button(f"✋ Daftar Ikut", key=f"join_{k['id']}"):
                    current = ds.get("kegiatan")
                    for item in current:
                        if item["id"] == k["id"]:
                            item["peserta"].append(nama)
                    ds.set_data("kegiatan", current)
                    st.success(f"Berhasil mendaftar kegiatan {k['nama']}!")
                    st.rerun()
        with col_del:
            if role in ["Pengurus RW", "Pengurus RT"]:
                if confirm_delete_button(
                    f"kegiatan_{k['id']}",
                    confirm_text=f"Hapus kegiatan \"{k['nama']}\"?",
                ):
                    current = ds.get("kegiatan")
                    ds.set_data("kegiatan", [x for x in current if x["id"] != k["id"]])
                    st.success("Kegiatan dihapus.")
                    st.rerun()

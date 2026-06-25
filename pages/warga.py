import streamlit as st
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds
from app import render_section_header, render_empty_state, confirm_delete_button


def render():
    render_section_header(
        "👥 Kelola Data Warga",
        "Tambah, ubah, hapus dan cari data warga RW",
    )

    warga_list = ds.get("warga")

    # =========================
    # SEARCH + TAMBAH
    # =========================
    col_s, col_b = st.columns([4, 1])

    with col_s:
        search = st.text_input(
            "Cari Warga",
            placeholder="🔍 Ketik nama atau NIK warga...",
            label_visibility="collapsed"
        )

    with col_b:
        add = st.button(
            "➕ Tambah Warga",
            use_container_width=True,
            type="primary"
        )

    if search:
        warga_list = [
            w for w in warga_list
            if search.lower() in w["nama"].lower()
            or search in w["nik"]
        ]

    # =========================
    # FORM TAMBAH
    # =========================
    if add or st.session_state.get("show_add_warga", False):

        st.session_state["show_add_warga"] = True

        with st.expander("📝 Form Tambah Warga Baru", expanded=True):

            c1, c2 = st.columns(2)

            with c1:
                new_nik = st.text_input("NIK *", max_chars=16)
                new_nama = st.text_input("Nama Lengkap *")
                new_alamat = st.text_input("Alamat")

            with c2:
                new_kk = st.text_input("Nomor KK *", max_chars=16)
                new_hp = st.text_input("No. HP")
                new_stat = st.selectbox(
                    "Status",
                    ["Aktif", "Pindah", "Meninggal"]
                )

            b1, b2 = st.columns(2)

            with b1:
                if st.button(
                    "💾 Simpan",
                    type="primary",
                    use_container_width=True
                ):
                    if new_nik and new_nama and new_kk:

                        current = ds.get("warga")

                        new_id = (
                            max(
                                (w["id"] for w in current),
                                default=0
                            ) + 1
                        )

                        current.append({
                            "id": new_id,
                            "nik": new_nik,
                            "nama": new_nama,
                            "no_kk": new_kk,
                            "alamat": new_alamat,
                            "no_hp": new_hp,
                            "status": new_stat,
                            "validasi": "Menunggu"
                        })

                        ds.set_data("warga", current)

                        st.success("✅ Data warga berhasil ditambahkan")

                        st.session_state["show_add_warga"] = False
                        st.rerun()

                    else:
                        st.error(
                            "NIK, Nama dan Nomor KK wajib diisi."
                        )

            with b2:
                if st.button(
                    "✖ Batal",
                    use_container_width=True
                ):
                    st.session_state["show_add_warga"] = False
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    edit_id = st.session_state.get("edit_warga_id")

    # =========================
    # CARD DAFTAR WARGA
    # =========================
    if not warga_list:
        render_empty_state(
            "🔍" if search else "👥",
            "Tidak ada warga yang cocok dengan pencarian" if search else "Belum ada data warga",
            "Coba kata kunci lain." if search else "Klik \"Tambah Warga\" untuk menambahkan data pertama.",
        )
        return

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="section-header"><div class="section-title">Daftar Warga ({len(warga_list)} orang)</div></div>',
        unsafe_allow_html=True
    )

    # HEADER
    header = st.columns([3, 3, 2, 2, 2, 1, 1, 1])

    header[0].markdown("**Nama**")
    header[1].markdown("**Alamat**")
    header[2].markdown("**No HP**")
    header[3].markdown("**Status**")
    header[4].markdown("**Validasi**")
    header[5].markdown("**Detail**")
    header[6].markdown("**Edit**")
    header[7].markdown("**Hapus**")

    st.divider()

    for w in warga_list:

        val_cls = {
            "Terverifikasi": "badge-green",
            "Menunggu": "badge-yellow"
        }.get(w["validasi"], "badge-gray")

        stat_cls = {
            "Aktif": "badge-green",
            "Pindah": "badge-gray",
            "Meninggal": "badge-red"
        }.get(w["status"], "badge-gray")

        cols = st.columns([3, 3, 2, 2, 2, 1, 1, 1])

        cols[0].markdown(
            f"<b>{w['nama']}</b><br><small>{w['nik']}</small>",
            unsafe_allow_html=True
        )

        cols[1].write(w["alamat"])
        cols[2].write(w["no_hp"])

        cols[3].markdown(
            f'<span class="badge {stat_cls}">{w["status"]}</span>',
            unsafe_allow_html=True
        )

        cols[4].markdown(
            f'<span class="badge {val_cls}">{w["validasi"]}</span>',
            unsafe_allow_html=True
        )

        if cols[5].button(
            "🔍",
            key=f"view_{w['id']}"
        ):
            st.session_state["detail_warga_id"] = w["id"]
            st.session_state["current_page"] = "detail_warga"
            st.rerun()

        if cols[6].button(
            "✏️",
            key=f"edit_{w['id']}"
        ):
            st.session_state["edit_warga_id"] = w["id"]
            st.rerun()

        with cols[7]:
            if confirm_delete_button(
                f"warga_{w['id']}",
                confirm_text=f"Yakin ingin menghapus data {w['nama']}?",
            ):
                current = ds.get("warga")
                current = [x for x in current if x["id"] != w["id"]]
                ds.set_data("warga", current)
                st.success(f"Data {w['nama']} berhasil dihapus.")
                st.rerun()

        # =====================
        # EDIT FORM
        # =====================
        if edit_id == w["id"]:

            with st.expander(
                f"✏️ Edit Data - {w['nama']}",
                expanded=True
            ):

                e1, e2 = st.columns(2)

                with e1:
                    e_nama = st.text_input(
                        "Nama Lengkap",
                        value=w["nama"],
                        key=f"nama_{w['id']}"
                    )

                    e_alamat = st.text_input(
                        "Alamat",
                        value=w["alamat"],
                        key=f"alamat_{w['id']}"
                    )

                with e2:
                    e_hp = st.text_input(
                        "No HP",
                        value=w["no_hp"],
                        key=f"hp_{w['id']}"
                    )

                    e_stat = st.selectbox(
                        "Status",
                        ["Aktif", "Pindah", "Meninggal"],
                        index=[
                            "Aktif",
                            "Pindah",
                            "Meninggal"
                        ].index(w["status"]),
                        key=f"status_{w['id']}"
                    )

                b1, b2 = st.columns(2)

                with b1:
                    if st.button(
                        "💾 Update",
                        key=f"update_{w['id']}",
                        type="primary",
                        use_container_width=True
                    ):

                        current = ds.get("warga")

                        for item in current:
                            if item["id"] == w["id"]:
                                item["nama"] = e_nama
                                item["alamat"] = e_alamat
                                item["no_hp"] = e_hp
                                item["status"] = e_stat

                        ds.set_data("warga", current)

                        st.success(
                            "✅ Data berhasil diperbarui"
                        )

                        st.session_state[
                            "edit_warga_id"
                        ] = None

                        st.rerun()

                with b2:
                    if st.button(
                        "✖ Batal",
                        key=f"cancel_{w['id']}",
                        use_container_width=True
                    ):
                        st.session_state[
                            "edit_warga_id"
                        ] = None
                        st.rerun()

        st.divider()

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

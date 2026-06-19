import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds


def render():
    st.markdown('<div class="page-title">👥 Kelola Data Warga</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Tambah, ubah, hapus dan cari data warga RW</div>', unsafe_allow_html=True)

    warga_list = ds.get("warga")

    # ── Search + Add ─────────────────────────────────────────────────────────
    col_s, col_b = st.columns([4, 1])
    with col_s:
        search = st.text_input("🔍 Cari nama / NIK", placeholder="Ketik nama atau NIK warga…", label_visibility="collapsed")
    with col_b:
        add = st.button("➕ Tambah Warga", use_container_width=True, type="primary")

    if search:
        warga_list = [w for w in warga_list if search.lower() in w["nama"].lower() or search in w["nik"]]

    # ── Add modal (expander) ─────────────────────────────────────────────────
    if add or st.session_state.get("show_add_warga"):
        st.session_state["show_add_warga"] = True
        with st.expander("📝 Form Tambah Warga Baru", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                new_nik    = st.text_input("NIK *", max_chars=16)
                new_nama   = st.text_input("Nama Lengkap *")
                new_alamat = st.text_input("Alamat")
            with c2:
                new_kk   = st.text_input("Nomor KK *", max_chars=16)
                new_hp   = st.text_input("No. HP")
                new_stat = st.selectbox("Status", ["Aktif", "Pindah", "Meninggal"])
            bc1, bc2 = st.columns(2)
            with bc1:
                if st.button("💾 Simpan", type="primary", use_container_width=True):
                    if new_nik and new_nama and new_kk:
                        current = ds.get("warga")
                        new_id = max((w["id"] for w in current), default=0) + 1
                        current.append({
                            "id": new_id, "nik": new_nik, "nama": new_nama,
                            "no_kk": new_kk, "alamat": new_alamat, "no_hp": new_hp,
                            "status": new_stat, "validasi": "Menunggu",
                        })
                        ds.set_data("warga", current)
                        st.session_state["show_add_warga"] = False
                        st.success("✅ Data warga berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.error("NIK, Nama, dan No. KK wajib diisi.")
            with bc2:
                if st.button("✖ Batal", use_container_width=True):
                    st.session_state["show_add_warga"] = False
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Edit state ────────────────────────────────────────────────────────────
    edit_id = st.session_state.get("edit_warga_id")

    # ── Table ────────────────────────────────────────────────────────────────
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">Daftar Warga ({len(warga_list)} orang)</div><br>', unsafe_allow_html=True)

    for w in warga_list:
        val_cls  = {"Terverifikasi": "badge-green", "Menunggu": "badge-yellow"}.get(w["validasi"], "badge-gray")
        stat_cls = {"Aktif": "badge-green", "Pindah": "badge-gray", "Meninggal": "badge-red"}.get(w["status"], "badge-gray")

        with st.container():
            cc = st.columns([3, 3, 2, 2, 2, 1, 1])
            cc[0].markdown(f"**{w['nama']}**<br><small style='color:#6B7280;'>{w['nik']}</small>", unsafe_allow_html=True)
            cc[1].markdown(f"<small>{w['alamat']}</small>", unsafe_allow_html=True)
            cc[2].markdown(f"<small>{w['no_hp']}</small>", unsafe_allow_html=True)
            cc[3].markdown(f"<span class='badge {stat_cls}'>{w['status']}</span>", unsafe_allow_html=True)
            cc[4].markdown(f"<span class='badge {val_cls}'>{w['validasi']}</span>", unsafe_allow_html=True)
            if cc[5].button("✏️", key=f"edit_{w['id']}", help="Edit"):
                st.session_state["edit_warga_id"] = w["id"]
                st.rerun()
            if cc[6].button("🗑️", key=f"del_{w['id']}", help="Hapus"):
                current = ds.get("warga")
                ds.set_data("warga", [x for x in current if x["id"] != w["id"]])
                st.success(f"Data {w['nama']} dihapus.")
                st.rerun()

        # Inline edit
        if edit_id == w["id"]:
            with st.expander(f"✏️ Edit Data: {w['nama']}", expanded=True):
                ec1, ec2 = st.columns(2)
                with ec1:
                    e_nama   = st.text_input("Nama Lengkap", value=w["nama"],   key=f"en_{w['id']}")
                    e_alamat = st.text_input("Alamat",       value=w["alamat"], key=f"ea_{w['id']}")
                with ec2:
                    e_hp   = st.text_input("No. HP",  value=w["no_hp"], key=f"eh_{w['id']}")
                    e_stat = st.selectbox("Status", ["Aktif","Pindah","Meninggal"],
                                          index=["Aktif","Pindah","Meninggal"].index(w["status"]),
                                          key=f"es_{w['id']}")
                eb1, eb2 = st.columns(2)
                with eb1:
                    if st.button("💾 Update", type="primary", use_container_width=True, key=f"upd_{w['id']}"):
                        current = ds.get("warga")
                        for item in current:
                            if item["id"] == w["id"]:
                                item.update({"nama": e_nama, "alamat": e_alamat, "no_hp": e_hp, "status": e_stat})
                        ds.set_data("warga", current)
                        st.session_state["edit_warga_id"] = None
                        st.success("✅ Data diperbarui!")
                        st.rerun()
                with eb2:
                    if st.button("✖ Batal", use_container_width=True, key=f"can_{w['id']}"):
                        st.session_state["edit_warga_id"] = None
                        st.rerun()
        st.markdown("<hr style='margin:6px 0; border-color:#F3F4F6;'>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

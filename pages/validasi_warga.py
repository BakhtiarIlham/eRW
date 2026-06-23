import streamlit as st
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds


def render():

    st.markdown(
        '<div class="page-title">✅ Validasi Data Warga</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Verifikasi data warga baru atau perubahan data di wilayah RT</div>',
        unsafe_allow_html=True
    )

    warga_list = ds.get("warga")

    pending = [
        w for w in warga_list
        if w["validasi"] == "Menunggu"
    ]

    verified = [
        w for w in warga_list
        if w["validasi"] == "Terverifikasi"
    ]

    # ==================================================
    # SUMMARY CARD
    # ==================================================

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon" style="background:#FDE68A;">
                    ⏳
                </div>

                <div>
                    <div class="metric-label">
                        Menunggu Validasi
                    </div>

                    <div class="metric-value" style="color:#92400E;">
                        {len(pending)}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon" style="background:#A7F3D0;">
                    ✅
                </div>

                <div>
                    <div class="metric-label">
                        Terverifikasi
                    </div>

                    <div class="metric-value" style="color:#065F46;">
                        {len(verified)}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================================================
    # DATA MENUNGGU VALIDASI
    # ==================================================

    st.markdown("### ⏳ Data Menunggu Validasi")

    if pending:

        for w in pending:

            st.markdown(
                f"""
                <div class="card" style="border-left:5px solid #F59E0B;">
                    <div style="font-weight:700;font-size:1rem;color:#1E3A8A;">
                        {w['nama']}
                    </div>

                    <div style="font-size:0.85rem;color:#6B7280;margin-top:6px;">
                        🪪 NIK : {w['nik']}
                    </div>

                    <div style="font-size:0.85rem;color:#6B7280;">
                        🏠 Alamat : {w['alamat']}
                    </div>

                    <div style="font-size:0.85rem;color:#6B7280;">
                        📱 No HP : {w['no_hp']}
                    </div>

                    <div style="margin-top:10px;">
                        <span class="badge badge-yellow">
                            Menunggu Validasi
                        </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            a, b, c, d = st.columns([1, 1, 1, 4])

            with a:
                if st.button(
                    "✅ Setujui",
                    key=f"approve_{w['id']}",
                    type="primary",
                    use_container_width=True
                ):

                    current = ds.get("warga")

                    for item in current:
                        if item["id"] == w["id"]:
                            item["validasi"] = "Terverifikasi"

                    ds.set_data("warga", current)

                    st.success(
                        f"{w['nama']} berhasil diverifikasi."
                    )

                    st.rerun()

            with b:
                if st.button(
                    "❌ Tolak",
                    key=f"reject_{w['id']}",
                    use_container_width=True
                ):

                    current = ds.get("warga")

                    current = [
                        x for x in current
                        if x["id"] != w["id"]
                    ]

                    ds.set_data("warga", current)

                    st.warning(
                        f"{w['nama']} ditolak dan dihapus."
                    )

                    st.rerun()

            with c:
                if st.button(
                    "🔍 Detail",
                    key=f"detail_pending_{w['id']}",
                    use_container_width=True
                ):

                    st.session_state["detail_warga_id"] = w["id"]
                    st.session_state["current_page"] = "detail_warga"

                    st.rerun()

            st.divider()

    else:

        st.success(
            "🎉 Tidak ada data yang menunggu validasi."
        )

    # ==================================================
    # DATA TERVERIFIKASI
    # ==================================================

    st.markdown("### ✅ Data Terverifikasi")

    if verified:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        header = st.columns([3, 3, 2, 1])

        header[0].markdown("**Nama**")
        header[1].markdown("**Alamat**")
        header[2].markdown("**Status**")
        header[3].markdown("**Detail**")

        st.divider()

        for w in verified:

            row = st.columns([3, 3, 2, 1])

            row[0].markdown(
                f"""
                <b>{w['nama']}</b><br>
                <small>{w['nik']}</small>
                """,
                unsafe_allow_html=True
            )

            row[1].write(w["alamat"])

            row[2].markdown(
                """
                <span class="badge badge-green">
                    Terverifikasi
                </span>
                """,
                unsafe_allow_html=True
            )

            if row[3].button(
                "🔍",
                key=f"view_verified_{w['id']}"
            ):
                st.session_state["detail_warga_id"] = w["id"]
                st.session_state["current_page"] = "detail_warga"
                st.rerun()

            st.divider()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    else:

        st.info(
            "Belum ada warga yang terverifikasi."
        )

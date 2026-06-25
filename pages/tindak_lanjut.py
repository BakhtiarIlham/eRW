
import streamlit as st
import sys, os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds
from app import render_section_header, render_empty_state, html_block


def render():

    user = st.session_state.get("user", {})
    nama = user.get("nama", "")

    render_section_header(
        "🔧 Tindak Lanjut Laporan",
        "Update progres penanganan laporan warga",
    )

    laporan_list = ds.get("laporan")

    my_laporan = [
        l for l in laporan_list
        if l.get("petugas") == nama
        or l["status"] == "Diverifikasi"
    ]

    if not my_laporan:
        render_empty_state("🔧", "Tidak ada laporan yang perlu ditindaklanjuti", "Laporan baru akan muncul di sini setelah diverifikasi oleh Pengurus RT/RW.")
        return

    for l in my_laporan:

        badge_cls = {
            "Diverifikasi": "badge-yellow",
            "Diproses": "badge-blue",
            "Selesai": "badge-green",
            "Ditolak": "badge-red"
        }.get(l["status"], "badge-gray")

        html_block(
            f"""
            <div class="card">

                <div style="display:flex;justify-content:space-between;align-items:center;">

                    <div style="font-weight:700;font-size:1rem;color:#1E3A8A;">
                        {l['judul']}
                    </div>

                    <span class="badge {badge_cls}">
                        {l['status']}
                    </span>

                </div>

                <div style="font-size:0.82rem;color:#6B7280;margin-top:6px;">
                    👤 {l['nama']}
                    &nbsp;&nbsp;|&nbsp;&nbsp;
                    📅 {l['tanggal']}
                </div>

                <div style="font-size:0.88rem;color:#374151;margin-top:10px;">
                    {l['deskripsi']}
                </div>

            </div>
            """
        )

        b1, b2 = st.columns([1, 3])

        with b1:
            if st.button(
                "🔍 Detail",
                key=f"detail_{l['id']}",
                use_container_width=True
            ):
                st.session_state["detail_laporan_id"] = l["id"]
                st.session_state["detail_laporan_back"] = "tindak_lanjut"
                st.session_state["current_page"] = "detail_laporan"
                st.rerun()

        with b2:

            if l["status"] in ["Diverifikasi", "Diproses"]:

                with st.expander(
                    "📝 Update Status & Catatan"
                ):

                    catatan = st.text_area(
                        "Catatan Penanganan",
                        value=l.get("catatan", ""),
                        key=f"catatan_{l['id']}"
                    )

                    status_opsi = [
                        "Diproses",
                        "Selesai",
                        "Ditolak"
                    ]

                    new_status = st.selectbox(
                        "Update Status",
                        status_opsi,
                        key=f"status_{l['id']}"
                    )

                    if st.button(
                        "💾 Simpan Perubahan",
                        type="primary",
                        key=f"save_{l['id']}"
                    ):

                        current = ds.get("laporan")

                        for item in current:

                            if item["id"] == l["id"]:

                                item["status"] = new_status
                                item["catatan"] = catatan
                                item["petugas"] = nama

                                if (
                                    not item.get("riwayat")
                                    or item["riwayat"][-1]["status"] != new_status
                                ):
                                    item.setdefault(
                                        "riwayat",
                                        []
                                    ).append(
                                        {
                                            "status": new_status,
                                            "tanggal": str(date.today()),
                                            "oleh": nama
                                        }
                                    )

                        ds.set_data(
                            "laporan",
                            current
                        )

                        st.success(
                            f"Status laporan berhasil diubah menjadi {new_status}"
                        )

                        st.rerun()

        st.divider()

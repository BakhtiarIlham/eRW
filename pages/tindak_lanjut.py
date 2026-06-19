import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds


def render():
    user = st.session_state.get("user", {})
    nama = user.get("nama", "")

    st.markdown('<div class="page-title">🔧 Tindak Lanjut Laporan</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Update progres penanganan laporan warga</div>', unsafe_allow_html=True)

    laporan_list = ds.get("laporan")
    my_laporan   = [l for l in laporan_list if l.get("petugas") == nama or l["status"] == "Diverifikasi"]

    if not my_laporan:
        st.info("Tidak ada laporan yang perlu ditindaklanjuti saat ini.")
        return

    for l in my_laporan:
        badge_cls = {"Diverifikasi":"badge-yellow","Diproses":"badge-blue","Selesai":"badge-green"}.get(l["status"],"badge-gray")
        with st.container():
            st.markdown(
                f"""<div class="card">
                  <div style="font-weight:700; font-size:1rem; color:#1E3A8A;">{l['judul']}
                    <span class="badge {badge_cls}" style="margin-left:8px;">{l['status']}</span>
                  </div>
                  <div style="font-size:0.8rem; color:#6B7280; margin:4px 0 8px;">👤 {l['nama']} · 📅 {l['tanggal']}</div>
                  <div style="font-size:0.87rem; color:#374151; margin-bottom:8px;">{l['deskripsi']}</div>
                </div>""",
                unsafe_allow_html=True,
            )

            if l["status"] in ["Diverifikasi", "Diproses"]:
                with st.expander("📝 Update Status & Catatan"):
                    catatan  = st.text_area("Catatan Penanganan", value=l.get("catatan",""), key=f"cat_{l['id']}")
                    new_stat = st.selectbox("Update Status", ["Diproses", "Selesai", "Ditolak"], key=f"st_{l['id']}")
                    if st.button("💾 Update Laporan", type="primary", key=f"upd_{l['id']}"):
                        current = ds.get("laporan")
                        for item in current:
                            if item["id"] == l["id"]:
                                item["status"]  = new_stat
                                item["catatan"] = catatan
                                item["petugas"] = nama
                        ds.set_data("laporan", current)
                        st.success(f"✅ Status laporan '{l['judul']}' diperbarui menjadi {new_stat}.")
                        st.rerun()

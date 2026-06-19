import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds


STATUS_FLOW = {
    "Pengurus RW": ("Menunggu", "Diverifikasi"),
    "Pengurus RT": ("Menunggu", "Diverifikasi"),
    "Petugas Operasional": ("Diverifikasi", "Diproses"),
}

BADGE = {
    "Menunggu":    "badge-gray",
    "Diverifikasi":"badge-yellow",
    "Diproses":    "badge-blue",
    "Selesai":     "badge-green",
    "Ditolak":     "badge-red",
}


def render():
    user = st.session_state.get("user", {})
    role = user.get("role", "")

    st.markdown('<div class="page-title">📋 Kelola Laporan Warga</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Verifikasi dan tindaklanjuti laporan pengaduan warga</div>', unsafe_allow_html=True)

    laporan_list = ds.get("laporan")

    # Filter
    col_f, _ = st.columns([2, 4])
    with col_f:
        f_stat = st.selectbox("Filter Status", ["Semua", "Menunggu", "Diverifikasi", "Diproses", "Selesai", "Ditolak"])

    filtered = laporan_list if f_stat == "Semua" else [l for l in laporan_list if l["status"] == f_stat]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    for l in filtered[::-1]:
        badge_cls = BADGE.get(l["status"], "badge-gray")
        st.markdown(
            f"""<div style="padding:12px 0; border-bottom:1px solid #F3F4F6;">
              <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div style="flex:1;">
                  <span style="font-weight:700; color:#1E3A8A;">{l['judul']}</span>
                  <span class="badge {badge_cls}" style="margin-left:10px;">{l['status']}</span>
                  <div style="font-size:0.8rem; color:#6B7280; margin:4px 0 6px;">
                    👤 {l['nama']} &nbsp;·&nbsp; 📅 {l['tanggal']}
                    {f"&nbsp;·&nbsp; 🔧 {l['petugas']}" if l.get('petugas') else ''}
                  </div>
                  <div style="font-size:0.87rem; color:#374151;">{l['deskripsi']}</div>
                  {f"<div style='margin-top:6px; font-size:0.83rem; color:#059669; background:#ECFDF5; padding:4px 8px; border-radius:6px; display:inline-block;'>📝 {l['catatan']}</div>" if l.get('catatan') else ''}
                </div>
              </div>
            </div>""",
            unsafe_allow_html=True,
        )

        # Action buttons
        if role in ["Pengurus RW", "Pengurus RT"] and l["status"] == "Menunggu":
            cb1, cb2, _ = st.columns([1.5, 1.5, 5])
            with cb1:
                if st.button("✅ Verifikasi", key=f"ver_l_{l['id']}"):
                    current = ds.get("laporan")
                    for item in current:
                        if item["id"] == l["id"]:
                            item["status"] = "Diverifikasi"
                    ds.set_data("laporan", current)
                    st.rerun()
            with cb2:
                if st.button("❌ Tolak", key=f"tol_l_{l['id']}"):
                    current = ds.get("laporan")
                    for item in current:
                        if item["id"] == l["id"]:
                            item["status"] = "Ditolak"
                    ds.set_data("laporan", current)
                    st.rerun()

        if role == "Petugas Operasional" and l["status"] == "Diverifikasi":
            if st.button("🔧 Ambil & Proses", key=f"proses_{l['id']}"):
                current = ds.get("laporan")
                for item in current:
                    if item["id"] == l["id"]:
                        item["status"]   = "Diproses"
                        item["petugas"]  = user.get("nama", "")
                ds.set_data("laporan", current)
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

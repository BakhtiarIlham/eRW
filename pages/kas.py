import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds
from datetime import date


def render():
    st.markdown('<div class="page-title">💰 Kelola Kas Warga</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Input dan verifikasi pembayaran kas warga</div>', unsafe_allow_html=True)

    kas_list = ds.get("kas")
    role     = st.session_state.get("user", {}).get("role", "")

    # ── Summary cards ────────────────────────────────────────────────────────
    total_lunas = sum(k["nominal"] for k in kas_list if k["status"] == "Lunas")
    total_belum = sum(k["nominal"] for k in kas_list if k["status"] == "Belum Lunas")
    pending_ver = sum(1 for k in kas_list if k["status"] == "Menunggu Verifikasi")

    c1, c2, c3 = st.columns(3)
    c1.markdown(
        f"""<div class="metric-card">
          <div class="metric-icon" style="background:#A7F3D0;">✅</div>
          <div><div class="metric-label">Total Terkumpul</div>
               <div class="metric-value" style="color:#065F46;">Rp {total_lunas:,}</div></div>
        </div>""", unsafe_allow_html=True)
    c2.markdown(
        f"""<div class="metric-card">
          <div class="metric-icon" style="background:#FECACA;">⚠️</div>
          <div><div class="metric-label">Belum Lunas</div>
               <div class="metric-value" style="color:#991B1B;">Rp {total_belum:,}</div></div>
        </div>""", unsafe_allow_html=True)
    c3.markdown(
        f"""<div class="metric-card">
          <div class="metric-icon" style="background:#FDE68A;">⏳</div>
          <div><div class="metric-label">Menunggu Verifikasi</div>
               <div class="metric-value" style="color:#92400E;">{pending_ver} orang</div></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Input pembayaran (RW only) ───────────────────────────────────────────
    if role == "Pengurus RW":
        with st.expander("➕ Input Pembayaran Kas Baru"):
            warga_list = ds.get("warga")
            nama_options = {w["nama"]: w["id"] for w in warga_list if w["status"] == "Aktif"}
            c1, c2, c3 = st.columns(3)
            with c1:
                pilih_warga = st.selectbox("Pilih Warga", list(nama_options.keys()))
            with c2:
                nominal = st.number_input("Nominal (Rp)", min_value=0, value=50000, step=10000)
            with c3:
                tgl = st.date_input("Tanggal Bayar", value=date.today())
            if st.button("💾 Simpan Pembayaran", type="primary"):
                current = ds.get("kas")
                new_id  = max((k["id"] for k in current), default=0) + 1
                current.append({
                    "id": new_id,
                    "id_warga": nama_options[pilih_warga],
                    "nama": pilih_warga,
                    "nominal": nominal,
                    "tanggal": str(tgl),
                    "status": "Lunas",
                })
                ds.set_data("kas", current)
                st.success(f"✅ Pembayaran {pilih_warga} sebesar Rp {nominal:,} tersimpan.")
                st.rerun()

    # ── Filter ──────────────────────────────────────────────────────────────
    col_f1, col_f2 = st.columns([1, 3])
    with col_f1:
        filter_status = st.selectbox("Filter Status", ["Semua", "Lunas", "Belum Lunas", "Menunggu Verifikasi"])

    filtered = kas_list if filter_status == "Semua" else [k for k in kas_list if k["status"] == filter_status]

    # ── Table ────────────────────────────────────────────────────────────────
    st.markdown('<div class="card">', unsafe_allow_html=True)
    rows = ""
    for k in filtered:
        badge_cls = {
            "Lunas": "badge-green",
            "Belum Lunas": "badge-red",
            "Menunggu Verifikasi": "badge-yellow",
        }.get(k["status"], "badge-gray")

        aksi = ""
        if k["status"] == "Menunggu Verifikasi" and role == "Pengurus RW":
            aksi = f"verif_{k['id']}"

        rows += f"""<tr>
          <td>{k['nama']}</td>
          <td>Rp {k['nominal']:,}</td>
          <td>{k['tanggal']}</td>
          <td><span class="badge {badge_cls}">{k['status']}</span></td>
        </tr>"""

    st.markdown(
        f"""<table class="styled-table"><thead><tr>
          <th>Nama Warga</th><th>Nominal</th><th>Tanggal</th><th>Status</th>
        </tr></thead><tbody>{rows}</tbody></table>""",
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Verifikasi buttons (bawah tabel agar mudah) ─────────────────────────
    if role == "Pengurus RW":
        pending = [k for k in kas_list if k["status"] == "Menunggu Verifikasi"]
        if pending:
            st.markdown("**⏳ Verifikasi Pembayaran Pending:**")
            for k in pending:
                col_n, col_b = st.columns([5, 1])
                col_n.markdown(f"• **{k['nama']}** — Rp {k['nominal']:,} ({k['tanggal']})")
                if col_b.button("✅ Verifikasi", key=f"ver_{k['id']}"):
                    current = ds.get("kas")
                    for item in current:
                        if item["id"] == k["id"]:
                            item["status"] = "Lunas"
                    ds.set_data("kas", current)
                    st.success(f"Pembayaran {k['nama']} diverifikasi!")
                    st.rerun()

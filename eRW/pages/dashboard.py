import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_store as ds


def metric_card(icon, label, value, color="#EEF2FF", icon_bg="#C7D2FE"):
    return f"""
    <div class="metric-card">
      <div class="metric-icon" style="background:{icon_bg};">{icon}</div>
      <div>
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color:#1E3A8A;">{value}</div>
      </div>
    </div>
    """


def render():
    user = st.session_state.get("user", {})
    role = user.get("role", "")
    nama = user.get("nama", "")

    warga_list   = ds.get("warga")
    kas_list     = ds.get("kas")
    bansos_list  = ds.get("bansos")
    laporan_list = ds.get("laporan")
    pengumuman   = ds.get("pengumuman")

    # ── Header ──────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="page-title">🏠 Dashboard</div>
        <div class="page-subtitle">Selamat datang, <b>{nama}</b> — {role}</div>
        """,
        unsafe_allow_html=True,
    )

    # ══════════════════════════════════════════════════════════════════════════
    # PENGURUS RW
    # ══════════════════════════════════════════════════════════════════════════
    if role == "Pengurus RW":
        total_warga  = len(warga_list)
        aktif_warga  = sum(1 for w in warga_list if w["status"] == "Aktif")
        total_kas    = sum(k["nominal"] for k in kas_list if k["status"] == "Lunas")
        total_bansos = len(bansos_list)
        lap_open     = sum(1 for l in laporan_list if l["status"] in ["Menunggu","Diverifikasi","Diproses"])

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(metric_card("👥", "Total Warga",      total_warga,          "#EEF2FF", "#C7D2FE"), unsafe_allow_html=True)
        c2.markdown(metric_card("✅", "Warga Aktif",      aktif_warga,          "#ECFDF5", "#A7F3D0"), unsafe_allow_html=True)
        c3.markdown(metric_card("💰", "Total Kas (Rp)",   f"{total_kas:,}",     "#FFFBEB", "#FDE68A"), unsafe_allow_html=True)
        c4.markdown(metric_card("📋", "Laporan Aktif",    lap_open,             "#FEF2F2", "#FECACA"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_l, col_r = st.columns([3, 2])

        with col_l:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📋 Laporan Terbaru</div><br>', unsafe_allow_html=True)
            rows = ""
            for l in laporan_list[-4:][::-1]:
                badge_cls = {"Selesai":"badge-green","Diproses":"badge-blue","Diverifikasi":"badge-yellow","Menunggu":"badge-gray"}.get(l["status"],"badge-gray")
                rows += f"""<tr>
                  <td>{l['nama']}</td>
                  <td>{l['judul']}</td>
                  <td>{l['tanggal']}</td>
                  <td><span class="badge {badge_cls}">{l['status']}</span></td>
                </tr>"""
            st.markdown(
                f"""<table class="styled-table"><thead><tr>
                  <th>Nama</th><th>Judul</th><th>Tanggal</th><th>Status</th>
                </tr></thead><tbody>{rows}</tbody></table>""",
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

        with col_r:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📢 Pengumuman Terbaru</div><br>', unsafe_allow_html=True)
            for p in pengumuman[-3:][::-1]:
                st.markdown(
                    f"""<div style="border-left:3px solid #3B82F6; padding:6px 10px; margin-bottom:10px; border-radius:4px; background:#F9FAFB;">
                      <div style="font-weight:600; font-size:0.87rem; color:#1E3A8A;">{p['judul']}</div>
                      <div style="font-size:0.76rem; color:#9CA3AF;">{p['tanggal']} · {p['oleh']}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🎁 Bansos Aktif</div><br>', unsafe_allow_html=True)
            aktif_b = sum(1 for b in bansos_list if b["status"] == "Aktif")
            st.markdown(
                f'<div style="font-size:2rem; font-weight:700; color:#1E3A8A; text-align:center;">{aktif_b}</div>'
                '<div style="text-align:center; color:#6B7280; font-size:0.85rem;">dari {total_bansos} penerima</div>'.format(total_bansos=total_bansos),
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # PENGURUS RT
    # ══════════════════════════════════════════════════════════════════════════
    elif role == "Pengurus RT":
        menunggu_validasi = sum(1 for w in warga_list if w["validasi"] == "Menunggu")
        lap_rt = [l for l in laporan_list if l["status"] in ["Menunggu", "Diverifikasi"]]

        c1, c2, c3 = st.columns(3)
        c1.markdown(metric_card("⏳", "Validasi Pending",  menunggu_validasi, "#FFFBEB", "#FDE68A"), unsafe_allow_html=True)
        c2.markdown(metric_card("📋", "Laporan Masuk",     len(lap_rt),       "#FEF2F2", "#FECACA"), unsafe_allow_html=True)
        c3.markdown(metric_card("📢", "Pengumuman Aktif",  len(pengumuman),   "#EEF2FF", "#C7D2FE"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⏳ Warga Menunggu Validasi</div><br>', unsafe_allow_html=True)
        rows = ""
        for w in [x for x in warga_list if x["validasi"] == "Menunggu"]:
            rows += f"<tr><td>{w['nik']}</td><td>{w['nama']}</td><td>{w['alamat']}</td><td><span class='badge badge-yellow'>Menunggu</span></td></tr>"
        if not rows:
            rows = "<tr><td colspan='4' style='text-align:center;color:#9CA3AF;'>Tidak ada data menunggu validasi</td></tr>"
        st.markdown(
            f"""<table class="styled-table"><thead><tr><th>NIK</th><th>Nama</th><th>Alamat</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table>""",
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # PETUGAS OPERASIONAL
    # ══════════════════════════════════════════════════════════════════════════
    elif role == "Petugas Operasional":
        lap_verified  = [l for l in laporan_list if l["status"] == "Diverifikasi"]
        lap_diproses  = [l for l in laporan_list if l["status"] == "Diproses"]
        lap_selesai   = [l for l in laporan_list if l["status"] == "Selesai"]

        c1, c2, c3 = st.columns(3)
        c1.markdown(metric_card("📬", "Perlu Ditangani",  len(lap_verified), "#FEF2F2", "#FECACA"), unsafe_allow_html=True)
        c2.markdown(metric_card("🔧", "Sedang Diproses",  len(lap_diproses), "#FFFBEB", "#FDE68A"), unsafe_allow_html=True)
        c3.markdown(metric_card("✅", "Selesai",           len(lap_selesai),  "#ECFDF5", "#A7F3D0"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📬 Laporan Yang Perlu Ditindaklanjuti</div><br>', unsafe_allow_html=True)
        rows = ""
        for l in (lap_verified + lap_diproses):
            badge_cls = "badge-blue" if l["status"] == "Diproses" else "badge-yellow"
            rows += f"<tr><td>{l['nama']}</td><td>{l['judul']}</td><td>{l['tanggal']}</td><td><span class='badge {badge_cls}'>{l['status']}</span></td></tr>"
        if not rows:
            rows = "<tr><td colspan='4' style='text-align:center;color:#9CA3AF;'>Tidak ada laporan menunggu</td></tr>"
        st.markdown(
            f"""<table class="styled-table"><thead><tr><th>Pelapor</th><th>Judul</th><th>Tanggal</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table>""",
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # WARGA
    # ══════════════════════════════════════════════════════════════════════════
    elif role == "Warga":
        kas_warga     = [k for k in kas_list if k["id_warga"] == 1]
        bansos_warga  = [b for b in bansos_list if b["id_warga"] == 1]
        laporan_warga = [l for l in laporan_list if l["id_warga"] == 1]
        status_kas    = kas_warga[-1]["status"] if kas_warga else "Belum Ada"

        c1, c2, c3 = st.columns(3)
        c1.markdown(metric_card("💳", "Status Kas Bulan Ini", status_kas, "#EEF2FF", "#C7D2FE"), unsafe_allow_html=True)
        c2.markdown(metric_card("🎁", "Bansos Diterima",   len(bansos_warga),  "#ECFDF5", "#A7F3D0"), unsafe_allow_html=True)
        c3.markdown(metric_card("📋", "Laporan Dikirim",   len(laporan_warga), "#FFFBEB", "#FDE68A"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_l, col_r = st.columns([3, 2])

        with col_l:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📢 Pengumuman Terbaru</div><br>', unsafe_allow_html=True)
            for p in pengumuman[:3]:
                st.markdown(
                    f"""<div style="border-left:3px solid #3B82F6; padding:8px 12px; margin-bottom:12px; border-radius:4px; background:#F9FAFB;">
                      <div style="font-weight:600; color:#1E3A8A; font-size:0.9rem;">{p['judul']}</div>
                      <div style="font-size:0.8rem; color:#6B7280; margin-top:3px;">{p['isi'][:80]}…</div>
                      <div style="font-size:0.72rem; color:#9CA3AF; margin-top:4px;">{p['tanggal']}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

        with col_r:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📋 Status Laporan Saya</div><br>', unsafe_allow_html=True)
            if laporan_warga:
                for l in laporan_warga:
                    badge_cls = {"Selesai":"badge-green","Diproses":"badge-blue","Diverifikasi":"badge-yellow","Menunggu":"badge-gray"}.get(l["status"],"badge-gray")
                    st.markdown(
                        f"""<div style="padding:8px 0; border-bottom:1px solid #F3F4F6;">
                          <div style="font-weight:500; font-size:0.88rem;">{l['judul']}</div>
                          <div style="margin-top:4px;"><span class="badge {badge_cls}">{l['status']}</span></div>
                        </div>""",
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown('<p style="color:#9CA3AF; font-size:0.85rem;">Belum ada laporan.</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

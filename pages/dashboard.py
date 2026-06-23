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


def render_card(title, subtitle, meta, badge_cls):
    return f"""
    <div class='panel-card-sm'>
      <div class='panel-card-title'>{title}</div>
      <div class='panel-card-text'>{subtitle}</div>
      <div class='panel-card-meta'>{meta}</div>
      <div style='margin-top:0.8rem; text-align:right;'>
        <span class='badge {badge_cls}' style='font-size:0.8rem; padding:0.45rem 0.9rem;'>
          {badge_cls.replace('badge-','').capitalize()}
        </span>
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
            st.markdown("<div class='section-heading'>📋 Laporan Terbaru</div>", unsafe_allow_html=True)
            recent = laporan_list[-4:][::-1]
            if recent:
                for l in recent:
                    badge_cls = {"Selesai":"badge-green","Diproses":"badge-blue","Diverifikasi":"badge-yellow","Menunggu":"badge-gray"}.get(l["status"],"badge-gray")
                    st.markdown(
                        render_card(
                            title=f"{l['nama']}",
                            subtitle=l['judul'],
                            meta=f"📅 {l['tanggal']}",
                            badge_cls=badge_cls,
                        ),
                        unsafe_allow_html=True,
                    )
                    if st.button("🔍", key=f"dash_rw_lap_{l['id']}", help="Lihat Detail"):
                        st.session_state["detail_laporan_id"] = l["id"]
                        st.session_state["detail_laporan_back"] = "dashboard"
                        st.session_state["current_page"] = "detail_laporan"
                        st.rerun()
            else:
                st.info("📭 Belum ada laporan.")

        with col_r:
            st.markdown("<div class='section-heading'>📢 Pengumuman Terbaru</div>", unsafe_allow_html=True)
            if pengumuman:
                for p in pengumuman[-3:][::-1]:
                    st.markdown(
                        f"""<div class='panel-card-sm'>
                              <div class='panel-card-title'>{p['judul']}</div>
                              <div class='panel-card-text'>{p['isi'][:120] + ('…' if len(p['isi']) > 120 else '')}</div>
                              <div class='panel-card-meta'>📅 {p['tanggal']} • {p['oleh']}</div>
                            </div>""",
                        unsafe_allow_html=True,
                    )
            else:
                st.info("📭 Belum ada pengumuman.")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='section-heading'>🎁 Bansos Aktif</div>", unsafe_allow_html=True)
            aktif_b = sum(1 for b in bansos_list if b["status"] == "Aktif")
            st.markdown(
                f"""<div class='panel-card-sm'>
                      <div class='panel-card-title'>Status Bansos</div>
                      <div class='panel-card-text'>Aktif: <strong>{aktif_b}</strong> dari <strong>{total_bansos}</strong> penerima</div>
                    </div>""",
                unsafe_allow_html=True,
            )

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
        st.subheader("⏳ Warga Menunggu Validasi")
        pending_w = [x for x in warga_list if x["validasi"] == "Menunggu"]
        if pending_w:
            for idx, w in enumerate(pending_w):
                c1, c2, c3 = st.columns([3.5, 1, 1])
                with c1:
                    st.write(f"**{w['nama']}**")
                    st.caption(f"🪪 {w['nik']} • 🏠 {w['alamat']}")
                with c2:
                    st.markdown('<span class="badge badge-yellow">Menunggu</span>', unsafe_allow_html=True)
                with c3:
                    if st.button("🔍", key=f"dash_rt_warga_{w['id']}", help="Lihat Detail"):
                        st.session_state["detail_warga_id"] = w["id"]
                        st.session_state["current_page"] = "detail_warga"
                        st.rerun()
                if idx < len(pending_w) - 1:
                    st.divider()
        else:
            st.info("✅ Tidak ada data menunggu validasi.")

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
        st.subheader("📬 Laporan Yang Perlu Ditindaklanjuti")
        antrian = lap_verified + lap_diproses
        if antrian:
            for idx, l in enumerate(antrian):
                badge_cls = "badge-blue" if l["status"] == "Diproses" else "badge-yellow"
                c1, c2, c3 = st.columns([4, 1, 1])
                with c1:
                    st.write(f"**{l['nama']}** — {l['judul']}")
                    st.caption(f"📅 {l['tanggal']}")
                with c2:
                    st.markdown(f'<span class="badge {badge_cls}">{l["status"]}</span>', unsafe_allow_html=True)
                with c3:
                    if st.button("🔍", key=f"dash_pet_lap_{l['id']}", help="Lihat Detail"):
                        st.session_state["detail_laporan_id"] = l["id"]
                        st.session_state["detail_laporan_back"] = "dashboard"
                        st.session_state["current_page"] = "detail_laporan"
                        st.rerun()
                if idx < len(antrian) - 1:
                    st.divider()
        else:
            st.info("✅ Tidak ada laporan menunggu.")

    # ══════════════════════════════════════════════════════════════════════════
    # WARGA
    # ══════════════════════════════════════════════════════════════════════════
    elif role == "Warga":
        w_self        = ds.get_warga_by_nama(nama) or {"id": 1}
        kas_warga     = [k for k in kas_list if k["id_warga"] == w_self["id"]]
        bansos_warga  = [b for b in bansos_list if b["id_warga"] == w_self["id"]]
        laporan_warga = [l for l in laporan_list if l["id_warga"] == w_self["id"]]
        status_kas    = kas_warga[-1]["status"] if kas_warga else "Belum Ada"

        c1, c2, c3 = st.columns(3)
        c1.markdown(metric_card("💳", "Status Kas Bulan Ini", status_kas, "#EEF2FF", "#C7D2FE"), unsafe_allow_html=True)
        c2.markdown(metric_card("🎁", "Bansos Diterima",   len(bansos_warga),  "#ECFDF5", "#A7F3D0"), unsafe_allow_html=True)
        c3.markdown(metric_card("📋", "Laporan Dikirim",   len(laporan_warga), "#FFFBEB", "#FDE68A"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_l, col_r = st.columns([3, 2])

        with col_l:
            st.subheader("📢 Pengumuman Terbaru")
            if pengumuman:
                for p in pengumuman[:3]:
                    st.markdown(
                        f"""<div style="border-left:4px solid #3B82F6; padding:8px 12px; margin-bottom:10px; border-radius:4px; background:#F9FAFB;">
                          <div style="font-weight:600; color:#1E3A8A; font-size:0.9rem;">{p['judul']}</div>
                          <div style="font-size:0.8rem; color:#6B7280; margin-top:3px;">{p['isi'][:80] if len(p['isi']) > 80 else p['isi']}{'…' if len(p['isi']) > 80 else ''}</div>
                          <div style="font-size:0.72rem; color:#9CA3AF; margin-top:4px;">{p['tanggal']}</div>
                        </div>""",
                        unsafe_allow_html=True,
                    )
            else:
                st.info("📭 Belum ada pengumuman.")

        with col_r:
            st.subheader("📋 Status Laporan Saya")
            if laporan_warga:
                for idx, l in enumerate(laporan_warga[::-1]):
                    badge_cls = {"Selesai":"badge-green","Diproses":"badge-blue","Diverifikasi":"badge-yellow","Menunggu":"badge-gray"}.get(l["status"],"badge-gray")
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.write(f"**{l['judul']}**")
                        st.markdown(f'<span class="badge {badge_cls}">{l["status"]}</span>', unsafe_allow_html=True)
                    with c2:
                        if st.button("🔍", key=f"dash_warga_lap_{l['id']}", help="Lihat Detail"):
                            st.session_state["detail_laporan_id"] = l["id"]
                            st.session_state["detail_laporan_back"] = "dashboard"
                            st.session_state["current_page"] = "detail_laporan"
                            st.rerun()
                    if idx < len(laporan_warga) - 1:
                        st.divider()
            else:
                st.info("📭 Belum ada laporan.")

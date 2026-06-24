import streamlit as st

# ── Page config (must be first) ──────────────────────────────────────────────
st.set_page_config(
    page_title="e-RW | Sistem Layanan Warga",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Dummy accounts ────────────────────────────────────────────────────────────
USERS = {
    "rw@erw.id":      {"password": "rw123",       "role": "Pengurus RW",         "nama": "Budi Santoso"},
    "rt@erw.id":      {"password": "rt123",        "role": "Pengurus RT",         "nama": "Siti Rahayu"},
    "petugas@erw.id": {"password": "petugas123",   "role": "Petugas Operasional", "nama": "Ahmad Fauzi"},
    "warga@erw.id":   {"password": "warga123",     "role": "Warga",               "nama": "Dewi Lestari"},
}

# ── Global CSS ─────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        html, body, .stApp { font-family: 'Inter', sans-serif; }
        .stApp { background: #F0F4FF; }
        #MainMenu, footer, header { visibility: hidden; }
        .block-container { padding-top: 1rem; }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1E3A8A 0%, #1D4ED8 100%);
            border-right: none;
        }
        [data-testid="stSidebar"] {
        min-width: 280px !important;
        width: 280px !important;
        }
        [data-testid="stSidebar"] * { color: #E0E7FF !important; }
        [data-testid="stSidebar"] .stButton > button {
            background: rgba(255,255,255,0.08) !important;
            border: 1px solid rgba(255,255,255,0.15) !important;
            color: white !important;
            width: 100% !important;
            text-align: left !important;
            border-radius: 10px !important;
            margin-bottom: 4px !important;
            transition: all 0.2s !important;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(255,255,255,0.18) !important;
            transform: translateX(4px) !important;
        }

        .card {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
            border: 1px solid #E8F0FE;
            margin-bottom: 1rem;
        }
        .metric-card {
            background: white;
            border-radius: 16px;
            padding: 1.4rem 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            border: 1px solid #E8F0FE;
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        .metric-icon {
            font-size: 2rem;
            width: 52px; height: 52px;
            display: flex; align-items: center; justify-content: center;
            border-radius: 12px;
        }
        .metric-label { color: #6B7280; font-size: 0.82rem; font-weight: 500; }
        .metric-value { color: #111827; font-size: 1.6rem; font-weight: 700; line-height: 1; }

        .page-title    { font-size: 1.5rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0.2rem; }
        .page-subtitle { color: #6B7280; font-size: 0.88rem; margin-bottom: 1.5rem; }

        .badge         { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.76rem; font-weight: 600; }
        .badge-green   { background:#D1FAE5; color:#065F46; }
        .badge-yellow  { background:#FEF3C7; color:#92400E; }
        .badge-blue    { background:#DBEAFE; color:#1E40AF; }
        .badge-red     { background:#FEE2E2; color:#991B1B; }
        .badge-gray    { background:#F3F4F6; color:#374151; }

        .styled-table             { width:100%; border-collapse:collapse; font-size:0.88rem; }
        .styled-table th          { background:#EEF2FF; color:#1E3A8A; font-weight:600; padding:10px 14px; text-align:left; border-bottom:2px solid #C7D2FE; }
        .styled-table td          { padding:9px 14px; border-bottom:1px solid #F3F4F6; color:#374151; }
        .styled-table tr:hover td { background:#F9FAFB; }

        .stButton > button { border-radius: 10px !important; font-weight: 500 !important; transition: all 0.2s !important; }
        .stButton button { border-radius: 10px;}

        .logout-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: white;
            border-radius: 12px;
            padding: 0.6rem 1.2rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
            border: 1px solid #E8F0FE;
        }

        .login-container {
            max-width: 420px; margin: 4vh auto 0; padding: 2.5rem;
            background: white; border-radius: 20px;
            box-shadow: 0 8px 40px rgba(30,58,138,0.12); border: 1px solid #E0E7FF;
        }
        .login-logo { text-align: center; margin-bottom: 1.5rem; }
        .login-logo .icon { font-size: 3rem; }
        .login-logo h1 { color: #1E3A8A; font-size: 1.8rem; font-weight: 700; margin: 0.2rem 0 0; }
        .login-logo p  { color: #6B7280; font-size: 0.85rem; margin: 0; }

        .info-box {
            background: #EFF6FF; border-left: 4px solid #3B82F6;
            border-radius: 8px; padding: 0.8rem 1rem;
            font-size: 0.83rem; color: #1E40AF; margin-bottom: 1rem;
        }
        .section-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:1rem; }
        .section-title  { font-size:1rem; font-weight:700; color:#1E3A8A; margin-bottom:0.2rem; }

        /* ── Panel detail interaktif ───────────────────────────────────── */
        .detail-panel {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 16px;
            padding: 1rem 1.2rem;
            margin-bottom: 1rem;
        }
        .detail-header {
            display:flex; align-items:center; gap:0.8rem; margin-bottom:0.9rem;
            padding-bottom:0.8rem; border-bottom:1px solid #E0E7FF;
        }
        .detail-avatar {
            width:46px; height:46px; border-radius:50%;
            background:linear-gradient(135deg,#1D4ED8,#3B82F6);
            display:flex; align-items:center; justify-content:center;
            font-size:1.3rem; color:white; flex-shrink:0;
        }
        .detail-label { font-size:0.74rem; color:#9CA3AF; margin-bottom:1px; }
        .detail-value { font-size:0.9rem; color:#1F2937; font-weight:500; }
        .detail-grid {
            display:grid;
            grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
            gap:1rem;
        }
        .info-item { background:#F8FAFC; border-radius:12px; padding:0.8rem; }
        .info-label { color:#6B7280; font-size:0.75rem; margin-bottom:4px; }
        .info-value { color:#111827; font-weight:600; font-size:0.9rem; }

        /* ── Timeline status laporan ──────────────────────────────────── */
        .timeline-card {
            background:white; border:1px solid #E5E7EB; border-radius:14px;
            padding:1rem; margin-bottom:0.75rem;
        }
        .tl-item { display:flex; gap:0.7rem; padding-bottom:1rem; position:relative; }
        .tl-item:not(:last-child)::before {
            content:""; position:absolute; left:13px; top:30px; bottom:0;
            width:2px; background:#E0E7FF;
        }
        .tl-dot {
            width:28px; height:28px; border-radius:50%; flex-shrink:0;
            background:#1D4ED8; color:white; font-size:0.8rem;
            display:flex; align-items:center; justify-content:center; font-weight:700;
            margin-top:1px; z-index:1;
        }
        .tl-text   { font-size:0.86rem; color:#1F2937; font-weight:600; }
        .tl-meta   { font-size:0.74rem; color:#9CA3AF; margin-top:1px; }

        /* ── Empty state konsisten ────────────────────────────────────── */
        .empty-state {
            text-align:center; padding:2.6rem 1.5rem;
            color:#6B7280;
        }
        .empty-state .es-icon { font-size:2.6rem; margin-bottom:0.6rem; opacity:0.85; }
        .empty-state .es-title { font-size:0.95rem; font-weight:600; color:#374151; margin-bottom:4px; }
        .empty-state .es-sub { font-size:0.82rem; color:#9CA3AF; }

        /* ── Sidebar: item menu aktif ─────────────────────────────────── */
        .nav-active, .nav-inactive { margin-bottom: 2px; }
        .nav-active > button {
            background: rgba(255,255,255,0.22) !important;
            border-color: rgba(255,255,255,0.4) !important;
            font-weight: 700 !important;
        }
        .nav-active > button::after { content: " ●"; opacity: 0.8; font-size: 0.6rem; }

        /* ── Tambahan: kartu lampiran file ────────────────────────────────── */
        .file-chip {
            display:flex; align-items:center; gap:0.6rem;
            background:white; border:1px solid #E0E7FF; border-radius:10px;
            padding:0.6rem 0.9rem; margin-top:0.5rem;
        }
        .file-chip .fi { font-size:1.4rem; }
        .file-chip .fn { font-size:0.85rem; font-weight:600; color:#1E3A8A; }
        .file-chip .fs { font-size:0.72rem; color:#9CA3AF; }

        .file-chip:hover {
            background:#EFF6FF;
            border-color:#93C5FD;
        }

        /* ── Panel & card pendukung lainnya ───────────────────────────── */
        .panel-section {
            background: #FFFFFF;
            border: 1px solid #DBEAFE;
            border-radius: 18px;
            padding: 1.25rem;
            margin-bottom: 1rem;
        }
        .panel-card-sm {
            background: #EFF6FF;
            border: 1px solid #BBD7FF;
            border-radius: 18px;
            padding: 1rem 1.1rem;
            margin-bottom: 0.85rem;
            box-shadow: 0 14px 30px rgba(29, 78, 216, 0.08);
            transition: all 0.2s ease;
        }
        .panel-card-sm:hover {
            transform: translateY(-1px);
            box-shadow: 0 16px 32px rgba(29, 78, 216, 0.12);
        }
        .panel-card-title {
            color: #1E40AF;
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 0.35rem;
        }
        .panel-card-text {
            color: #0F172A;
            font-size: 0.9rem;
            margin-bottom: 0.55rem;
            line-height: 1.55;
        }
        .panel-card-meta {
            color: #475569;
            font-size: 0.82rem;
        }

        /* ── Heading konsisten untuk semua section di seluruh halaman ──── */
        .section-heading {
            color: #1D4ED8;
            font-size: 1.12rem;
            font-weight: 800;
            margin-bottom: 1rem;
        }
        .section-heading-secondary {
            color: #0F172A;
            font-size: 1.15rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }
        .section-subtitle {
            color: #475569;
            font-size: 0.88rem;
        }

        /* ── Tombol: gaya solid biru jadi default, kecuali tombol icon kecil ── */
        .stButton > button {
            border-radius: 10px !important;
            font-weight: 500 !important;
            transition: all 0.2s !important;
            background: #1D4ED8 !important;
            border: 1px solid #2563EB !important;
            color: white !important;
        }
        .stButton > button:hover {
            background: #1E40AF !important;
            border-color: #1E40AF !important;
        }
        /* Tombol aksi sekunder/icon dalam tabel (Lihat/Edit) tetap soft */
        div[data-testid="column"] .stButton > button[kind="secondary"] {
            background:#EEF2FF !important; color:#1E3A8A !important;
            border:1px solid #C7D2FE !important;
        }
        /* Tombol berbahaya (hapus, tolak, batal) — beri warna merah lembut
           lewat data-testid khusus yang kita pasang dari Python via help text
           class tidak bisa diberi langsung oleh Streamlit, jadi kita pakai
           kontainer pembungkus .danger-zone untuk menandai area tombol hapus. */
        .danger-zone .stButton > button {
            background:#FEF2F2 !important; color:#991B1B !important;
            border:1px solid #FECACA !important;
        }
        .danger-zone .stButton > button:hover {
            background:#FEE2E2 !important; border-color:#FCA5A5 !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# ── Session helpers ────────────────────────────────────────────────────────────
def is_logged_in() -> bool:
    return st.session_state.get("logged_in", False)

def get_user():
    return st.session_state.get("user", {})

def logout():
    for k in ["logged_in", "user", "current_page", "confirm_logout"]:
        st.session_state.pop(k, None)
    st.rerun()


# ── Komponen UI reusable (dipakai oleh semua halaman di folder pages/) ───────
def render_section_header(title: str, subtitle: str = ""):
    """Header judul halaman yang konsisten di semua halaman."""
    sub_html = f'<div class="page-subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f'<div class="page-title">{title}</div>{sub_html}',
        unsafe_allow_html=True,
    )


def render_empty_state(icon: str, title: str, subtitle: str = ""):
    """Tampilan kosong yang konsisten dipakai di semua daftar/tabel
    yang belum punya data, menggantikan campuran st.info() dan HTML ad-hoc."""
    sub_html = f'<div class="es-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f"""<div class="card">
          <div class="empty-state">
            <div class="es-icon">{icon}</div>
            <div class="es-title">{title}</div>
            {sub_html}
          </div>
        </div>""",
        unsafe_allow_html=True,
    )


def confirm_delete_button(item_key: str, trigger_label: str = "🗑️", confirm_text: str = "Yakin ingin menghapus data ini?", use_container_width: bool = False):
    """Tombol hapus dengan konfirmasi dua-langkah agar tidak ada data yang
    terhapus tidak sengaja karena salah klik:
      1) Pengguna klik tombol trigger (ikon 🗑️ atau label lain).
      2) Muncul kotak konfirmasi "Ya, Hapus" / "Batal".
    Mengembalikan True hanya pada klik "Ya, Hapus".

    Pemakaian:
        if confirm_delete_button(f"warga_{w['id']}"):
            # lakukan penghapusan data di sini
    """
    state_key = f"confirm_del_{item_key}"
    deleted = False

    if not st.session_state.get(state_key, False):
        if st.button(trigger_label, key=f"del_btn_{item_key}", use_container_width=use_container_width):
            st.session_state[state_key] = True
            st.rerun()
    else:
        st.markdown('<div class="danger-zone">', unsafe_allow_html=True)
        st.caption(f"⚠️ {confirm_text}")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Ya, Hapus", key=f"del_yes_{item_key}", use_container_width=True):
                st.session_state[state_key] = False
                deleted = True
        with c2:
            if st.button("✖ Batal", key=f"del_no_{item_key}", use_container_width=True):
                st.session_state[state_key] = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    return deleted


# ── Sidebar navigation ─────────────────────────────────────────────────────────
MENUS = {
    "Pengurus RW": [
        ("🏠", "Dashboard",          "dashboard"),
        ("👥", "Kelola Warga",        "warga"),
        ("💰", "Kelola Kas",          "kas"),
        ("🎁", "Kelola Bansos",       "bansos"),
        ("📢", "Pengumuman",          "pengumuman"),
        ("📅", "Kegiatan",            "kegiatan"),
        ("📋", "Laporan",             "laporan"),
    ],
    "Pengurus RT": [
        ("🏠", "Dashboard",           "dashboard"),
        ("✅", "Validasi Warga",       "validasi_warga"),
        ("📢", "Pengumuman RT",        "pengumuman"),
        ("📅", "Kegiatan RT",          "kegiatan"),
        ("📋", "Kelola Laporan",       "laporan"),
    ],
    "Petugas Operasional": [
        ("🏠", "Dashboard",            "dashboard"),
        ("📋", "Lihat Laporan",        "laporan"),
        ("🔧", "Tindak Lanjut",        "tindak_lanjut"),
    ],
    "Warga": [
        ("🏠", "Dashboard",            "dashboard"),
        ("👤", "Data Pribadi",          "profil"),
        ("📢", "Pengumuman",            "pengumuman"),
        ("📅", "Kegiatan",              "kegiatan"),
        ("📩", "Kirim Laporan",         "kirim_laporan"),
        ("📊", "Status Laporan",        "status_laporan"),
        ("💳", "Status Kas",            "status_kas"),
        ("🎁", "Status Bansos",         "status_bansos"),
    ],
}

def render_sidebar():
    """Render panel navigasi di kolom kiri (pengganti st.sidebar bawaan,
    karena beberapa environment Streamlit menyembunyikan sidebar asli).
    Menu yang sedang aktif diberi highlight agar pengguna tahu posisinya."""
    user = get_user()
    role = user.get("role", "")
    menus = MENUS.get(role, [])
    current_page = st.session_state.get("current_page", "dashboard")

    sidebar_html = f"""
    <div style="background: linear-gradient(180deg, #1E3A8A 0%, #1D4ED8 100%);
                            padding:1.2rem; border-radius:12px; color:white;">
        <div style="text-align:center; margin-bottom:0.6rem;">
            <div style="font-size:2rem;">🏘️</div>
            <div style="font-size:1.1rem; font-weight:700; margin-top:6px;">e-RW</div>
            <div style="font-size:0.72rem; opacity:0.92; margin-top:4px;">Sistem Layanan Warga</div>
        </div>
        <div style="background:rgba(255,255,255,0.06); padding:0.65rem; border-radius:10px; margin-bottom:0.9rem;">
            <div style="font-size:0.82rem; opacity:0.95;">Selamat datang,</div>
            <div style="font-weight:600; font-size:0.95rem;">{user.get('nama','')}</div>
            <div style="font-size:0.74rem; opacity:0.9; margin-top:6px;">
                <span style="background:rgba(255,255,255,0.12); padding:4px 8px; border-radius:18px;">{role}</span>
            </div>
        </div>
    </div>
    """
    st.markdown(sidebar_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Menu navigasi — item yang sedang aktif diberi class .nav-active agar
    # ter-highlight melalui CSS, dan halaman detail (mis. detail_warga yang
    # dibuka dari menu "warga") tetap menyalakan menu induknya.
    DETAIL_PARENT = {"detail_warga": "warga", "detail_laporan": None}
    active_key = DETAIL_PARENT.get(current_page, current_page)
    if current_page == "detail_laporan":
        active_key = st.session_state.get("detail_laporan_back", "laporan")

    for icon, label, key in menus:
        is_active = (key == active_key)
        wrapper_class = "nav-active" if is_active else "nav-inactive"
        st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
        if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
            st.session_state["current_page"] = key
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


# ── Header bar dengan tombol Logout ───────────────────────────────────────────
def render_header_logout():
    user = get_user()
    col_info, col_btn = st.columns([7, 1])
    with col_info:
        st.markdown(
            f"""<div class="logout-bar">
                  <span style="font-size:0.88rem; color:#374151;">
                    👤 <b style="color:#1E3A8A;">{user.get('nama','')}</b>
                    &nbsp;·&nbsp; {user.get('role','')}
                  </span>
                  <span style="font-size:0.78rem; color:#9CA3AF;">e-RW 🏘️</span>
                </div>""",
            unsafe_allow_html=True,
        )
    with col_btn:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state["confirm_logout"] = True
            st.rerun()

    if st.session_state.get("confirm_logout"):
        st.warning("⚠️ Yakin ingin keluar dari akun ini?")
        c1, c2, c3 = st.columns([1, 1, 5])
        with c1:
            if st.button("✅ Ya, Keluar", type="primary"):
                logout()
        with c2:
            if st.button("❌ Batal"):
                st.session_state["confirm_logout"] = False
                st.rerun()


# ── Login page ─────────────────────────────────────────────────────────────────
def render_login():
    inject_css()
    st.markdown(
        """
        <div class="login-container">
          <div class="login-logo">
            <div class="icon">🏘️</div>
            <h1>e-RW</h1>
            <p>Sistem Layanan Masyarakat Rukun Warga</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col_l, col_c, col_r = st.columns([1, 1.6, 1])
    with col_c:
        st.markdown("#### 🔐 Masuk ke Akun Anda")
        email    = st.text_input("Email",    placeholder="email@erw.id",  key="login_email")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Masuk", use_container_width=True, type="primary"):
            u = USERS.get(email)
            if u and u["password"] == password:
                st.session_state["logged_in"]    = True
                st.session_state["user"]         = {**u, "email": email}
                st.session_state["current_page"] = "dashboard"
                st.rerun()
            else:
                st.error("Email atau password salah. Silakan coba lagi.")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="info-box">
              <b>Akun Demo:</b><br>
              🔵 Pengurus RW &nbsp;→ rw@erw.id / rw123<br>
              🟢 Pengurus RT &nbsp;→ rt@erw.id / rt123<br>
              🟠 Petugas &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ petugas@erw.id / petugas123<br>
              ⚪ Warga &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ warga@erw.id / warga123
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── Page router ────────────────────────────────────────────────────────────────
def render_page():
    page = st.session_state.get("current_page", "dashboard")
    role = get_user().get("role", "")

    if   page == "dashboard":                                 from pages import dashboard      as p; p.render()
    elif page == "warga"          and role == "Pengurus RW":  from pages import warga          as p; p.render()
    elif page == "validasi_warga" and role == "Pengurus RT":  from pages import validasi_warga as p; p.render()
    elif page == "kas":                                       from pages import kas            as p; p.render()
    elif page == "bansos":                                    from pages import bansos         as p; p.render()
    elif page == "pengumuman":                                from pages import pengumuman     as p; p.render()
    elif page == "kegiatan":                                  from pages import kegiatan       as p; p.render()
    elif page == "laporan":                                   from pages import laporan        as p; p.render()
    elif page == "tindak_lanjut":                             from pages import tindak_lanjut  as p; p.render()
    elif page == "profil":                                    from pages import profil         as p; p.render()
    elif page == "kirim_laporan":                             from pages import kirim_laporan  as p; p.render()
    elif page == "status_laporan":                            from pages import status_laporan as p; p.render()
    elif page == "status_kas":                                from pages import status_kas     as p; p.render()
    elif page == "status_bansos":                             from pages import status_bansos  as p; p.render()
    elif page == "detail_warga"   and role in ["Pengurus RW", "Pengurus RT"]:
                                                               from pages import detail_warga   as p; p.render()
    elif page == "detail_laporan":                            from pages import detail_laporan as p; p.render()
    else:                                                     from pages import dashboard      as p; p.render()


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    inject_css()
    if not is_logged_in():
        render_login()
    else:
        left_col, main_col = st.columns([1, 4])
        with left_col:
            render_sidebar()
        with main_col:
            render_header_logout()
            render_page()

if __name__ == "__main__":
    main()
    
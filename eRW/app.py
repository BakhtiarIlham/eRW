import streamlit as st

# ── Page config (must be first) ──────────────────────────────────────────────
st.set_page_config(
    page_title="e-RW | Sistem Layanan Warga",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Dummy accounts ────────────────────────────────────────────────────────────
USERS = {
    "rw@erw.id": {
        "password": "rw123",
        "role": "Pengurus RW",
        "nama": "Budi Santoso",
    },
    "rt@erw.id": {
        "password": "rt123",
        "role": "Pengurus RT",
        "nama": "Siti Rahayu",
    },
    "petugas@erw.id": {
        "password": "petugas123",
        "role": "Petugas Operasional",
        "nama": "Ahmad Fauzi",
    },
    "warga@erw.id": {
        "password": "warga123",
        "role": "Warga",
        "nama": "Dewi Lestari",
    },
}

# ── Global CSS ─────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown(
        """
        <style>
        /* ── Google Font ── */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* ── Base ── */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        .stApp {
            background: #F0F4FF;
        }

        /* ── Hide default Streamlit chrome ── */
        #MainMenu, footer, header { visibility: hidden; }
        .block-container { padding-top: 1rem; }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1E3A8A 0%, #1D4ED8 100%);
            border-right: none;
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

        /* ── Cards ── */
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
            width: 52px;
            height: 52px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
        }
        .metric-label { color: #6B7280; font-size: 0.82rem; font-weight: 500; }
        .metric-value { color: #111827; font-size: 1.6rem; font-weight: 700; line-height: 1; }

        /* ── Page title ── */
        .page-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1E3A8A;
            margin-bottom: 0.2rem;
        }
        .page-subtitle {
            color: #6B7280;
            font-size: 0.88rem;
            margin-bottom: 1.5rem;
        }

        /* ── Status badges ── */
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.76rem;
            font-weight: 600;
        }
        .badge-green  { background:#D1FAE5; color:#065F46; }
        .badge-yellow { background:#FEF3C7; color:#92400E; }
        .badge-blue   { background:#DBEAFE; color:#1E40AF; }
        .badge-red    { background:#FEE2E2; color:#991B1B; }
        .badge-gray   { background:#F3F4F6; color:#374151; }

        /* ── Table ── */
        .styled-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
        }
        .styled-table th {
            background: #EEF2FF;
            color: #1E3A8A;
            font-weight: 600;
            padding: 10px 14px;
            text-align: left;
            border-bottom: 2px solid #C7D2FE;
        }
        .styled-table td {
            padding: 9px 14px;
            border-bottom: 1px solid #F3F4F6;
            color: #374151;
        }
        .styled-table tr:hover td { background: #F9FAFB; }

        /* ── Primary button ── */
        .stButton > button {
            border-radius: 10px !important;
            font-weight: 500 !important;
            transition: all 0.2s !important;
        }
        div[data-testid="column"] .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #1D4ED8, #2563EB) !important;
            border: none !important;
            color: white !important;
        }

        /* ── Login page ── */
        .login-container {
            max-width: 420px;
            margin: 4vh auto 0;
            padding: 2.5rem;
            background: white;
            border-radius: 20px;
            box-shadow: 0 8px 40px rgba(30,58,138,0.12);
            border: 1px solid #E0E7FF;
        }
        .login-logo {
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .login-logo .icon { font-size: 3rem; }
        .login-logo h1 {
            color: #1E3A8A;
            font-size: 1.8rem;
            font-weight: 700;
            margin: 0.2rem 0 0;
        }
        .login-logo p {
            color: #6B7280;
            font-size: 0.85rem;
            margin: 0;
        }

        /* ── Info box ── */
        .info-box {
            background: #EFF6FF;
            border-left: 4px solid #3B82F6;
            border-radius: 8px;
            padding: 0.8rem 1rem;
            font-size: 0.83rem;
            color: #1E40AF;
            margin-bottom: 1rem;
        }

        /* ── Section header ── */
        .section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1rem;
        }
        .section-title {
            font-size: 1rem;
            font-weight: 600;
            color: #1E3A8A;
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
    for k in ["logged_in", "user", "current_page"]:
        st.session_state.pop(k, None)
    st.rerun()


# ── Sidebar navigation ─────────────────────────────────────────────────────────
MENUS = {
    "Pengurus RW": [
        ("🏠", "Dashboard",         "dashboard"),
        ("👥", "Kelola Warga",       "warga"),
        ("💰", "Kelola Kas",         "kas"),
        ("🎁", "Kelola Bansos",      "bansos"),
        ("📢", "Pengumuman",         "pengumuman"),
        ("📅", "Kegiatan",           "kegiatan"),
        ("📋", "Laporan",            "laporan"),
    ],
    "Pengurus RT": [
        ("🏠", "Dashboard",          "dashboard"),
        ("✅", "Validasi Warga",      "validasi_warga"),
        ("📢", "Pengumuman RT",       "pengumuman"),
        ("📅", "Kegiatan RT",         "kegiatan"),
        ("📋", "Kelola Laporan",      "laporan"),
    ],
    "Petugas Operasional": [
        ("🏠", "Dashboard",           "dashboard"),
        ("📋", "Lihat Laporan",       "laporan"),
        ("🔧", "Tindak Lanjut",       "tindak_lanjut"),
    ],
    "Warga": [
        ("🏠", "Dashboard",           "dashboard"),
        ("👤", "Data Pribadi",         "profil"),
        ("📢", "Pengumuman & Kegiatan","pengumuman"),
        ("📩", "Kirim Laporan",        "kirim_laporan"),
        ("📊", "Status Laporan",       "status_laporan"),
        ("💳", "Status Kas",           "status_kas"),
        ("🎁", "Status Bansos",        "status_bansos"),
    ],
}


def render_sidebar():
    user = get_user()
    role = user.get("role", "")
    menus = MENUS.get(role, [])

    with st.sidebar:
        # Logo
        st.markdown(
            """
            <div style="text-align:center; padding:1.2rem 0 1rem;">
              <div style="font-size:2rem;">🏘️</div>
              <div style="font-size:1.1rem; font-weight:700; color:white; margin-top:4px;">e-RW</div>
              <div style="font-size:0.72rem; color:#A5B4FC; margin-top:2px;">Sistem Layanan Warga</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div style="background:rgba(255,255,255,0.1); border-radius:12px;
                        padding:0.75rem 1rem; margin-bottom:1rem;">
              <div style="font-size:0.82rem; color:#C7D2FE;">Selamat datang,</div>
              <div style="font-weight:600; font-size:0.95rem; color:white;">{user.get('nama','')}</div>
              <div style="font-size:0.74rem; color:#93C5FD; margin-top:2px;">
                <span style="background:rgba(255,255,255,0.15); padding:2px 8px;
                             border-radius:20px;">{role}</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("---")
        for icon, label, key in menus:
            if st.button(f"{icon}  {label}", key=f"nav_{key}"):
                st.session_state["current_page"] = key
                st.rerun()
        st.markdown("---")
        if st.button("🚪  Logout"):
            logout()


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

    # Center the form
    col_l, col_c, col_r = st.columns([1, 1.6, 1])
    with col_c:
        with st.container():
            st.markdown("#### 🔐 Masuk ke Akun Anda")
            email = st.text_input("Email", placeholder="email@erw.id", key="login_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Masuk", use_container_width=True, type="primary"):
                u = USERS.get(email)
                if u and u["password"] == password:
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = {**u, "email": email}
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

    if page == "dashboard":
        from pages import dashboard as p; p.render()
    elif page == "warga" and role == "Pengurus RW":
        from pages import warga as p; p.render()
    elif page == "validasi_warga" and role == "Pengurus RT":
        from pages import validasi_warga as p; p.render()
    elif page == "kas":
        from pages import kas as p; p.render()
    elif page == "bansos":
        from pages import bansos as p; p.render()
    elif page == "pengumuman":
        from pages import pengumuman as p; p.render()
    elif page == "kegiatan":
        from pages import kegiatan as p; p.render()
    elif page == "laporan":
        from pages import laporan as p; p.render()
    elif page == "tindak_lanjut":
        from pages import tindak_lanjut as p; p.render()
    elif page == "profil":
        from pages import profil as p; p.render()
    elif page == "kirim_laporan":
        from pages import kirim_laporan as p; p.render()
    elif page == "status_laporan":
        from pages import status_laporan as p; p.render()
    elif page == "status_kas":
        from pages import status_kas as p; p.render()
    elif page == "status_bansos":
        from pages import status_bansos as p; p.render()
    else:
        from pages import dashboard as p; p.render()


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    inject_css()
    if not is_logged_in():
        render_login()
    else:
        render_sidebar()
        render_page()


if __name__ == "__main__":
    main()

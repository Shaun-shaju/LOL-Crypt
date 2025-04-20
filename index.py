import streamlit as st
from services.firebase_options import db
from services.passwords import create_user, validate_user

st.set_page_config(page_title="LOL Crypt Access Node", page_icon="😂", layout="centered", menu_items={})

# 🧠 Session init
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None
if "page" not in st.session_state:
    st.session_state.page = "welcome"

# 🔐 Auth page logic
def authenticate():
    hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] {
            display: none !important;
        }
        [data-testid="collapsedControl"] {
            display: none !important;
        }
    </style>
"""
    st.markdown(hide_sidebar_style, unsafe_allow_html=True)
    st.title("🔐 LOL Crypt Access Node")
    st.markdown("------")
    st.title("🧑 Identity Verification Portal")

    with st.expander("🔧 Select Protocol Mode"):
        auth_mode = st.selectbox("Operation Mode", ["Access Node (Login)", "Deploy Credentials (Sign Up)"])

    username = st.text_input("Agent Handle")
    password = st.text_input("Access Phrase", type="password")

    if auth_mode == "Deploy Credentials (Sign Up)":
        name = st.text_input("Codename")
        age = st.number_input("Unit Age", min_value=15, max_value=120)

        if st.button("Initialize Identity Record"):
            if create_user(username, password, name, age):
                st.success("Identity record deployed! Proceed to access node. 🎉")
            else:
                st.error("Handle already exists in system 🔒")

    else:
        if st.button("Engage Access Node"):
            if validate_user(username, password):
                st.success("Verification complete. 🔓")
                st.session_state["authenticated"] = True
                st.session_state["user"] = username
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Access Denied ❌ Verify credentials.")

# 🌐 Pages (load only when logged in)
pages = {
    "Account": [
        st.Page("pages/home.py", title="Command Hub", icon="🗄️"),
        st.Page("pages/profile.py", title="Profile Settings", icon="👤"),
    ],
    "Apps": [
        st.Page("pages/friend.py", title="Target Link Scan", icon="📡"),
        st.Page("pages/chat.py", title="Execute PeerComm", icon="⚡"),
    ],
}

# ✅ Logic flow
if st.session_state["authenticated"]:
    pg = st.navigation(pages)
    st.sidebar.write(f"🛰️ Active Node Identifier ID: `{st.session_state['user']}`")
    if st.sidebar.button("🛑 Terminate Session"):
        st.session_state["authenticated"] = False
        st.session_state["user"] = None
        st.session_state.page = "welcome"
        st.rerun()
    pg.run()
else:
    authenticate()

import streamlit as st
from services.firebase_options import db

# 📩 Deploy Connection Signal
def send_friend_request(to_user):
    current_user = st.session_state['user']
    to_user_ref = db.collection("users").document(to_user)

    if not to_user_ref.get().exists:
        st.error("⚠️ Identity Node not located.")
        return False

    # 🚫 Already linked?
    if db.collection("users").document(current_user).collection("friends").document(to_user).get().exists:
        st.warning("🎯 Target already linked to your network 💕")
        return False

    if to_user_ref.collection("friend_requests").document(current_user).get().exists:
        st.warning("📡 Connection signal already transmitted 😅")
        return False

    # ✨ Send signal
    to_user_ref.collection("friend_requests").document(current_user).set({"status": "pending"})
    return True

# ✅ Accept Signal
def accept_friend_request(from_user):
    current_user = st.session_state['user']
    current_ref = db.collection("users").document(current_user)
    from_ref = db.collection("users").document(from_user)

    # 🔗 Link networks
    current_ref.collection("friends").document(from_user).set({"status": "friend"})
    from_ref.collection("friends").document(current_user).set({"status": "friend"})

    # ❌ Remove pending signal
    current_ref.collection("friend_requests").document(from_user).delete()
    return True

# ❌ Deny Signal
def reject_friend_request(from_user):
    current_user = st.session_state['user']
    current_ref = db.collection("users").document(current_user)
    current_ref.collection("friend_requests").document(from_user).delete()
    return True

# 🛸 SusNet Interface
def add_friend_screen():
    st.title("🤝 Link Requests Dashboard")

    if "user" not in st.session_state:
        st.error("🔐 Log in to connect with agents.")
        return

    current_user = st.session_state["user"]

    tab1, tab2 = st.tabs(["🔍 Deploy Signal", "📨 Incoming Signals"])

    # 🔍 Seek & Connect
    with tab1:
        friend_username = st.text_input("🔎 Locate target identity...")
        if friend_username and st.button("📡 Transmit Friend Signal"):
            if send_friend_request(friend_username):
                st.success(f"💌 Signal successfully sent to `{friend_username}`!")

    # 📥 Incoming signals
    with tab2:
        st.subheader("⚠️ Pending Incoming Signals")
        requests = db.collection("users").document(current_user).collection("friend_requests").stream()
        has_requests = False
        for req in requests:
            from_user = req.id
            has_requests = True
            with st.container():
                st.write(f"📡 Incoming link request from `{from_user}`")
                col1, col2 = st.columns(2)
                if col1.button(f"✅ Accept `{from_user}`", key=f"accept_{from_user}"):
                    accept_friend_request(from_user)
                    st.success(f"🌐 You are now connected with `{from_user}`!")
                    st.rerun()
                if col2.button(f"❌ Reject `{from_user}`", key=f"reject_{from_user}"):
                    reject_friend_request(from_user)
                    st.info(f"🛑 Signal from `{from_user}` declined.")
                    st.rerun()
        if not has_requests:
            st.write("💤 No incoming signals detected.")

    # 🧾 Current Link Directory
    st.subheader("📖 Connected Nodes")
    friends_ref = db.collection("users").document(current_user).collection("friends").stream()
    friends_list = [f.id for f in friends_ref]

    if friends_list:
        for f in friends_list:
            st.write(f"💘 Connected to: `{f}`")
    else:
        st.write("🌌 Empty link list... deploy some signals!")

# Run the screen when script is executed
if __name__ == "__main__":
    add_friend_screen()

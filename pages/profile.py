import streamlit as st
import bcrypt
from services.firebase_options import db

# 👀 Sneaky check if the username is out there
def check_username_exists(username):
    user_ref = db.collection("users").where("username", "==", username).get()
    return len(user_ref) > 0

# 🕵️‍♀️ Dig up user data if the vibes match
def get_user_data(username, password):
    user_ref = db.collection("users").where("username", "==", username).get()
    if not user_ref:
        return None

    user = user_ref[0].to_dict()
    stored_password = user["password"]
    if bcrypt.checkpw(password.encode("utf-8"), stored_password):
        return user
    return None

# 🔐 Encrypting the sauce (aka password)
def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

# 💻 Top Secret Profile Lounge
st.subheader("🕶️ Secret Agent Profile Panel")

username_input = st.text_input("Agent codename (username) 🕵️")
password_input = st.text_input("Whisper the passphrase...", type="password")

if st.button("Enter the Den"):
    data = get_user_data(username_input, password_input)
    if data:
        st.session_state["user"] = data["username"]
        st.session_state["password"] = password_input
        st.session_state["authenticated"] = True
        st.success("Access confirmed. Gate to your secrets unlocked! 🗝️")
    else:
        st.session_state["authenticated"] = False
        st.error("Identity mismatch! You shall not pass 🚫")

# Only step inside if you're verified and not an imposter 👻
if st.session_state.get("authenticated") and st.session_state.get("user") == username_input:
    data = get_user_data(st.session_state["user"], st.session_state["password"])
    if data:
        name = st.text_input("Alias (Full Name)", value=data.get("name", ""))
        age = st.number_input("Your age in Earth years 🌍", min_value=15, max_value=120, value=data.get("age", 15))

        st.subheader("🔐 Password Recalibration")
        old_password = st.text_input("Old Codeword", type="password")
        new_password = st.text_input("New Top Secret Pass", type="password")
        confirm_password = st.text_input("Repeat the New Codeword", type="password")

        if st.button("Update Credentials"):
            if bcrypt.checkpw(old_password.encode("utf-8"), data["password"]):
                if new_password == confirm_password:
                    hashed_new = hash_password(new_password)
                    db.collection("users").document(st.session_state["user"]).update({"password": hashed_new})
                    st.success("🔓 Passcode changed. You're a certified ninja now!")
                else:
                    st.error("Oops! The two new codewords don't match. Check again! 🙈")
            else:
                st.error("Nope, that old passcode ain't right 😬")

        if st.button("Save Alter Ego"):
            db.collection("users").document(st.session_state["user"]).update({
                "name": name,
                "age": age
            })
            st.success("Details secured in the vault 💾✨")
else:
    st.warning("🚷 Unauthorized! You gotta log in to unlock the vault 💼")
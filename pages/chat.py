import streamlit as st
import time
from datetime import datetime
from services.firebase_options import db

# --- Utility Functions ---

def encrypt_message_to_emojis(message, base_emoji, jump):
    base_unicode = ord(base_emoji)
    return ''.join(chr(base_unicode + (ord(c) * jump) % 1000) for c in message)

def decrypt_emojis_to_message(emoji_msg, base_emoji, jump):
    base_unicode = ord(base_emoji)
    return ''.join(chr(((ord(e) - base_unicode) // jump) % 256) for e in emoji_msg)

# --- Firebase Chat Logic ---

def get_friends(username):
    friends_ref = db.collection("users").document(username).collection("friends").stream()
    return [friend.id for friend in friends_ref]

def get_or_create_chatroom(user1, user2):
    user1_ref = db.collection("users").document(user1).collection("chats").document(user2)
    doc = user1_ref.get()
    if doc.exists:
        return doc.to_dict()["chatroom_id"]
    chatroom_id = f"{user1}_{user2}_{int(time.time()*1000)}"
    db.collection("users").document(user1).collection("chats").document(user2).set({"chatroom_id": chatroom_id})
    db.collection("users").document(user2).collection("chats").document(user1).set({"chatroom_id": chatroom_id})
    db.collection("chats").document(chatroom_id).set({"user1": user1, "user2": user2})
    return chatroom_id

def send_message(chatroom_id, sender, encrypted_msg):
    timestamp = int(time.time() * 1000)
    db.collection("chats").document(chatroom_id).collection("chats").document(str(timestamp)).set({
        "sender": sender,
        "message": encrypted_msg
    })

def get_messages(chatroom_id):
    messages_ref = db.collection("chats").document(chatroom_id).collection("chats").order_by("__name__").stream()
    messages = []
    for msg in messages_ref:
        data = msg.to_dict()
        messages.append((data["sender"], data["message"]))
    return messages

def is_first_time_chat(chatroom_id):
    chat_ref = db.collection("chats").document(chatroom_id).collection("chats")
    messages = list(chat_ref.limit(1).stream())
    return len(messages) == 0

# --- Main UI ---

if "user" not in st.session_state:
    st.error("🔒 Entry Denied. Node access requires authentication.")
    st.stop()

current_user = st.session_state["user"]
st.title("🧬 CipherComm Console")

# Select friend
friends = get_friends(current_user)
if not friends:
    st.warning("🧭 No linked nodes found. Please establish target connections first.")
    st.stop()
friend_selected = st.selectbox("🎯 Choose Target Comm Node:", friends)

# Emoji encryption settings
base_emoji = st.text_input("📍 Glyph Anchor Emoji", value="😀")
jump = st.slider("⚙️ Encryption Flux Multiplier", 1, 50, 1)

# Displaying a small disappearing suspicious banner
banner = st.empty()  # Create an empty container for the banner
banner.markdown(
    """
    <style>
        .disappearing-banner {
            background-color: #f9d342;
            color: #333;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
            text-align: center;
        }
    </style>
    <div class="disappearing-banner">
        Chat may flicker, but the message will send. Proceed with caution.
    </div>
    """, unsafe_allow_html=True
)

# Wait for 3 seconds and then remove the banner
time.sleep(3)
banner.empty()

if friend_selected:
    chatroom_id = get_or_create_chatroom(current_user, friend_selected)
    first_time = is_first_time_chat(chatroom_id)
    messages = get_messages(chatroom_id)

    if first_time:
        st.info(f"👾 First contact with node `{friend_selected}` established. Initiate Comm Protocol.")

    st.markdown("---")
    st.subheader(f"🛰️ CipherComm Stream: {friend_selected}")

    raw_messages = []

    for sender, enc_msg in messages:
        decrypted = decrypt_emojis_to_message(enc_msg, base_emoji, jump)
        is_user = sender == current_user
        with st.chat_message("user" if is_user else "assistant"):
            st.markdown(decrypted)
        raw_messages.append(f"{sender}: {enc_msg}")

    # Handle new message
    new_msg = st.chat_input("💭 Transmit New Glyph Transmission...")
    if new_msg:
        encrypted_msg = encrypt_message_to_emojis(new_msg, base_emoji, jump)
        send_message(chatroom_id, current_user, encrypted_msg)

        # Update session timestamp and prevent immediate rerun after sending
        st.session_state['last_message_time'] = time.time()

        # Prevent rerun while typing
        st.rerun()

    st.markdown("---")
    st.subheader("📦 Intercepted Cipher Payloads")
    st.code(raw_messages[-1], language="text")

# --- Auto-refresh mechanism ---
# Only refresh if no message was sent in the last second
if "last_message_time" in st.session_state:
    if time.time() - st.session_state['last_message_time'] > 1:
        st.rerun()

# 🕵️‍♂️ LOL-Crypt

> "Definitely *not* your everyday chat app. 👀"

LOL-Crypt is a suspiciously secure, emoji-based encrypted chat system built using Streamlit and Firebase. Messages are sent as emoji sequences and decrypted only on the client side. No raw messages are ever stored. Just vibes. 😎

---

## 🚀 Features

- 🔐 Encrypted emoji messages with custom base emoji & jump logic
- 🔄 Real-time chat with Firestore integration
- 🤫 Secret chatroom IDs created per user pairing
- 🧠 Decryption only on receiver side (client-based only)
- 🧍‍♂️ Friend selector (from Firestore's friends subcollection)
- 🐸 Totally normal. Absolutely no government surveillance here. Trust us.

---

## 🔧 Setup Instructions

1. Clone this super normal repo:

```bash
git clone https://github.com/Shaun-shaju/LOL-Crypt.git
cd LOL-Crypt
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Add a `.streamlit/secrets.toml` file:

```toml
[firestore]
type = "service_account"
project_id = "l0lcrypt"
private_key_id = "<your-key-id>"
private_key = "<your-private-key>"
client_email = "<your-client-email>"
client_id = "<your-client-id>"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "<your-cert-url>"
```

4. Run the app:

```bash
streamlit run main.py
```

---

## ⚙️ Tech Stack

- 🐍 Python 3
- 📦 Streamlit
- 🔥 Firebase (Firestore)
- 🧂 bcrypt (for password hashing)

---

## 🛠️ Dev Notes

- The emoji encryption is a ✨custom algorithm✨ based on ASCII shifts
- No messages are saved in plaintext — only encrypted emoji gibberish
- This is definitely not a front for secret communication

---

## 🚀 Try LOL Crypt  
Click below to experience the text encryption work live:  

[![Run on Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://lol-crypt.streamlit.app/)

## 🧙‍♂️ Author

Built with love, paranoia, and caffeine by [Shaun](https://github.com/Shaun-shaju) ☕💀

> "If it looks sus, that's because it *is* sus."

---

## 📌 Disclaimer

This is project is meant for fun & educational purposes. Use at your own risk. And always double-check your emojis before sending. 🧐


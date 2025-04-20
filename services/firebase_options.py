import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# Initialize Firebase only if not already initialized
if not firebase_admin._apps:
    # Get credentials from Streamlit secrets
    creds = credentials.Certificate({
        "type": st.secrets["firestore"]["type"],
        "project_id": st.secrets["firestore"]["project_id"],
        "private_key_id": st.secrets["firestore"]["private_key_id"],
        "private_key": st.secrets["firestore"]["private_key"].replace("\\n", "\n"),  # Ensure newline characters are handled
        "client_email": st.secrets["firestore"]["client_email"],
        "client_id": st.secrets["firestore"]["client_id"],
        "auth_uri": st.secrets["firestore"]["auth_uri"],
        "token_uri": st.secrets["firestore"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["firestore"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["firestore"]["client_x509_cert_url"]
    })
    firebase_admin.initialize_app(creds)

# Get Firestore client
db = firestore.client()

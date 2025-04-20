from services.firebase_options import db
import bcrypt

# Function to check if the username exists
def check_username_exists(username):
    user_ref = db.collection("users").where("username", "==", username).get()
    return len(user_ref) > 0

# Function to add user to Firestore with hashed password
def create_user(username, password, name, age):
    if check_username_exists(username):
        return False  # Username already exists
    
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    db.collection("users").document(username).set({
        "username": username,
        "password": hashed_password,
        "name": name,
        "age": age,
    })
    return True

# Function to validate login credentials
def validate_user(username, password):
    user_ref = db.collection("users").where("username", "==", username).get()
    
    if len(user_ref) == 0:
        return False  # No such user
    
    user = user_ref[0].to_dict()
    stored_password = user["password"]
    
    # Check if password matches
    if bcrypt.checkpw(password.encode("utf-8"), stored_password):
        return True
    return False
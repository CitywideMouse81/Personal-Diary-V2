import bcrypt
import pwinput
from storage import user_exists, save_user, load_users

def register_user():
    """
    Registers a new user by taking a username and visible password input.
    """
    username = input("Choose a username: ")
    if user_exists(username):
        print("⚠️ Username already exists.")
        return

    while True:
        password = input("Create a password (visible): ")
        if len(password) >= 8:
            break
        print("⚠️ Password too short. Must be at least 8 characters.")

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    save_user(username, hashed)
    print("✅ Registration successful!")

def login_user():
    """
    Logs in a user with masked password input using asterisks.
    """
    username = input("Username: ")
    password = pwinput.pwinput("Password: ", mask="*")
    users = load_users()

    if username in users and bcrypt.checkpw(password.encode(), users[username].encode()):
        print(f"✅ Welcome back, {username}!")
        return username
    else:
        print("❌ Login failed. Invalid credentials.")
        return None

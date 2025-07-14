import json
import os

USER_FILE = 'users.txt'
DIARY_FILE = 'diary_entries.json'

def load_users():
    try:
        users = {}
        with open(USER_FILE, 'r') as f:
            for line in f:
                username, hash_pw = line.strip().split(':')
                users[username] = hash_pw
        return users
    except FileNotFoundError:
        return {}

def save_user(username, hashed_password):
    with open(USER_FILE, 'a') as f:
        f.write(f"{username}:{hashed_password.decode()}\n")

def user_exists(username):
    users = load_users()
    return username in users

def load_entries():
    try:
        with open(DIARY_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_entries(entries):
    with open(DIARY_FILE, 'w') as f:
        json.dump(entries, f, indent=4)

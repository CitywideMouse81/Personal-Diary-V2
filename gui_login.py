from tkinter import *
from tkinter import messagebox
import bcrypt
import os
import json
from datetime import datetime

USERS_FILE = "users.txt"
ENTRIES_FILE = "diary_entries.json"

# ------------- Auth Functions -------------
def register_user_to_file(username, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    with open(USERS_FILE, 'a') as f:
        f.write(f"{username}:{hashed_password.decode()}\n")

def user_exists(username):
    if not os.path.exists(USERS_FILE):
        return False
    with open(USERS_FILE, 'r') as f:
        return any(line.split(':')[0] == username for line in f)

def verify_login(username, password):
    if not os.path.exists(USERS_FILE):
        return False
    with open(USERS_FILE, 'r') as f:
        for line in f:
            stored_username, stored_hash = line.strip().split(':')
            if stored_username == username:
                return bcrypt.checkpw(password.encode(), stored_hash.encode())
    return False

# ------------- UI Windows -------------
def show_welcome():
    clear_window()
    Label(root, text="\U0001F4D3 Welcome to Personal Diary App", font=("Helvetica", 18, "bold"), bg="#e0f7fa").pack(pady=30)
    Button(root, text="Login", width=20, font=("Helvetica", 12), bg="#00bcd4", fg="white", relief="flat", command=show_login).pack(pady=10)
    Button(root, text="Register", width=20, font=("Helvetica", 12), bg="#4db6ac", fg="white", relief="flat", command=show_register).pack(pady=10)
    Button(root, text="Exit", width=20, font=("Helvetica", 12), bg="#f44336", fg="white", relief="flat", command=root.quit).pack(pady=10)

def show_login():
    clear_window()
    Label(root, text="\U0001F510 Login", font=("Helvetica", 16, "bold"), bg="#e8f5e9").pack(pady=20)
    frame = Frame(root, bg="#e8f5e9")
    frame.pack(pady=10)

    Label(frame, text="Username:", font=("Helvetica", 12), bg="#e8f5e9").grid(row=0, column=0, sticky=E, pady=5)
    username_entry = Entry(frame, width=30)
    username_entry.grid(row=0, column=1)

    Label(frame, text="Password:", font=("Helvetica", 12), bg="#e8f5e9").grid(row=1, column=0, sticky=E, pady=5)
    password_entry = Entry(frame, width=30, show="*")
    password_entry.grid(row=1, column=1)

    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        if verify_login(username, password):
            messagebox.showinfo("Success", f"Welcome, {username}!")
            show_dashboard(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    Button(root, text="Login", command=handle_login, font=("Helvetica", 12), width=20, bg="#4caf50", fg="white", relief="flat").pack(pady=5)
    Button(root, text="\u2190 Back", command=show_welcome, font=("Helvetica", 12), width=20, bg="#9e9e9e", fg="white", relief="flat").pack(pady=5)

def show_register():
    clear_window()
    Label(root, text="\U0001F4DD Register", font=("Helvetica", 16, "bold"), bg="#fff3e0").pack(pady=20)
    frame = Frame(root, bg="#fff3e0")
    frame.pack(pady=10)

    Label(frame, text="Username:", font=("Helvetica", 12), bg="#fff3e0").grid(row=0, column=0, sticky=E, pady=5)
    username_entry = Entry(frame, width=30)
    username_entry.grid(row=0, column=1)

    Label(frame, text="Password:", font=("Helvetica", 12), bg="#fff3e0").grid(row=1, column=0, sticky=E, pady=5)
    password_entry = Entry(frame, width=30)  # visible password
    password_entry.grid(row=1, column=1)

    def handle_register():
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        if user_exists(username):
            messagebox.showerror("Error", "Username already exists.")
            return
        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters.")
            return
        register_user_to_file(username, password)
        messagebox.showinfo("Success", "Registration successful!")
        show_login()

    Button(root, text="Register", command=handle_register, font=("Helvetica", 12), width=20, bg="#ff9800", fg="white", relief="flat").pack(pady=5)
    Button(root, text="\u2190 Back", command=show_welcome, font=("Helvetica", 12), width=20, bg="#9e9e9e", fg="white", relief="flat").pack(pady=5)

# ------------- Dashboard -------------
def show_dashboard(username):
    clear_window()
    Label(root, text=f"\U0001F44B Welcome, {username}!", font=("Helvetica", 16, "bold"), bg="#e3f2fd").pack(pady=20)
    Button(root, text="\U0001F4DD Create New Entry", width=25, font=("Helvetica", 12), bg="#4caf50", fg="white", relief="flat", command=lambda: create_entry_ui(username)).pack(pady=5)
    Button(root, text="\U0001F4D6 View All Entries", width=25, font=("Helvetica", 12), bg="#2196f3", fg="white", relief="flat", command=lambda: view_entries_ui(username)).pack(pady=5)
    Button(root, text="\U0001F50D Search Entries", width=25, font=("Helvetica", 12), bg="#ff9800", fg="white", relief="flat", command=lambda: search_entries_ui(username)).pack(pady=5)
    Button(root, text="\U0001F5D1️ Delete Entry", width=25, font=("Helvetica", 12), bg="#f44336", fg="white", relief="flat", command=lambda: delete_entry_ui(username)).pack(pady=5)
    Button(root, text="\U0001F6AA Logout", width=25, font=("Helvetica", 12), bg="#607d8b", fg="white", relief="flat", command=show_welcome).pack(pady=20)

# ------------- Diary Functionality -------------
def create_entry_ui(username):
    clear_window()
    Label(root, text="\U0001F4DD New Diary Entry", font=("Helvetica", 16, "bold"), bg="#f3e5f5").pack(pady=10)
    frame = Frame(root, bg="#f3e5f5")
    frame.pack(pady=5)

    Label(frame, text="Title:", font=("Helvetica", 12), bg="#f3e5f5").grid(row=0, column=0, sticky=E)
    title_entry = Entry(frame, width=40)
    title_entry.grid(row=0, column=1, pady=5)

    Label(frame, text="Category:", font=("Helvetica", 12), bg="#f3e5f5").grid(row=1, column=0, sticky=E)
    category_entry = Entry(frame, width=40)
    category_entry.grid(row=1, column=1, pady=5)

    Label(frame, text="Content:", font=("Helvetica", 12), bg="#f3e5f5").grid(row=2, column=0, sticky=NE)
    content_text = Text(frame, height=10, width=30)
    content_text.grid(row=2, column=1, pady=5)

    def save_entry():
        title = title_entry.get()
        category = category_entry.get()
        content = content_text.get("1.0", END).strip()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not title or not content:
            messagebox.showerror("Error", "Title and Content are required.")
            return

        entry = {
            "title": title,
            "category": category or "Uncategorized",
            "content": content,
            "timestamp": timestamp,
            "author": username
        }

        try:
            if os.path.exists(ENTRIES_FILE):
                with open(ENTRIES_FILE, "r") as f:
                    data = json.load(f)
            else:
                data = []

            data.append(entry)
            with open(ENTRIES_FILE, "w") as f:
                json.dump(data, f, indent=4)
            messagebox.showinfo("Success", "Entry saved successfully.")
            show_dashboard(username)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save entry: {str(e)}")

    Button(root, text="Save Entry", command=save_entry, font=("Helvetica", 12), width=20, bg="#4caf50", fg="white", relief="flat").pack(pady=10)
    Button(root, text="\u2190 Back", command=lambda: show_dashboard(username), font=("Helvetica", 12), width=20, bg="#9e9e9e", fg="white", relief="flat").pack()

def view_entries_ui(username):
    clear_window()
    Label(root, text="\U0001F4D6 Your Diary Entries", font=("Helvetica", 16, "bold"), bg="#e1f5fe").pack(pady=10)
    frame = Frame(root, bg="#e1f5fe")
    frame.pack(pady=5)

    try:
        with open(ENTRIES_FILE, "r") as f:
            entries = json.load(f)
    except:
        entries = []

    user_entries = [e for e in entries if e["author"] == username]
    if not user_entries:
        Label(frame, text="No entries found.", font=("Helvetica", 12), bg="#e1f5fe").pack()
    else:
        for e in user_entries:
            Label(frame, text=f"Title: {e['title']}\nDate: {e['timestamp']}\nCategory: {e['category']}\nContent: {e['content']}\n", justify=LEFT, font=("Helvetica", 11), bg="#e1f5fe", anchor=W, wraplength=360).pack(pady=5)

    Button(root, text="\u2190 Back", command=lambda: show_dashboard(username), font=("Helvetica", 12), width=20, bg="#9e9e9e", fg="white", relief="flat").pack(pady=10)

def delete_entry_ui(username):
    clear_window()
    Label(root, text="\U0001F5D1️ Delete Diary Entry", font=("Helvetica", 16, "bold"), bg="#ffebee").pack(pady=10)
    frame = Frame(root, bg="#ffebee")
    frame.pack(pady=5)

    try:
        with open(ENTRIES_FILE, "r") as f:
            entries = json.load(f)
    except:
        entries = []

    user_entries = [e for e in entries if e["author"] == username]
    if not user_entries:
        Label(frame, text="No entries to delete.", font=("Helvetica", 12), bg="#ffebee").pack()
    else:
        var = StringVar(value="")
        for idx, e in enumerate(user_entries):
            entry_str = f"{e['title']} ({e['timestamp']})"
            Radiobutton(frame, text=entry_str, variable=var, value=str(idx), font=("Helvetica", 11), bg="#ffebee", anchor=W, wraplength=360).pack(anchor=W)

        def delete_selected():
            sel = var.get()
            if sel == "":
                messagebox.showerror("Error", "Please select an entry to delete.")
                return
            idx = int(sel)
            entry_to_delete = user_entries[idx]
            entries.remove(entry_to_delete)
            with open(ENTRIES_FILE, "w") as f:
                json.dump(entries, f, indent=4)
            messagebox.showinfo("Deleted", "Entry deleted successfully.")
            show_dashboard(username)

        Button(root, text="Delete Selected Entry", command=delete_selected, font=("Helvetica", 12), width=25, bg="#f44336", fg="white", relief="flat").pack(pady=10)

    Button(root, text="\u2190 Back", command=lambda: show_dashboard(username), font=("Helvetica", 12), width=20, bg="#9e9e9e", fg="white", relief="flat").pack(pady=10)

def search_entries_ui(username):
    clear_window()
    Label(root, text="\U0001F50D Search Diary Entries", font=("Helvetica", 16, "bold"), bg="#fffde7").pack(pady=10)
    frame = Frame(root, bg="#fffde7")
    frame.pack(pady=5)

    Label(frame, text="Search by Title or Category:", font=("Helvetica", 12), bg="#fffde7").grid(row=0, column=0, sticky=E)
    search_entry = Entry(frame, width=30)
    search_entry.grid(row=0, column=1, pady=5)

    result_frame = Frame(root, bg="#fffde7")
    result_frame.pack(pady=10)

    def perform_search():
        query = search_entry.get().lower()
        for widget in result_frame.winfo_children():
            widget.destroy()
        try:
            with open(ENTRIES_FILE, "r") as f:
                entries = json.load(f)
        except:
            entries = []
        user_entries = [e for e in entries if e["author"] == username]
        filtered = [e for e in user_entries if query in e["title"].lower() or query in e["category"].lower()]
        if not filtered:
            Label(result_frame, text="No matching entries found.", font=("Helvetica", 12), bg="#fffde7").pack()
        else:
            for e in filtered:
                Label(result_frame, text=f"Title: {e['title']}\nDate: {e['timestamp']}\nCategory: {e['category']}\nContent: {e['content']}\n", justify=LEFT, font=("Helvetica", 11), bg="#fffde7", anchor=W, wraplength=360).pack(pady=5)

    Button(frame, text="Search", command=perform_search, font=("Helvetica", 12), width=15, bg="#ff9800", fg="white", relief="flat").grid(row=1, column=0, columnspan=2, pady=5)
    Button(root, text="\u2190 Back", command=lambda: show_dashboard(username), font=("Helvetica", 12), width=20, bg="#9e9e9e", fg="white", relief="flat").pack(pady=10)

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# ------------- Run App -------------
root = Tk()
root.title("Diary App")
root.geometry("440x550")
root.resizable(False, False)
root.configure(bg="#e0f7fa")

show_welcome()
root.mainloop()
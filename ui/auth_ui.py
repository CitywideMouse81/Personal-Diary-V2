from tkinter import *
from tkinter import messagebox
from auth import verify_login, register_user
from ui.dashboard_ui import show_dashboard_screen
from ui.common import clear_window

def show_welcome_screen(root):
    clear_window(root)
    Label(root, text="📓 Welcome to Personal Diary App", font=("Helvetica", 18, "bold"), bg="#e0f7fa").pack(pady=30)
    Button(root, text="Login", width=20, font=("Helvetica", 12), bg="#00bcd4", fg="white",
           command=lambda: show_login_screen(root)).pack(pady=10)
    Button(root, text="Register", width=20, font=("Helvetica", 12), bg="#4db6ac", fg="white",
           command=lambda: show_register_screen(root)).pack(pady=10)
    Button(root, text="Exit", width=20, font=("Helvetica", 12), bg="#f44336", fg="white",
           command=root.quit).pack(pady=10)

def show_login_screen(root):
    clear_window(root)
    Label(root, text="🔐 Login", font=("Helvetica", 16, "bold"), bg="#e8f5e9").pack(pady=20)
    frame = Frame(root, bg="#e8f5e9")
    frame.pack(pady=10)

    Label(frame, text="Username:", font=("Helvetica", 12), bg="#e8f5e9").grid(row=0, column=0, sticky=E)
    username_entry = Entry(frame, width=30)
    username_entry.grid(row=0, column=1)

    Label(frame, text="Password:", font=("Helvetica", 12), bg="#e8f5e9").grid(row=1, column=0, sticky=E)
    password_entry = Entry(frame, width=30, show="*")
    password_entry.grid(row=1, column=1)

    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        if verify_login(username, password):
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            show_dashboard_screen(root, username)
        else:
            messagebox.showerror("Error", "Invalid credentials")

    Button(root, text="Login", command=handle_login, font=("Helvetica", 12), width=20, bg="#4caf50", fg="white").pack(pady=5)
    Button(root, text="← Back", command=lambda: show_welcome_screen(root), font=("Helvetica", 12), width=20, bg="#9e9e9e", fg="white").pack(pady=5)

def show_register_screen(root):
    clear_window(root)
    Label(root, text="📝 Register", font=("Helvetica", 16, "bold"), bg="#fff3e0").pack(pady=20)
    frame = Frame(root, bg="#fff3e0")
    frame.pack(pady=10)

    Label(frame, text="Username:", font=("Helvetica", 12), bg="#fff3e0").grid(row=0, column=0, sticky=E)
    username_entry = Entry(frame, width=30)
    username_entry.grid(row=0, column=1)

    Label(frame, text="Password:", font=("Helvetica", 12), bg="#fff3e0").grid(row=1, column=0, sticky=E)
    password_entry = Entry(frame, width=30)
    password_entry.grid(row=1, column=1)

    def handle_register():
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return
        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters.")
            return
        register_user(username, password)
        messagebox.showinfo("Success", "Registration successful!")
        show_login_screen(root)

    Button(root, text="Register", command=handle_register, font=("Helvetica", 12), width=20, bg="#ff9800", fg="white").pack(pady=5)
    Button(root, text="← Back", command=lambda: show_welcome_screen(root), font=("Helvetica", 12), width=20, bg="#9e9e9e", fg="white").pack(pady=5)

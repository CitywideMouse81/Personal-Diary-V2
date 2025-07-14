from tkinter import *
from tkinter import messagebox
from datetime import datetime
import json
import os

from entries import save_entry, load_entries
from ui.common import clear_window
from ui.auth_ui import show_welcome_screen

ENTRIES_FILE = "diary_entries.json"

def show_dashboard_screen(root, username):
    clear_window(root)
    root.configure(bg="#e3f2fd")
    Label(root, text=f"👋 Welcome, {username}!", font=("Helvetica", 16, "bold"), bg="#e3f2fd").pack(pady=20)

    Button(root, text="📝 Create Entry", width=25, font=("Helvetica", 12), bg="#4caf50", fg="white",
           command=lambda: create_entry_ui(root, username)).pack(pady=5)
    Button(root, text="📖 View Entries", width=25, font=("Helvetica", 12), bg="#2196f3", fg="white",
           command=lambda: view_entries_ui(root, username)).pack(pady=5)
    Button(root, text="🔍 Search Entries", width=25, font=("Helvetica", 12), bg="#ff9800", fg="white",
           command=lambda: search_entries_ui(root, username)).pack(pady=5)
    Button(root, text="🚪 Logout", width=25, font=("Helvetica", 12), bg="#607d8b", fg="white",
           command=lambda: show_welcome_screen(root)).pack(pady=20)
    Button(root, text="📁 Filter by Category", width=25, font=("Helvetica", 12), bg="#7e57c2", fg="white",
           command=lambda: filter_by_category_ui(root, username)).pack(pady=5)

    Button(root, text="📅 Filter by Date", width=25, font=("Helvetica", 12), bg="#689f38", fg="white",
           command=lambda: filter_by_date_ui(root, username)).pack(pady=5)

    Button(root, text="🗑️ Delete Entry", width=25, font=("Helvetica", 12), bg="#e53935", fg="white",
           command=lambda: delete_entry_ui(root, username)).pack(pady=5)


def create_entry_ui(root, username):
    clear_window(root)
    root.configure(bg="#f3e5f5")
    Label(root, text="📝 New Diary Entry", font=("Helvetica", 16, "bold"), bg="#f3e5f5").pack(pady=10)

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

    def handle_save():
        title = title_entry.get()
        category = category_entry.get()
        content = content_text.get("1.0", END).strip()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not title or not content:
            messagebox.showerror("Error", "Title and content cannot be empty.")
            return

        entry = {
            "title": title,
            "category": category or "Uncategorized",
            "content": content,
            "timestamp": timestamp,
            "author": username
        }

        save_entry(entry)
        messagebox.showinfo("Success", "Entry saved successfully.")
        show_dashboard_screen(root, username)

    Button(root, text="Save Entry", command=handle_save, font=("Helvetica", 12), width=20, bg="#4caf50", fg="white").pack(pady=10)
    Button(root, text="← Back", command=lambda: show_dashboard_screen(root, username), font=("Helvetica", 12), width=20, bg="#9e9e9e", fg="white").pack()

def view_entries_ui(root, username):
    clear_window(root)
    root.configure(bg="#e1f5fe")
    Label(root, text="📖 Your Diary Entries", font=("Helvetica", 16, "bold"), bg="#e1f5fe").pack(pady=10)

    try:
        entries = load_entries()
    except:
        entries = []

    user_entries = [e for e in entries if e["author"] == username]
    if not user_entries:
        Label(root, text="No entries found.", font=("Helvetica", 12), bg="#e1f5fe").pack()
    else:
        for e in user_entries:
            Label(root, text=f"• {e['title']} ({e['timestamp']})\nCategory: {e['category']}\n{e['content']}\n",
                  justify=LEFT, font=("Helvetica", 11), bg="#e1f5fe", wraplength=360, anchor=W).pack(pady=5)

    Button(root, text="← Back", command=lambda: show_dashboard_screen(root, username), font=("Helvetica", 12), width=20, bg="#9e9e9e", fg="white").pack(pady=10)

def search_entries_ui(root, username):
    clear_window(root)
    root.configure(bg="#fffde7")
    Label(root, text="🔍 Search Diary Entries", font=("Helvetica", 16, "bold"), bg="#fffde7").pack(pady=10)

    frame = Frame(root, bg="#fffde7")
    frame.pack(pady=10)

    Label(frame, text="Keyword:", font=("Helvetica", 12), bg="#fffde7").grid(row=0, column=0, sticky=E)
    keyword_entry = Entry(frame, width=30)
    keyword_entry.grid(row=0, column=1)

    result_frame = Frame(root, bg="#fffde7")
    result_frame.pack()

    def handle_search():
        for widget in result_frame.winfo_children():
            widget.destroy()

        keyword = keyword_entry.get().lower()
        entries = load_entries()
        matches = [e for e in entries if e["author"] == username and (keyword in e["title"].lower() or keyword in e["content"].lower())]

        if not matches:
            Label(result_frame, text="No matching entries found.", font=("Helvetica", 11), bg="#fffde7").pack()
        else:
            for e in matches:
                Label(result_frame, text=f"• {e['title']} ({e['timestamp']})\nCategory: {e['category']}\n{e['content']}\n",
                      justify=LEFT, font=("Helvetica", 11), bg="#fffde7", wraplength=360, anchor=W).pack(pady=5)

    Button(root, text="Search", command=handle_search, font=("Helvetica", 12), width=20, bg="#ff9800", fg="white").pack(pady=5)
    Button(root, text="← Back", command=lambda: show_dashboard_screen(root, username), font=("Helvetica", 12), width=20, bg="#9e9e9e", fg="white").pack(pady=10)

def delete_entry_ui(root, username):
    clear_window(root)
    root.configure(bg="#ffebee")
    Label(root, text="🗑️ Delete Entry", font=("Helvetica", 16, "bold"), bg="#ffebee").pack(pady=10)

    frame = Frame(root, bg="#ffebee")
    frame.pack(pady=5)

    Label(frame, text="Title to delete:", font=("Helvetica", 12), bg="#ffebee").grid(row=0, column=0, sticky=E)
    title_entry = Entry(frame, width=30)
    title_entry.grid(row=0, column=1)

    def handle_delete():
        title = title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Title is required.")
            return
        entries = load_entries()
        new_entries = [e for e in entries if not (e["author"] == username and e["title"] == title)]

        if len(new_entries) == len(entries):
            messagebox.showinfo("Not Found", "No matching entry found.")
        else:
            with open("diary_entries.json", "w") as f:
                json.dump(new_entries, f, indent=4)
            messagebox.showinfo("Deleted", "Entry deleted successfully.")
            show_dashboard_screen(root, username)

    Button(root, text="Delete", command=handle_delete, font=("Helvetica", 12), width=20, bg="#e53935", fg="white").pack(pady=5)
    Button(root, text="← Back", command=lambda: show_dashboard_screen(root, username), font=("Helvetica", 12), width=20, bg="#9e9e9e", fg="white").pack()

def filter_by_category_ui(root, username):
    clear_window(root)
    root.configure(bg="#ede7f6")
    Label(root, text="📁 Filter by Category", font=("Helvetica", 16, "bold"), bg="#ede7f6").pack(pady=10)

    frame = Frame(root, bg="#ede7f6")
    frame.pack(pady=5)

    Label(frame, text="Enter category:", font=("Helvetica", 12), bg="#ede7f6").grid(row=0, column=0, sticky=E)
    cat_entry = Entry(frame, width=30)
    cat_entry.grid(row=0, column=1)

    result_frame = Frame(root, bg="#ede7f6")
    result_frame.pack()

    def handle_filter():
        for widget in result_frame.winfo_children():
            widget.destroy()

        category = cat_entry.get().strip().lower()
        if not category:
            messagebox.showerror("Error", "Please enter a category.")
            return

        entries = load_entries()
        matches = [e for e in entries if e["author"] == username and e["category"].lower() == category]

        if not matches:
            Label(result_frame, text="No entries found in this category.", bg="#ede7f6").pack()
        else:
            for e in matches:
                Label(result_frame, text=f"{e['title']} ({e['timestamp']})\n{e['content']}\n", bg="#ede7f6", anchor=W, wraplength=360).pack(pady=5)

    Button(root, text="Filter", command=handle_filter, font=("Helvetica", 12), width=20, bg="#7e57c2", fg="white").pack(pady=5)
    Button(root, text="← Back", command=lambda: show_dashboard_screen(root, username), font=("Helvetica", 12), width=20, bg="#9e9e9e", fg="white").pack()

def filter_by_date_ui(root, username):
    clear_window(root)
    root.configure(bg="#f1f8e9")
    Label(root, text="📅 Filter by Date Range", font=("Helvetica", 16, "bold"), bg="#f1f8e9").pack(pady=10)

    frame = Frame(root, bg="#f1f8e9")
    frame.pack(pady=5)

    Label(frame, text="Start (YYYY-MM-DD):", font=("Helvetica", 12), bg="#f1f8e9").grid(row=0, column=0)
    start_entry = Entry(frame, width=30)
    start_entry.grid(row=0, column=1)

    Label(frame, text="End (YYYY-MM-DD):", font=("Helvetica", 12), bg="#f1f8e9").grid(row=1, column=0)
    end_entry = Entry(frame, width=30)
    end_entry.grid(row=1, column=1)

    result_frame = Frame(root, bg="#f1f8e9")
    result_frame.pack()

    def handle_filter():
        for widget in result_frame.winfo_children():
            widget.destroy()

        try:
            start_date = datetime.strptime(start_entry.get(), "%Y-%m-%d")
            end_date = datetime.strptime(end_entry.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format.")
            return

        entries = load_entries()
        matches = []
        for e in entries:
            if e["author"] == username:
                try:
                    entry_date = datetime.strptime(e["timestamp"].split()[0], "%Y-%m-%d")
                    if start_date <= entry_date <= end_date:
                        matches.append(e)
                except:
                    continue

        if not matches:
            Label(result_frame, text="No entries in this date range.", bg="#f1f8e9").pack()
        else:
            for e in matches:
                Label(result_frame, text=f"{e['title']} ({e['timestamp']})\n{e['content']}\n", bg="#f1f8e9", anchor=W, wraplength=360).pack(pady=5)

    Button(root, text="Filter", command=handle_filter, font=("Helvetica", 12), width=20, bg="#689f38", fg="white").pack(pady=5)
    Button(root, text="← Back", command=lambda: show_dashboard_screen(root, username), font=("Helvetica", 12), width=20, bg="#9e9e9e", fg="white").pack()

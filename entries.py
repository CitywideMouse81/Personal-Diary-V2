from datetime import datetime
from storage import load_entries, save_entries

def create_entry(user):
    title = input("Title: ")
    content = input("Content: ")
    category = input("Category: ")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = {
        "title": title,
        "content": content,
        "category": category,
        "timestamp": timestamp,
        "author": user
    }

    entries = load_entries()
    entries.append(entry)
    save_entries(entries)
    print("✅ Entry saved!")

def view_entries(user):
    entries = load_entries()
    user_entries = [e for e in entries if e["author"] == user]
    if not user_entries:
        print("📂 No entries found.")
    else:
        for e in user_entries:
            print(f"\n📝 {e['title']} | {e['timestamp']} | {e['category']}\n{e['content']}")

def delete_entry(user):
    entries = load_entries()
    title = input("Enter title to delete: ")
    updated = [e for e in entries if not (e["author"] == user and e["title"] == title)]
    if len(updated) == len(entries):
        print("❌ Entry not found.")
    else:
        save_entries(updated)
        print("🗑️ Entry deleted.")

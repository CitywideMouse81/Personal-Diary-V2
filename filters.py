from datetime import datetime
from storage import load_entries

def get_all_categories(user):
    entries = load_entries()
    return sorted({e["category"] for e in entries if e["author"] == user})

def filter_by_category(user):
    categories = get_all_categories(user)
    if not categories:
        print("📂 No categories found.")
        return
    print("\nAvailable Categories:")
    for cat in categories:
        print(f"- {cat}")
    chosen = input("Filter by: ")
    matches = [e for e in load_entries() if e["author"] == user and e["category"].lower() == chosen.lower()]
    if matches:
        for e in matches:
            print(f"\n📌 {e['title']} | {e['timestamp']}\n{e['content']}")
    else:
        print("❌ No entries found in that category.")

def filter_by_date(user):
    entries = [e for e in load_entries() if e["author"] == user]
    if not entries:
        print("📂 No entries found.")
        return

    start = get_date("Start Date (YYYY-MM-DD): ")
    end = get_date("End Date (YYYY-MM-DD): ")

    results = []
    for e in entries:
        entry_date = datetime.strptime(e['timestamp'][:10], '%Y-%m-%d')
        if start <= entry_date <= end:
            results.append(e)

    if results:
        for e in results:
            print(f"\n📅 {e['title']} | {e['timestamp']} | {e['category']}\n{e['content']}")
    else:
        print("❌ No entries found in range.")

def get_date(prompt):
    while True:
        try:
            return datetime.strptime(input(prompt), '%Y-%m-%d')
        except ValueError:
            print("Invalid date format.")

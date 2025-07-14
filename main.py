from auth import register_user, login_user
from entries import create_entry, view_entries, delete_entry
from filters import filter_by_category, filter_by_date
from storage import load_entries

def search_entries_by_keyword(keyword, user):
    entries = load_entries()
    keyword = keyword.lower()
    return [e for e in entries if e["author"] == user and (keyword in e["title"].lower() or keyword in e["content"].lower())]

def main():
    user = None
    while True:
        if not user:
            print("\n📘 Diary App")
            print("1. Login\n2. Register\n3. Exit")
            ch = input("Choose: ")
            if ch == "1":
                user = login_user()
            elif ch == "2":
                register_user()
            elif ch == "3":
                break
        else:
            print(f"\n👤 Logged in as {user}")
            print("1. Create Entry\n2. View Entries\n3. Search\n4. Filter by Category\n5. Filter by Date\n6. Delete Entry\n7. Logout")
            ch = input("Choose: ")
            if ch == "1": create_entry(user)
            elif ch == "2": view_entries(user)
            elif ch == "3":
                kw = input("Keyword: ")
                results = search_entries_by_keyword(kw, user)
                if results:
                    for r in results:
                        print(f"\n🔍 {r['title']} | {r['timestamp']}\n{r['content']}")
                else:
                    print("❌ No match found.")
            elif ch == "4": filter_by_category(user)
            elif ch == "5": filter_by_date(user)
            elif ch == "6": delete_entry(user)
            elif ch == "7": user = None

if __name__ == '__main__':
    main()

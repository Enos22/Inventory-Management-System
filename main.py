import requests, json, os

BASE = "http://127.0.0.1:5000"
USER_FILE = "admins.json"

# Load admins from file if exists
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return [{"username": "admin", "password": "admin123"}]

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

users = load_users()

def register():
    print("\n--- Create Admin Account ---")
    u = input("New username: ").strip()
    if any(x["username"] == u for x in users):
        print("Username already exists!")
        return False
    p = input("New password: ").strip()
    users.append({"username": u, "password": p})
    save_users(users)
    print(f"Account '{u}' created! Now login.")
    return True

def login():
    print("\n--- Admin Login ---")
    u = input("Username: ").strip()
    p = input("Password: ").strip()
    for x in users:
        if x["username"] == u and x["password"] == p:
            print(f"Welcome {u}!")
            return True
    print("Invalid username or password!")
    return False

# AUTH - Must login to continue
logged_in = False
while not logged_in:
    print("\n==== INVENTORY SYSTEM ====")
    print("1. Login")
    print("2. Create Admin Account")
    print("0. Exit")
    c = input("Choose: ").strip()
    if c == "1":
        logged_in = login()
    elif c == "2":
        register()
    elif c == "0":
        exit()
    else:
        print("Invalid choice")

# MAIN MENU - After login
while True:
    print("\n==== MAIN MENU ====")
    print("1. View all inventory")
    print("2. View one item")
    print("3. Add item")
    print("4. Update stock")
    print("5. Delete item")
    print("6. Search external by barcode")
    print("0. Logout / Exit")

    choice = input("Choose: ").strip()
    try:
        if choice == "1":
            r = requests.get(f"{BASE}/inventory")
            data = r.json()
            if not data:
                print("Inventory empty")
            else:
                for item in data:
                    print(f"[{item['id']}] {item['product_name']} - Stock:  {item['stock']} - ${item['price']}")

        elif choice == "2":
            id = input("Enter ID:")
            r = requests.get(f"{BASE}/inventory/{id}")
            print(r.json())

        elif choice == "3":
            name = input("Product name: ")
            price = float(input("Price: ") or 0)
            stock = int(input("Stock: ") or 0)
            barcode = input("Barcode: ")
            r = requests.post(f"{BASE}/inventory", json={"product_name": name, "price": price, "stock": stock, "barcode": barcode})
            print("Added:", r.json())

        elif choice == "4":
            id = input("Enter ID of Product to Update: ")
            stock = int(input("Enter New Stock: "))
            r = requests.post(f"{BASE}/inventory/{id}", json={"stock": stock})
            print(r.json())
            
        elif choice == "5":
            id = input("Enter ID of Product to delete: ")
            r = requests.delete(f"{BASE}/inventory/{id}")
            print(r.json())

        elif choice == "6":
            barcode = input("Enter Barcode to search Product: ")
            r = requests.get(f"{BASE}/external/product/{barcode}")
            print(r.json())

        elif choice == "0":
            print(f"Logging out....Goodbye")
            break
        else:
            print("Invalid choice, try again")

    except Exception as e:
        print(f"Error: {e} - Is app.py running?")

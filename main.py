import json
import os

import requests

BASE = "http://127.0.0.1:5000"
USER_FILE = "admins.json"

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
WHITE = "\033[97m"


def colorize(text, *codes):
    return "".join(codes) + str(text) + RESET


def render_inventory_table(items):
    if not items:
        return colorize("Inventory is empty.", YELLOW)

    headers = ["ID", "Product", "Stock", "Price"]
    rows = [
        [
            str(item.get("id", "")),
            str(item.get("product_name", "")),
            str(item.get("stock", "")),
            f"${float(item.get('price', 0) or 0):.2f}",
        ]
        for item in items
    ]

    all_rows = [headers] + rows
    widths = [max(len(row[i]) for row in all_rows) for i in range(len(headers))]

    def fmt_row(values):
        return "| " + " | ".join(f"{value:<{widths[idx]}}" for idx, value in enumerate(values)) + " |"

    divider = "+-" + "-+-".join("-" * width for width in widths) + "-+"
    lines = [
        colorize(divider, CYAN),
        colorize(fmt_row(headers), BOLD + BLUE),
        colorize(divider, CYAN),
    ]

    for idx, row in enumerate(rows):
        color = MAGENTA if idx % 2 == 0 else GREEN
        lines.append(colorize(fmt_row(row), color))

    lines.append(colorize(divider, CYAN))
    return "\n".join(lines)


def render_menu(title, options):
    menu_lines = [colorize(f"\n=== {title} ===", BOLD + CYAN)]
    for option in options:
        label, description = option.split(". ", 1) if ". " in option else (option, "")
        menu_lines.append(f"{colorize(label, BOLD + BLUE)}. {colorize(description or label, WHITE)}")
    return "\n".join(menu_lines)


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
    print(colorize("\n--- Create Admin Account ---", BOLD + MAGENTA))
    u = input(colorize("New username: ", YELLOW)).strip()
    if any(x["username"] == u for x in users):
        print(colorize("Username already exists!", RED))
        return False
    p = input(colorize("New password: ", YELLOW)).strip()
    users.append({"username": u, "password": p})
    save_users(users)
    print(colorize(f"Account '{u}' created! Now login.", GREEN))
    return True


def login():
    print(colorize("\n--- Admin Login ---", BOLD + MAGENTA))
    u = input(colorize("Username: ", YELLOW)).strip()
    p = input(colorize("Password: ", YELLOW)).strip()
    for x in users:
        if x["username"] == u and x["password"] == p:
            print(colorize(f"Welcome {u}!", GREEN))
            return True
    print(colorize("Invalid username or password!", RED))
    return False


def main():
    logged_in = False
    while not logged_in:
        print(render_menu("Inventory System", ["1. Login", "2. Create Admin Account", "0. Exit"]))
        c = input(colorize("Choose: ", YELLOW)).strip()
        if c == "1":
            logged_in = login()
        elif c == "2":
            register()
        elif c == "0":
            exit()
        else:
            print(colorize("Invalid choice", RED))

    while True:
        print(render_menu("Main Menu", [
            "1. View all inventory",
            "2. View one item",
            "3. Add item",
            "4. Update stock",
            "5. Delete item",
            "6. Search external by barcode",
            "0. Logout / Exit",
        ]))

        choice = input(colorize("Choose: ", YELLOW)).strip()
        try:
            if choice == "1":
                r = requests.get(f"{BASE}/inventory")
                data = r.json()
                if not data:
                    print(colorize("Inventory empty", YELLOW))
                else:
                    print(render_inventory_table(data))

            elif choice == "2":
                item_id = input(colorize("Enter ID: ", YELLOW))
                r = requests.get(f"{BASE}/inventory/{item_id}")
                print(colorize(json.dumps(r.json(), indent=2), CYAN))

            elif choice == "3":
                name = input(colorize("Product name: ", YELLOW))
                price = float(input(colorize("Price: ", YELLOW)) or 0)
                stock = int(input(colorize("Stock: ", YELLOW)) or 0)
                barcode = input(colorize("Barcode: ", YELLOW))
                r = requests.post(
                    f"{BASE}/inventory",
                    json={"product_name": name, "price": price, "stock": stock, "barcode": barcode},
                )
                print(colorize(f"Added: {json.dumps(r.json(), indent=2)}", GREEN))

            elif choice == "4":
                item_id = input(colorize("Enter ID of Product to Update: ", YELLOW))
                stock = int(input(colorize("Enter New Stock: ", YELLOW)))
                r = requests.post(f"{BASE}/inventory/{item_id}", json={"stock": stock})
                print(colorize(json.dumps(r.json(), indent=2), CYAN))

            elif choice == "5":
                item_id = input(colorize("Enter ID of Product to delete: ", YELLOW))
                r = requests.delete(f"{BASE}/inventory/{item_id}")
                print(colorize(json.dumps(r.json(), indent=2), CYAN))

            elif choice == "6":
                barcode = input(colorize("Enter Barcode to search Product: ", YELLOW))
                r = requests.get(f"{BASE}/external/product/{barcode}")
                print(colorize(json.dumps(r.json(), indent=2), CYAN))

            elif choice == "0":
                print(colorize("Logging out....Goodbye", BOLD + YELLOW))
                break
            else:
                print(colorize("Invalid choice, try again", RED))

        except Exception as exc:
            print(colorize(f"Error: {exc} - Is app.py running?", RED))


if __name__ == "__main__":
    main()

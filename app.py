from flask import Flask, request, jsonify
from externalAPI import fetch_by_barcode, fetch_by_name

app = Flask(__name__)

inventory = [{
    "id": 1,
    "product_name": "Organic Almond Milk",
    "brands": "Silk",
    "barcode": "3274080005003",
    "price": 3.99,
    "stock": 50,
}]
next_id = 2

users = [{"username": "admin", "password": "admin1234"}]


@app.route('/')
def home():
    return jsonify({
        "message": "Inventory API running",
        "endpoints": [
            "/inventory",
            "/inventory/<id>",
            "/register",
            "/login",
            "/external/product/<barcode>",
            "/external/search",
        ],
    })


@app.route('/register', methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400
    if any(u["username"] == username for u in users):
        return jsonify({"error": "user exists"}), 400

    users.append({"username": username, "password": password})
    return jsonify({"message": "account created"}), 201


@app.route('/login', methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")
    user = next((u for u in users if u["username"] == username and u["password"] == password), None)

    if not user:
        return jsonify({"error": "invalid credentials"}), 401
    return jsonify({"message": "login successful", "username": user["username"]})


@app.route('/inventory', methods=["GET"])
def display_all():
    return jsonify(inventory), 200


@app.route('/inventory/<int:item_id>', methods=["GET"])
def get_one(item_id):
    item = next((x for x in inventory if x["id"] == item_id), None)
    return (jsonify(item), 200) if item else (jsonify({"error": "not found"}), 404)


@app.route('/inventory', methods=['POST'])
def add():
    global next_id
    data = request.get_json(silent=True) or {}

    try:
        price = float(data.get("price", 0))
        stock = int(data.get("stock", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "price and stock must be numeric"}), 400

    item = {
        "id": next_id,
        "product_name": data.get("product_name", "Unknown"),
        "brands": data.get("brands", ""),
        "barcode": data.get("barcode", ""),
        "price": price,
        "stock": stock,
    }
    inventory.append(item)
    next_id += 1
    return jsonify(item), 201


@app.route('/inventory/<int:item_id>', methods=["PATCH"])
def update(item_id):
    item = next((x for x in inventory if x["id"] == item_id), None)

    if not item:
        return jsonify({"error": "not found"}), 404

    data = request.get_json(silent=True) or {}
    if not data:
        return jsonify(item)

    item.update(data)
    return jsonify(item)


@app.route('/inventory/<int:item_id>', methods=["DELETE"])
def delete(item_id):
    global inventory
    inventory = [x for x in inventory if x['id'] != item_id]
    return jsonify({"message": "deleted"})


@app.route('/external/product/<barcode>')
def ext_product(barcode):
    return jsonify(fetch_by_barcode(barcode))


@app.route('/external/search', methods=['GET'])
def search_by_name():
    name = request.args.get("name", "")
    return jsonify(fetch_by_name(name))


if __name__ == '__main__':
    app.run(debug=True, port=5000)

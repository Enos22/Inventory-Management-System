from flask import Flask, request, jsonify
from externalAPI import fetch_by_barcode, fetch_by_name

app = Flask(__name__)

inventory = [{"id": 1, "product_name": "Organic Almond Milk", "brands": "Silk","barcode":3274080005003, "price": 3.99,"stock": 50 }]
next_id = 2

users = [{"username":"admin", "password": "admin1234"}]

@app.route('/register', methods=["POST"])
def register():
    data = request.get_json()
    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "username and password required"}), 400
    if any(u["username"] == data["username"] for u in users):
        return jsonify({"error": "user exists"}), 400
    users.append({"username": data["username"], "password": data["password"]})
    return jsonify({"message": "account created"}), 201

@app.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    user = next((u for u in users if u["username"] == data["username"] and u["password"] == data["password"]), None)
    if not user:
        return jsonify({"error": "invalid credentials"}), 401
    return jsonify({"message": "login successful", "username": user["username"]})

@app.route('/inventory', methods = ["GET"])
def display_all():
    return jsonify(inventory), 200

@app.route('/inventory/<int:item_id>', methods = ["GET"])
def get_one(item_id):
    item = next((x for x in inventory if x ['id'] ==id), None)
    return (jsonify(item), 200) if  item else (jsonify({"error": "not found"}), 404)

@app.route('/inventory', methods=['POST'])
def add():
    global next_id
    data = request.get_json() or {}
    item = {"id": next_id, 
            "product_name": data.get("product_name", ''),
            "brands": data.get("brands"),
            "barcode": data.get("barcode"),
            "price": data.get("price", 0), 
            "stock": data.get("stock", 0),
            "ingridients_text": data.get("ingridients_text")
    }
    inventory.append(item)
    next_id += 1
    return jsonify(item), 201

@app.route('/inventory/<int:item_id>', methods = ["PATCH"])
def update(item_id):
    item = next((x for x in inventory if x ['id'] == id), None)

    if not item: 
        return jsonify({"error": "not found"}), 404
    data = request.get_json()
    item.update(data)
    return jsonify(item)

@app.route('/inventory/<int:item_id>', methods = ["DELETE"])
def delete(item_id):
    global inventory
    inventory = [x for x in inventory if x['id'] !=id]
    return jsonify({"message":"deleted"})

@app.route('/external/product/<barcode>')
def ext_product(barcode):
    return jsonify(fetch_by_barcode(barcode))

@app.route('/external/search', methods = ['GET'])
def search_by_name ():
    name = request.args.get("name", "")
    return jsonify(fetch_by_name(name))


if __name__ == '__main__':
    app.run(debug= True, port= 5000)

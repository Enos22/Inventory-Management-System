import app as my_app
import main as cli

client = my_app.app.test_client()


def test_cli_inventory_table():
    rows = [{"id": 1, "product_name": "Milk", "stock": 12, "price": 2.5}]
    table = cli.render_inventory_table(rows)
    assert "ID" in table
    assert "Milk" in table
    assert "12" in table
    assert "2.50" in table


def test_get_inventory():
    res = client.get('/inventory')
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)
    print("GET /inventory works")

def test_add_inventory():
    new_item = {"product_name": "Test Milk", "price": 2.5, "stock": 10, "barcode": "123"}
    res = client.post('/inventory', json=new_item)
    assert res.status_code == 201
    data = res.get_json()
    assert data["product_name"] == "Test Milk"
    print(f"POST /inventory works - Added ID {data['id']}")

def test_get_one():
    new_id =client.post("/inventory", json={"product_name": "Temp", "stock": 1}).get_json()["id"]
    res = client.get(f'/inventory/{new_id}')
    assert res.status_code == 200
    print(f"GET /inventory/{new_id} works")

def test_update():
    res = client.patch('/inventory/1', json={"stock": 99})
    assert res.status_code == 200
    assert res.get_json()["stock"] == 99
    print("PATCH /inventory/{new_id} work")

def test_delete():
    # Add then delete
    add = client.post('/inventory', json={"product_name": "ToDelete", "stock": 1})
    id_to_del = add.get_json()["id"]
    res = client.delete(f'/inventory/{id_to_del}')
    assert res.status_code == 200
    print("DELETE works")

def test_external():
    res = client.get('/external/product/3274080005003')
    assert res.status_code == 200
    print("External Route working correctly")

if __name__ == '__main__':
    test_add_inventory()
    test_get_one()
    test_update()
    test_delete()
    test_external()
    print("\n==============All Tests r OK ==================")
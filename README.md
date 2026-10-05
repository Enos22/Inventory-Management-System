# Inventory Management System

A Flask-based inventory API for managing products, authenticating users, and looking up external product data from Open Food Facts.

## Features
- View all inventory items
- Get a single item by ID
- Add new stock items
- Update item stock or details
- Delete items
- Register and log in users
- Search products by barcode or name from the external API

## Prerequisites
- Python3
- pip

## Setup
1. Open a terminal in the project directory.
2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run the app
```bash
python3 app.py
```
The API runs by default on http://127.0.0.1:5000.

## API endpoints
### Authentication
- POST /register
  - Body: {"username": "admin", "password": "admin1234"}
- POST /login
  - Body: {"username": "admin", "password": "admin1234"}

### Inventory
- GET /inventory
- GET /inventory/<item_id>
- POST /inventory
  - Body example: {"product_name": "Milk", "brands": "Fresh", "barcode": "1234567890", "price": 2.5, "stock": 10}
- PATCH /inventory/<item_id>
- DELETE /inventory/<item_id>

### External product lookup
- GET /external/product/<barcode>
- GET /external/search?name=milk

## Example requests
```bash
curl http://127.0.0.1:5000/inventory
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"product_name":"Milk","brands":"Fresh","barcode":"1234567890","price":2.5,"stock":10}'
curl "http://127.0.0.1:5000/external/search?name=milk"
```

## Testing
Run the project test file:
```bash
python3 test.py
```
Or with pytest:
```bash
pytest -q test.py
```

The suite verifies inventory CRUD, external product lookup, and route responses.

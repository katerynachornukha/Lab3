from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)

# Дані для базової аутентифікації
USERS = {"admin": "password"}

# Каталог товарів
items = {
    1: {"name": "Arabica", "price": 100.25, "size": "Medium"},
    2: {"name": "Robusta", "price": 80.50, "size": "Large"}
}

# Декоратор для базової аутентифікації
def authenticate(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or USERS.get(auth.username) != auth.password:
            return jsonify({"message": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/items', methods=['GET', 'POST'])
@authenticate
def manage_items():
    if request.method == 'GET':
        return jsonify(items)
    elif request.method == 'POST':
        data = request.get_json()
        new_id = max(items.keys()) + 1
        items[new_id] = data
        return jsonify({"message": "Item added", "item": items[new_id]}), 201

@app.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
@authenticate
def manage_item(item_id):
    if item_id not in items:
        return jsonify({"message": "Item not found"}), 404
    
    if request.method == 'GET':
        return jsonify(items[item_id])
    elif request.method == 'PUT':
        data = request.get_json()
        items[item_id].update(data)
        return jsonify({"message": "Item updated", "item": items[item_id]})
    elif request.method == 'DELETE':
        del items[item_id]
        return jsonify({"message": "Item deleted"})

if __name__ == '__main__':
    app.run(port=8000)



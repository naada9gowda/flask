from flask import Flask, jsonify, request

app = Flask(__name__)

items = {}
next_item_id = 1


@app.get("/")
def index():
    return jsonify(message="Simple Items API", endpoints=["/api/items"])








@app.get("/api/items")
def list_items():
    return jsonify(list(items.values()))


@app.post("/api/items")
def create_item():
    global next_item_id

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("name"), str) or not data["name"].strip():
        return jsonify(error="A non-empty 'name' is required"), 400

    item = {
        "id": next_item_id,
        "name": data["name"].strip(),
        "description": data.get("description", ""),
    }
    items[next_item_id] = item
    next_item_id += 1
    return jsonify(item), 201


@app.get("/api/items/<int:item_id>")
def get_item(item_id):
    item = items.get(item_id)
    if item is None:
        return jsonify(error="Item not found"), 404
    return jsonify(item)


@app.put("/api/items/<int:item_id>")
def update_item(item_id):
    if item_id not in items:
        return jsonify(error="Item not found"), 404

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("name"), str) or not data["name"].strip():
        return jsonify(error="A non-empty 'name' is required"), 400

    item = {
        "id": item_id,
        "name": data["name"].strip(),
        "description": data.get("description", ""),
    }
    items[item_id] = item
    return jsonify(item)


@app.delete("/api/items/<int:item_id>")
def delete_item(item_id):
    if items.pop(item_id, None) is None:
        return jsonify(error="Item not found"), 404
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
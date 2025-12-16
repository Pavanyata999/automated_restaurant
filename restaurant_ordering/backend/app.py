from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

menu_items = [
    {"id": 1, "name": "Veg Manchurian", "price": 160, "category": "Starters (Veg)", "available": True, "description": "Crispy vegetable balls in tangy sauce", "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop"},
    {"id": 2, "name": "Gobi 65", "price": 150, "category": "Starters (Veg)", "available": True, "description": "Spicy cauliflower florets", "image": "https://images.unsplash.com/photo-1585238341710-4b4e6f289635?w=400&h=300&fit=crop"},
    {"id": 3, "name": "Paneer 65", "price": 180, "category": "Starters (Veg)", "available": True, "description": "Spicy paneer cubes", "image": "https://images.unsplash.com/photo-1585238341710-4b4e6f289635?w=400&h=300&fit=crop"},
    {"id": 4, "name": "Paneer Tikka", "price": 220, "category": "Starters (Veg)", "available": True, "description": "Grilled paneer with spices", "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd64b73?w=400&h=300&fit=crop"},
    {"id": 5, "name": "Crispy Corn", "price": 170, "category": "Starters (Veg)", "available": True, "description": "Crispy corn kernels", "image": "https://images.unsplash.com/photo-1599599810984-b0f4320166d7?w=400&h=300&fit=crop"},
    {"id": 6, "name": "Chilli Paneer", "price": 190, "category": "Starters (Veg)", "available": True, "description": "Spicy paneer in chilli sauce", "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400&h=300&fit=crop"},
    {"id": 7, "name": "Chicken 65", "price": 220, "category": "Starters (Non-Veg)", "available": True, "description": "Spicy Hyderabadi chicken", "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=400&h=300&fit=crop"},
    {"id": 8, "name": "Chicken Lollipop", "price": 240, "category": "Starters (Non-Veg)", "available": True, "description": "Chicken lollipop in spices", "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=400&h=300&fit=crop"},
    {"id": 9, "name": "Chilli Chicken", "price": 230, "category": "Starters (Non-Veg)", "available": True, "description": "Spicy chicken in chilli sauce", "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=400&h=300&fit=crop"},
    {"id": 10, "name": "Apollo Fish", "price": 280, "category": "Starters (Non-Veg)", "available": True, "description": "Crispy fish in special sauce", "image": "https://images.unsplash.com/photo-1580959375944-abd7e991f971?w=400&h=300&fit=crop"},
    {"id": 11, "name": "Chicken Tikka", "price": 260, "category": "Starters (Non-Veg)", "available": True, "description": "Grilled chicken tikka", "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=400&h=300&fit=crop"},
    {"id": 12, "name": "Mutton Seekh Kebab", "price": 320, "category": "Starters (Non-Veg)", "available": True, "description": "Minced mutton kebabs", "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd64b73?w=400&h=300&fit=crop"},
    {"id": 13, "name": "Paneer Butter Masala", "price": 260, "category": "Main Course (Veg)", "available": True, "description": "Creamy paneer in butter gravy", "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400&h=300&fit=crop"},
    {"id": 14, "name": "Kaju Curry", "price": 280, "category": "Main Course (Veg)", "available": True, "description": "Cashew nut curry", "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop"},
    {"id": 15, "name": "Dal Tadka", "price": 200, "category": "Main Course (Veg)", "available": True, "description": "Tempered lentils", "image": "https://images.unsplash.com/photo-1585238341710-4b4e6f289635?w=400&h=300&fit=crop"},
    {"id": 16, "name": "Veg Kolhapuri", "price": 230, "category": "Main Course (Veg)", "available": True, "description": "Spicy mixed vegetables", "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop"},
    {"id": 17, "name": "Mix Veg Curry", "price": 220, "category": "Main Course (Veg)", "available": True, "description": "Mixed vegetable curry", "image": "https://images.unsplash.com/photo-1585238341710-4b4e6f289635?w=400&h=300&fit=crop"},
    {"id": 18, "name": "Palak Paneer", "price": 250, "category": "Main Course (Veg)", "available": True, "description": "Spinach with paneer cubes", "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400&h=300&fit=crop"},
    {"id": 19, "name": "Chicken Curry", "price": 260, "category": "Main Course (Non-Veg)", "available": True, "description": "Spicy Andhra chicken curry", "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=400&h=300&fit=crop"},
    {"id": 20, "name": "Chicken Butter Masala", "price": 280, "category": "Main Course (Non-Veg)", "available": True, "description": "Creamy chicken curry", "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=400&h=300&fit=crop"},
    {"id": 21, "name": "Mutton Curry", "price": 340, "category": "Main Course (Non-Veg)", "available": True, "description": "Traditional mutton curry", "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd64b73?w=400&h=300&fit=crop"},
    {"id": 22, "name": "Mutton Rogan Josh", "price": 360, "category": "Main Course (Non-Veg)", "available": True, "description": "Kashmiri mutton curry", "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd64b73?w=400&h=300&fit=crop"},
    {"id": 23, "name": "Fish Curry", "price": 300, "category": "Main Course (Non-Veg)", "available": True, "description": "Hyderabadi style fish curry", "image": "https://images.unsplash.com/photo-1580959375944-abd7e991f971?w=400&h=300&fit=crop"},
    {"id": 24, "name": "Prawn Masala", "price": 340, "category": "Main Course (Non-Veg)", "available": True, "description": "Spicy prawn curry", "image": "https://images.unsplash.com/photo-1580959375944-abd7e991f971?w=400&h=300&fit=crop"},
    {"id": 25, "name": "Veg Biryani", "price": 200, "category": "Biryani", "available": True, "description": "Vegetable biryani", "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop"},
    {"id": 26, "name": "Paneer Biryani", "price": 240, "category": "Biryani", "available": True, "description": "Paneer biryani", "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400&h=300&fit=crop"},
    {"id": 27, "name": "Chicken Dum Biryani", "price": 260, "category": "Biryani", "available": True, "description": "Hyderabadi chicken dum biryani", "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=400&h=300&fit=crop"},
    {"id": 28, "name": "Chicken Fry Piece Biryani", "price": 280, "category": "Biryani", "available": True, "description": "Biryani with extra chicken pieces", "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=400&h=300&fit=crop"},
    {"id": 29, "name": "Mutton Dum Biryani", "price": 340, "category": "Biryani", "available": True, "description": "Hyderabadi mutton dum biryani", "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd64b73?w=400&h=300&fit=crop"},
    {"id": 30, "name": "Special Family Pack", "price": 699, "category": "Biryani", "available": True, "description": "Large family pack biryani", "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop"},
    {"id": 31, "name": "Tandoori Roti", "price": 25, "category": "Rotis & Rice", "available": True, "description": "Traditional tandoori roti", "image": "https://images.unsplash.com/photo-1585238341710-4b4e6f289635?w=400&h=300&fit=crop"},
    {"id": 32, "name": "Butter Naan", "price": 45, "category": "Rotis & Rice", "available": True, "description": "Butter naan", "image": "https://images.unsplash.com/photo-1585238341710-4b4e6f289635?w=400&h=300&fit=crop"},
    {"id": 33, "name": "Garlic Naan", "price": 55, "category": "Rotis & Rice", "available": True, "description": "Garlic naan", "image": "https://images.unsplash.com/photo-1585238341710-4b4e6f289635?w=400&h=300&fit=crop"},
    {"id": 34, "name": "Plain Rice", "price": 120, "category": "Rotis & Rice", "available": True, "description": "Steamed rice", "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop"},
    {"id": 35, "name": "Jeera Rice", "price": 160, "category": "Rotis & Rice", "available": True, "description": "Cumin flavored rice", "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop"},
    {"id": 36, "name": "Bagara Rice", "price": 180, "category": "Rotis & Rice", "available": True, "description": "Hyderabadi bagara rice", "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop"},
    {"id": 37, "name": "Raita", "price": 40, "category": "Extras", "available": True, "description": "Yogurt side dish", "image": "https://images.unsplash.com/photo-1585238341710-4b4e6f289635?w=400&h=300&fit=crop"},
    {"id": 38, "name": "Onion Salad", "price": 30, "category": "Extras", "available": True, "description": "Fresh onion salad", "image": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=400&h=300&fit=crop"},
    {"id": 39, "name": "Extra Gravy", "price": 60, "category": "Extras", "available": True, "description": "Extra gravy for dishes", "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop"},
    {"id": 40, "name": "Papad", "price": 20, "category": "Extras", "available": True, "description": "Crispy papad", "image": "https://images.unsplash.com/photo-1585238341710-4b4e6f289635?w=400&h=300&fit=crop"},
    {"id": 41, "name": "Mineral Water", "price": 20, "category": "Beverages", "available": True, "description": "Packaged mineral water", "image": "https://images.unsplash.com/photo-1554866585-c4db4b2a9b2b?w=400&h=300&fit=crop"},
    {"id": 42, "name": "Soft Drink", "price": 40, "category": "Beverages", "available": True, "description": "Soft drinks", "image": "https://images.unsplash.com/photo-1554866585-c4db4b2a9b2b?w=400&h=300&fit=crop"},
    {"id": 43, "name": "Butter Milk", "price": 30, "category": "Beverages", "available": True, "description": "Traditional butter milk", "image": "https://images.unsplash.com/photo-1585238341710-4b4e6f289635?w=400&h=300&fit=crop"},
    {"id": 44, "name": "Sweet Lassi", "price": 70, "category": "Beverages", "available": True, "description": "Sweet yogurt drink", "image": "https://images.unsplash.com/photo-1585238341710-4b4e6f289635?w=400&h=300&fit=crop"},
    {"id": 45, "name": "Masala Soda", "price": 50, "category": "Beverages", "available": True, "description": "Spiced soda", "image": "https://images.unsplash.com/photo-1554866585-c4db4b2a9b2b?w=400&h=300&fit=crop"},
    {"id": 46, "name": "Gulab Jamun", "price": 60, "category": "Desserts", "available": True, "description": "Sweet dumplings in syrup", "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400&h=300&fit=crop"},
    {"id": 47, "name": "Double Ka Meetha", "price": 90, "category": "Desserts", "available": True, "description": "Traditional bread pudding", "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400&h=300&fit=crop"},
    {"id": 48, "name": "Qubani Ka Meetha", "price": 110, "category": "Desserts", "available": True, "description": "Apricot dessert", "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400&h=300&fit=crop"},
    {"id": 49, "name": "Ice Cream", "price": 80, "category": "Desserts", "available": True, "description": "Ice cream scoops", "image": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400&h=300&fit=crop"},
]

tables = [
    {"id": 1, "number": "T1", "capacity": 4, "status": "available"},
    {"id": 2, "number": "T2", "capacity": 4, "status": "available"},
    {"id": 3, "number": "T3", "capacity": 6, "status": "available"},
    {"id": 4, "number": "T4", "capacity": 2, "status": "available"},
    {"id": 5, "number": "T5", "capacity": 8, "status": "available"},
]

orders = []

@app.route('/')
def root():
    return jsonify({"message": "Restaurant Ordering System API", "version": "1.0.0"})

@app.route('/api/v1/menu', methods=['GET'])
def get_menu():
    return jsonify(menu_items)

@app.route('/api/v1/menu/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    item = next((item for item in menu_items if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Menu item not found"}), 404
    return jsonify(item)

@app.route('/api/v1/tables', methods=['GET'])
def get_tables():
    return jsonify(tables)

@app.route('/api/v1/tables/<int:table_id>', methods=['GET'])
def get_table(table_id):
    table = next((table for table in tables if table["id"] == table_id), None)
    if not table:
        return jsonify({"error": "Table not found"}), 404
    return jsonify(table)

@app.route('/api/v1/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

@app.route('/api/v1/orders', methods=['POST'])
def create_order():
    order_data = request.get_json()
    if not order_data or 'table_id' not in order_data or 'items' not in order_data:
        return jsonify({"error": "Missing required fields"}), 400
    total = 0
    for item in order_data['items']:
        menu_item = next((mi for mi in menu_items if mi["id"] == item["menu_item_id"]), None)
        if menu_item:
            total += menu_item["price"] * item.get("quantity", 1)
    order = {
        "id": len(orders) + 1,
        "table_id": order_data["table_id"],
        "items": order_data["items"],
        "status": "pending",
        "total": round(total, 2),
        "created_at": "2024-01-01T12:00:00Z"
    }
    orders.append(order)
    return jsonify(order), 201

@app.route('/api/v1/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = next((order for order in orders if order["id"] == order_id), None)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order)

@app.route('/api/v1/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    order = next((order for order in orders if order["id"] == order_id), None)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    status_data = request.get_json()
    new_status = status_data.get('status', order['status'])
    valid_statuses = ['pending', 'confirmed', 'preparing', 'ready', 'served', 'completed', 'cancelled']
    if new_status not in valid_statuses:
        return jsonify({"error": f"Invalid status"}), 400
    order['status'] = new_status
    return jsonify(order)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)

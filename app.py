from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

items = {
    "Chips": 2.5,
    "Maggi": 1.5,
    "Cake": 10.0,
    "Milk": 2.0,
    "Biscuits": 3.0
}

if not os.path.exists("orders"):
    os.makedirs("orders")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order', methods=['POST'])
def order():
    name = request.form.get("name")
    address = request.form.get("address")

    if not name or not address:
        return "Please enter both name and address."

    return render_template('order.html', name=name, address=address, items=items)

@app.route('/submit_order', methods=['POST'])
def submit_order():
    name = request.form.get("name")
    address = request.form.get("address")
    selected_items = request.form.getlist("items")

    if not selected_items:
        return "No items selected."

    total = sum(items[item] for item in selected_items)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"orders/order_{name.replace(' ', '_')}_{timestamp}.txt"

    with open(filename, "w") as f:
        f.write(f"Name: {name}\n")
        f.write(f"Address: {address}\n")
        f.write(f"Items:\n")
        for item in selected_items:
            f.write(f" - {item}: ${items[item]:.2f}\n")
        f.write(f"\nTotal: ${total:.2f}")

    return f"Thank you, {name}! Your order has been placed. Total: ${total:.2f}"

if __name__ == '__main__':
    app.run(debug=True)

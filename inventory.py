import requests
import json

BASE_URL = "http://localhost:8000"

def get_all_inventory():
    """Query and print all inventory items via API."""
    response = requests.get(f"{BASE_URL}/inventory")
    if response.status_code == 200:
        items = response.json().get("inventory", [])
        for item in items:
            print(item)
    else:
        print(f"Error: {response.status_code} - {response.text}")

def get_inventory_by_id(product_id):
    """Query and print inventory item by product_id via API."""
    response = requests.get(f"{BASE_URL}/inventory/{product_id}")
    if response.status_code == 200:
        item = response.json().get("product")
        print(item)
    else:
        print(f"Error: {response.status_code} - {response.text}")

def add_inventory(category_id, product_code, product_name, description, list_price, inventory, discount_percent=0.0):
    """Add a new inventory item via API."""
    data = {
        "category_id": category_id,
        "product_code": product_code,
        "product_name": product_name,
        "description": description,
        "list_price": list_price,
        "inventory": inventory,
        "discount_percent": discount_percent
    }
    response = requests.post(f"{BASE_URL}/inventory", json=data)
    if response.status_code == 201:
        print("Product added:", response.json())
    else:
        print(f"Error: {response.status_code} - {response.text}")

def remove_inventory(product_id):
    """Remove an inventory item by product_id via API."""
    response = requests.delete(f"{BASE_URL}/inventory/{product_id}")
    if response.status_code == 200:
        print("Product removed:", response.json())
    else:
        print(f"Error: {response.status_code} - {response.text}")


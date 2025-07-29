import requests
import json


def get_all_inventory(base_url):
    """Query and print all inventory items via API."""
    response = requests.get(f"{base_url}/inventory")
    if response.status_code == 200:
        items = response.json().get("inventory", [])
        for item in items:
            print(item)
    else:
        print(f"Error: {response.status_code} - {response.text}")


def get_inventory_by_id(base_url):
    """Prompt for product_id, query and print inventory item via API."""
    product_id = input("Enter product_id: ")
    response = requests.get(f"{base_url}/inventory/{product_id}")
    if response.status_code == 200:
        item = response.json().get("product")
        print(item)
    else:
        print(f"Error: {response.status_code} - {response.text}")


def add_inventory(base_url):
    """Prompt for product details and add a new inventory item via API."""
    category_id = input("Enter category_id: ")
    product_code = input("Enter product_code: ")
    product_name = input("Enter product_name: ")
    description = input("Enter description: ")
    list_price = float(input("Enter list_price: "))
    inventory = int(input("Enter inventory: "))
    discount_percent = float(input("Enter discount_percent (default 0.0): ") or 0.0)
    data = {
        "category_id": category_id,
        "product_code": product_code,
        "product_name": product_name,
        "description": description,
        "list_price": list_price,
        "inventory": inventory,
        "discount_percent": discount_percent,
    }
    response = requests.post(f"{base_url}/inventory", json=data)
    if response.status_code == 201:
        print("Product added:", response.json())
    else:
        print(f"Error: {response.status_code} - {response.text}")


def remove_inventory(base_url):
    """Prompt for product_id and remove an inventory item via API."""
    product_id = input("Enter product_id to remove: ")
    response = requests.delete(f"{base_url}/inventory/{product_id}")
    if response.status_code == 200:
        print("Product removed:", response.json())
    else:
        print(f"Error: {response.status_code} - {response.text}")

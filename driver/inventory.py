import requests
import json
import asyncio
from driver.auth import get_auth_headers, prompt_and_get_new_cookie


def get_all_inventory(base_url):
    """Query and print all inventory items via API."""
    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.get(f"{base_url}/inventory", headers=headers)
            if response.status_code == 200:
                items = response.json().get("inventory", [])
                for item in items:
                    print(item)
                return
            elif response.status_code == 401 and attempt == 0:
                print("Session expired or invalid. Getting new cookie...")
                asyncio.run(prompt_and_get_new_cookie())
                continue
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return


def get_inventory_by_id(base_url):
    """Prompt for product_id, query and print inventory item via API."""
    product_id = input("Enter product_id: ")
    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.get(f"{base_url}/inventory/{product_id}", headers=headers)
            if response.status_code == 200:
                item = response.json().get("product")
                print(item)
                return
            elif response.status_code == 401 and attempt == 0:
                print("Session expired or invalid. Getting new cookie...")
                asyncio.run(prompt_and_get_new_cookie())
                continue
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return


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
    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.post(f"{base_url}/inventory", json=data, headers=headers)
            if response.status_code == 201:
                print("Product added:", response.json())
                return
            elif response.status_code == 401 and attempt == 0:
                print("Session expired or invalid. Getting new cookie...")
                asyncio.run(prompt_and_get_new_cookie())
                continue
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return


def remove_inventory(base_url):
    """Prompt for product_id and remove an inventory item via API."""
    product_id = input("Enter product_id to remove: ")
    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.delete(f"{base_url}/inventory/{product_id}", headers=headers)
            if response.status_code == 200:
                print("Product removed:", response.json())
                return
            elif response.status_code == 401 and attempt == 0:
                print("Session expired or invalid. Getting new cookie...")
                asyncio.run(prompt_and_get_new_cookie())
                continue
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return

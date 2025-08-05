import requests
import json
import asyncio
from driver.auth import get_auth_headers, prompt_and_get_new_cookie

def get_all_products(base_url):
    print("\n=== Getting all products ===")
    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.get(f"{base_url}/products", headers=headers)
            if response.status_code == 200:
                products = response.json()
                print("Products found:")
                for product in products["products"]:
                    print(
                        f"Code: {product['product_code']}, Name: {product['product_name']}, Price: {product['list_price']}"
                    )
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

def get_product_by_code(base_url):
    print("\n=== Get product by code ===")
    product_code = input("Enter product code: ")
    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.get(f"{base_url}/products/{product_code}", headers=headers)
            if response.status_code == 200:
                product = response.json()["product"]
                print(f"Product found:")
                print(f"Code: {product['product_code']}")
                print(f"Name: {product['product_name']}")
                print(f"Price: {product['list_price']}")
                return
            elif response.status_code == 401 and attempt == 0:
                print("Session expired or invalid. Getting new cookie...")
                asyncio.run(prompt_and_get_new_cookie())
                continue
            elif response.status_code == 404:
                print(f"Product with code {product_code} not found")
                return
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return

def add_new_product(base_url):
    print("\n=== Add new product ===")
    category_id = input("Enter category ID: ")
    product_code = input("Enter product code: ")
    product_name = input("Enter product name: ")
    description = input("Enter product description or leave blank: ")
    list_price = input("Enter product price: ")
    inventory = input("Enter product inventory: ")
    discount_percent = input("Enter product discount percent: ")
    date_added = input(
        "Enter date added (YYYY-MM-DD HH:MM:SS) or leave blank: "
    )

    product_data = {
        "category_id": int(category_id),
        "product_code": product_code,
        "product_name": product_name,
        "description": description,
        "list_price": float(list_price),
        "inventory": int(inventory),
        "discount_percent": float(discount_percent),
        "date_added": date_added if date_added else None,
    }

    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.put(f"{base_url}/products", json=product_data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                print(f"Success: {result['message']}")
                print(f"New product ID: {result['product_id']}")
                return
            elif response.status_code == 401 and attempt == 0:
                print("Session expired or invalid. Getting new cookie...")
                asyncio.run(prompt_and_get_new_cookie())
                continue
            elif response.status_code == 404:
                print("Error: Product not found")
                return
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return

def delete_product(base_url):
    print("\n=== Delete product ===")
    product_code = input("Enter product code to delete: ")
    confirm = input(
        f"Are you sure you want to delete product {product_code}? (y/n): "
    )

    if confirm.lower() != "y":
        print("Delete operation cancelled")
        return

    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.delete(f"{base_url}/products/{product_code}", headers=headers)
            if response.status_code == 200:
                result = response.json()
                print(f"Success: {result['message']}")
                return
            elif response.status_code == 401 and attempt == 0:
                print("Session expired or invalid. Getting new cookie...")
                asyncio.run(prompt_and_get_new_cookie())
                continue
            elif response.status_code == 404:
                print(f"Product with code {product_code} not found")
                return
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return


import requests
import asyncio
from driver.auth import get_auth_headers, prompt_and_get_new_cookie

def get_all_categories(base_url):
    print("\n=== Getting all categories ===")
    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.get(f"{base_url}/categories", headers=headers)
            if response.status_code == 200:
                categories = response.json()
                print("Categories found:")
                for category in categories["categories"]:
                    print(f"ID: {category['category_id']}, Name: {category['category_name']}")
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

def get_category_by_id(base_url):
    print("\n=== Get category by ID ===")
    category_id = input("Enter category ID: ")
    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.get(f"{base_url}/categories/{category_id}", headers=headers)
            if response.status_code == 200:
                category = response.json()["category"]
                print(f"Category found:")
                print(f"ID: {category['category_id']}")
                print(f"Name: {category['category_name']}")
                return
            elif response.status_code == 401 and attempt == 0:
                print("Session expired or invalid. Getting new cookie...")
                asyncio.run(prompt_and_get_new_cookie())
                continue
            elif response.status_code == 404:
                print(f"Category with ID {category_id} not found")
                return
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return

def add_new_category(base_url):
    print("\n=== Add new category ===")
    category_name = input("Enter category name: ")
    category_data = {
        "category_name": category_name
    }
    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.put(f"{base_url}/categories", json=category_data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                print(f"Success: {result['message']}")
                print(f"New category ID: {result['category_id']}")
                return
            elif response.status_code == 401 and attempt == 0:
                print("Session expired or invalid. Getting new cookie...")
                asyncio.run(prompt_and_get_new_cookie())
                continue
            elif response.status_code == 400:
                print(f"Error: Category '{category_name}' already exists")
                return
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return

def delete_category(base_url):
    print("\n=== Delete category ===")
    category_id = input("Enter category ID to delete: ")
    confirm = input(f"Are you sure you want to delete category {category_id}? (y/n): ")
    if confirm.lower() != 'y':
        print("Delete operation cancelled")
        return
    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.delete(f"{base_url}/categories/{category_id}", headers=headers)
            if response.status_code == 200:
                result = response.json()
                print(f"Success: {result['message']}")
                return
            elif response.status_code == 401 and attempt == 0:
                print("Session expired or invalid. Getting new cookie...")
                asyncio.run(prompt_and_get_new_cookie())
                continue
            elif response.status_code == 404:
                print(f"Category with ID {category_id} not found")
                return
            elif response.status_code == 400:
                print(f"Error: {response.text}")
                return
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return

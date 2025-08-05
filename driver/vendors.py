import requests
import asyncio
from driver.auth import get_auth_headers, prompt_and_get_new_cookie


def get_all_vendors(base_url):
    print("\n=== Getting all vendors ===")
    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.get(f"{base_url}/vendors", headers=headers)
            if response.status_code == 200:
                vendors = response.json()
                print("Vendors found:")
                for vendor in vendors["vendors"]:
                    print(
                        f"ID: {vendor['vendor_id']}, Name: {vendor['vendor_name']}, Product ID: {vendor['product_id']}"
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


def get_vendor_by_id(base_url):
    print("\n=== Get vendor by ID ===")
    vendor_id = input("Enter vendor ID: ")
    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.get(f"{base_url}/vendors/{vendor_id}", headers=headers)
            if response.status_code == 200:
                vendor = response.json()["vendor"]
                print(f"Vendor found:")
                print(f"ID: {vendor['vendor_id']}")
                print(f"Name: {vendor['vendor_name']}")
                print(f"Product ID: {vendor['product_id']}")
                return
            elif response.status_code == 401 and attempt == 0:
                print("Session expired or invalid. Getting new cookie...")
                asyncio.run(prompt_and_get_new_cookie())
                continue
            elif response.status_code == 404:
                print(f"Vendor with ID {vendor_id} not found")
                return
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return


def add_new_vendor(base_url):
    print("\n=== Add new vendor ===")
    vendor_name = input("Enter vendor name: ")
    product_id = input("Enter product ID: ")
    vendor_data = {"vendor_name": vendor_name, "product_id": int(product_id)}
    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.put(f"{base_url}/vendors", json=vendor_data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                print(f"Success: {result['message']}")
                print(f"New vendor ID: {result['vendor_id']}")
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


def delete_vendor(base_url):
    print("\n=== Delete vendor ===")
    vendor_id = input("Enter vendor ID to delete: ")
    confirm = input(f"Are you sure you want to delete vendor {vendor_id}? (y/n): ")

    if confirm.lower() != "y":
        print("Delete operation cancelled")
        return

    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.delete(f"{base_url}/vendors/{vendor_id}", headers=headers)
            if response.status_code == 200:
                result = response.json()
                print(f"Success: {result['message']}")
                return
            elif response.status_code == 401 and attempt == 0:
                print("Session expired or invalid. Getting new cookie...")
                asyncio.run(prompt_and_get_new_cookie())
                continue
            elif response.status_code == 404:
                print(f"Vendor with ID {vendor_id} not found")
                return
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return

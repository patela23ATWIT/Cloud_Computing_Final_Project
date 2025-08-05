import requests
from driver.auth import get_auth_headers, prompt_and_get_new_cookie
import asyncio

def get_all_admins(base_url):
    print("\n=== Getting all admins ===")
    for attempt in range(2):  # Try at most twice
        try:
            headers = get_auth_headers()
            response = requests.get(f"{base_url}/admins", headers=headers)
            if response.status_code == 200:
                admins = response.json()
                print("Admins found:")
                for admin in admins["admins"]:
                    print(f"ID: {admin['admin_id']}, Name: {admin['first_name']} {admin['last_name']}, Email: {admin['email_address']}")
                return
            elif response.status_code == 401 and attempt == 0:
                print("Session expired or invalid. Getting new cookie...")
                asyncio.run(prompt_and_get_new_cookie())
                continue  # Retry after getting new cookie
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return

# Apply the same retry logic to other functions:
def get_admin_by_id(base_url):
    print("\n=== Get admin by ID ===")
    admin_id = input("Enter admin ID: ")
    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.get(f"{base_url}/admins/{admin_id}", headers=headers)
            if response.status_code == 200:
                admin = response.json()["admin"]
                print(f"Admin found:")
                print(f"ID: {admin['admin_id']}")
                print(f"First Name: {admin['first_name']}")
                print(f"Last Name: {admin['last_name']}")
                print(f"Email: {admin['email_address']}")
                return
            elif response.status_code == 401 and attempt == 0:
                print("Session expired or invalid. Getting new cookie...")
                asyncio.run(prompt_and_get_new_cookie())
                continue
            elif response.status_code == 404:
                print(f"Admin with ID {admin_id} not found")
                return
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return

def add_new_admin(base_url):
    print("\n=== Add new admin ===")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email_address = input("Enter email address: ")
    password = input("Enter password: ")
    admin_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email_address": email_address,
        "password": password
    }
    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.put(f"{base_url}/admins", json=admin_data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                print(f"Success: {result['message']}")
                print(f"New admin ID: {result['admin_id']}")
                return
            elif response.status_code == 401 and attempt == 0:
                print("Session expired or invalid. Getting new cookie...")
                asyncio.run(prompt_and_get_new_cookie())
                continue
            elif response.status_code == 400:
                print("Error: Admin with this email already exists")
                return
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return

def delete_admin(base_url):
    print("\n=== Delete admin ===")
    admin_id = input("Enter admin ID to delete: ")
    confirm = input(f"Are you sure you want to delete admin {admin_id}? (y/n): ")
    if confirm.lower() != 'y':
        print("Delete operation cancelled")
        return
    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.delete(f"{base_url}/admins/{admin_id}", headers=headers)
            if response.status_code == 200:
                result = response.json()
                print(f"Success: {result['message']}")
                return
            elif response.status_code == 401 and attempt == 0:
                print("Session expired or invalid. Getting new cookie...")
                asyncio.run(prompt_and_get_new_cookie())
                continue
            elif response.status_code == 404:
                print(f"Admin with ID {admin_id} not found")
                return
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return

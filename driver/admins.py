import requests

def get_all_admins(base_url):
    # Get all admins
    print("\n=== Getting all admins ===")
    try:
        response = requests.get(f"{base_url}/admins")
        if response.status_code == 200:
            admins = response.json()
            print("Admins found:")
            for admin in admins["admins"]:
                print(f"ID: {admin['admin_id']}, Name: {admin['first_name']} {admin['last_name']}, Email: {admin['email_address']}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def get_admin_by_id(base_url):
    # Get admin by ID
    print("\n=== Get admin by ID ===")
    admin_id = input("Enter admin ID: ")
    try:
        response = requests.get(f"{base_url}/admins/{admin_id}")
        if response.status_code == 200:
            admin = response.json()["admin"]
            print(f"Admin found:")
            print(f"ID: {admin['admin_id']}")
            print(f"First Name: {admin['first_name']}")
            print(f"Last Name: {admin['last_name']}")
            print(f"Email: {admin['email_address']}")
        elif response.status_code == 404:
            print(f"Admin with ID {admin_id} not found")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def add_new_admin(base_url):
    # Add new admin
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
    
    try:
        response = requests.put(f"{base_url}/admins", json=admin_data)
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result['message']}")
            print(f"New admin ID: {result['admin_id']}")
        elif response.status_code == 400:
            print("Error: Admin with this email already exists")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def delete_admin(base_url):
    # Delete admin
    print("\n=== Delete admin ===")
    admin_id = input("Enter admin ID to delete: ")
    confirm = input(f"Are you sure you want to delete admin {admin_id}? (y/n): ")
    
    if confirm.lower() == 'y':
        try:
            response = requests.delete(f"{base_url}/admins/{admin_id}")
            if response.status_code == 200:
                result = response.json()
                print(f"Success: {result['message']}")
            elif response.status_code == 404:
                print(f"Admin with ID {admin_id} not found")
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
    else:
        print("Delete operation cancelled")

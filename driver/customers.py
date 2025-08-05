import requests
import asyncio
from driver.auth import get_auth_headers, prompt_and_get_new_cookie

def get_all_customers(base_url):
    print("\n=== Getting all customers ===")
    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.get(f"{base_url}/customers", headers=headers)
            if response.status_code == 200:
                customers = response.json()
                print("Customers found:")
                for customer in customers["customers"]:
                    print(
                        f"ID: {customer['customer_id']}, Name: {customer['first_name']} {customer['last_name']}, Email: {customer['email_address']}"
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

def get_customer_by_id(base_url):
    print("\n=== Get customer by ID ===")
    customer_id = input("Enter customer ID: ")
    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.get(f"{base_url}/customers/{customer_id}", headers=headers)
            if response.status_code == 200:
                customer = response.json()["customer"]
                print(f"Customer found:")
                print(f"ID: {customer['customer_id']}")
                print(f"First Name: {customer['first_name']}")
                print(f"Last Name: {customer['last_name']}")
                print(f"Email: {customer['email_address']}")
                return
            elif response.status_code == 401 and attempt == 0:
                print("Session expired or invalid. Getting new cookie...")
                asyncio.run(prompt_and_get_new_cookie())
                continue
            elif response.status_code == 404:
                print(f"Customer with ID {customer_id} not found")
                return
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return

def add_new_customer(base_url):
    print("\n=== Add new customer ===")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email address: ")
    password = input("Enter password: ")

    customer_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
    }

    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.put(f"{base_url}/customers", json=customer_data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                print(f"Success: {result['message']}")
                print(f"New customer ID: {result['customer_id']}")
                return
            elif response.status_code == 401 and attempt == 0:
                print("Session expired or invalid. Getting new cookie...")
                asyncio.run(prompt_and_get_new_cookie())
                continue
            elif response.status_code == 400:
                print("Error: Customer with this email already exists")
                return
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return

def delete_customer(base_url):
    print("\n=== Delete customer ===")
    customer_id = input("Enter customer ID to delete: ")
    confirm = input(
        f"Are you sure you want to delete customer {customer_id}? (y/n): "
    )

    if confirm.lower() != "y":
        print("Delete operation cancelled")
        return

    for attempt in range(2):
        try:
            headers = get_auth_headers()
            response = requests.delete(f"{base_url}/customers/{customer_id}", headers=headers)
            if response.status_code == 200:
                result = response.json()
                print(f"Success: {result['message']}")
                return
            elif response.status_code == 401 and attempt == 0:
                print("Session expired or invalid. Getting new cookie...")
                asyncio.run(prompt_and_get_new_cookie())
                continue
            elif response.status_code == 404:
                print(f"Customer with ID {customer_id} not found")
                return
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return
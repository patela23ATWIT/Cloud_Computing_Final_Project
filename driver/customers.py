import requests

def get_all_customers(base_url):
    print("\n=== Getting all customers ===")
    try:
        response = requests.get(f"{base_url}/customers")
        if response.status_code == 200:
            customers = response.json()
            print("Customers found:")
            for customer in customers["customers"]:
                print(
                    f"ID: {customer['customer_id']}, Name: {customer['first_name']} {customer['last_name']}, Email: {customer['email_address']}"
                )
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def get_customer_by_id(base_url):
    print("\n=== Get customer by ID ===")
    customer_id = input("Enter customer ID: ")
    try:
        response = requests.get(f"{base_url}/customers/{customer_id}")
        if response.status_code == 200:
            customer = response.json()["customer"]
            print(f"Customer found:")
            print(f"ID: {customer['customer_id']}")
            print(f"First Name: {customer['first_name']}")
            print(f"Last Name: {customer['last_name']}")
            print(f"Email: {customer['email_address']}")
        elif response.status_code == 404:
            print(f"Customer with ID {customer_id} not found")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

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

    try:
        response = requests.put(f"{base_url}/customers", json=customer_data)
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result['message']}")
            print(f"New customer ID: {result['customer_id']}")
        elif response.status_code == 400:
            print("Error: Customer with this email already exists")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def delete_customer(base_url):
    print("\n=== Delete customer ===")
    customer_id = input("Enter customer ID to delete: ")
    confirm = input(
        f"Are you sure you want to delete customer {customer_id}? (y/n): "
    )

    if confirm.lower() == "y":
        try:
            response = requests.delete(f"{base_url}/customers/{customer_id}")
            if response.status_code == 200:
                result = response.json()
                print(f"Success: {result['message']}")
            elif response.status_code == 404:
                print(f"Customer with ID {customer_id} not found")
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
    else:
        print("Delete operation cancelled")
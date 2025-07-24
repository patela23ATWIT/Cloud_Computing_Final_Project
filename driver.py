import requests
import json

def driver():
    print("Welcome to the Sporting Shop API Driver!")

    continueToLoop = True

    while continueToLoop:
        print("\nSelect a command to test:")
        print("0: Exit")
        print("1: Get all vendors")
        print("2: Get vendor by ID")
        print("3: Add new vendor")
        print("4: Delete vendor")
        print("9: Get all customers")
        print("10: Get customer by ID")
        print("11: Add new customer")
        print("12: Delete customer")

        command = input("Enter a command: ")
        base_url = "http://localhost:8000"

        if command == "0":
            continueToLoop = False

        elif command == "1": 
            # Get all vendors
            print("\n=== Getting all vendors ===")
            try:
                response = requests.get(f"{base_url}/vendors")
                if response.status_code == 200:
                    vendors = response.json()
                    print("Vendors found:")
                    for vendor in vendors["vendors"]:
                        print(f"ID: {vendor['vendor_id']}, Name: {vendor['vendor_name']}, Product ID: {vendor['product_id']}")
                else:
                    print(f"Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                
        elif command == "2":
            # Get vendor by ID
            print("\n=== Get vendor by ID ===")
            vendor_id = input("Enter vendor ID: ")
            try:
                response = requests.get(f"{base_url}/vendors/{vendor_id}")
                if response.status_code == 200:
                    vendor = response.json()["vendor"]
                    print(f"Vendor found:")
                    print(f"ID: {vendor['vendor_id']}")
                    print(f"Name: {vendor['vendor_name']}")
                    print(f"Product ID: {vendor['product_id']}")
                elif response.status_code == 404:
                    print(f"Vendor with ID {vendor_id} not found")
                else:
                    print(f"Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                
        elif command == "3":
            # Add new vendor
            print("\n=== Add new vendor ===")
            vendor_name = input("Enter vendor name: ")
            product_id = input("Enter product ID: ")
            
            vendor_data = {
                "vendor_name": vendor_name,
                "product_id": int(product_id)
            }
            
            try:
                response = requests.put(f"{base_url}/vendors", json=vendor_data)
                if response.status_code == 200:
                    result = response.json()
                    print(f"Success: {result['message']}")
                    print(f"New vendor ID: {result['vendor_id']}")
                elif response.status_code == 404:
                    print("Error: Product not found")
                else:
                    print(f"Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                
        elif command == "4":
            # Delete vendor
            print("\n=== Delete vendor ===")
            vendor_id = input("Enter vendor ID to delete: ")
            confirm = input(f"Are you sure you want to delete vendor {vendor_id}? (y/n): ")
            
            if confirm.lower() == 'y':
                try:
                    response = requests.delete(f"{base_url}/vendors/{vendor_id}")
                    if response.status_code == 200:
                        result = response.json()
                        print(f"Success: {result['message']}")
                    elif response.status_code == 404:
                        print(f"Vendor with ID {vendor_id} not found")
                    else:
                        print(f"Error: {response.status_code} - {response.text}")
                except requests.exceptions.RequestException as e:
                    print(f"Request failed: {e}")
            else:
                print("Delete operation cancelled")
                
        elif command == "9":
            # Get all customers
            print("\n=== Getting all customers ===")
            try:
                response = requests.get(f"{base_url}/customers")
                if response.status_code == 200:
                    customers = response.json()
                    print("Customers found:")
                    for customer in customers["customers"]:
                        print(f"ID: {customer['customer_id']}, Name: {customer['first_name']} {customer['last_name']}, Email: {customer['email_address']}")
                else:
                    print(f"Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                
        elif command == "10":
            # Get customer by ID
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
                
        elif command == "11":
            # Add new customer
            print("\n=== Add new customer ===")
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email address: ")
            password = input("Enter password: ")
            
            customer_data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password
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
                
        elif command == "12":
            # Delete customer
            print("\n=== Delete customer ===")
            customer_id = input("Enter customer ID to delete: ")
            confirm = input(f"Are you sure you want to delete customer {customer_id}? (y/n): ")
            
            if confirm.lower() == 'y':
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
                            
        else:
            print("Invalid Input, Try again.")


if __name__ == "__main__":
    driver()

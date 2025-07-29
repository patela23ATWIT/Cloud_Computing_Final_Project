import requests

def get_all_orders(base_url):
    print("\n=== Getting all orders ===")
    try:
        response = requests.get(f"{base_url}/orders")
        if response.status_code == 200:
            orders = response.json()
            print("Orders found:")
            for order in orders["orders"]:
                print(
                    f"Order ID: {order['order_id']}, Customer ID: {order['customer_id']}, Ship Amount: ${order['ship_amount']}"
                )
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def get_order_by_id(base_url):
    print("\n=== Get order by ID ===")
    order_id = input("Enter order ID: ")
    try:
        response = requests.get(f"{base_url}/orders/{order_id}")
        if response.status_code == 200:
            order = response.json()["order"]
            print(f"Order found:")
            print(f"Order ID: {order['order_id']}")
            print(f"Customer ID: {order['customer_id']}")
            print(f"Order Date: {order['order_date']}")
            print(f"Ship Amount: ${order['ship_amount']}")
            print(f"Card Number: {order['card_number']}")
        elif response.status_code == 404:
            print(f"Order with ID {order_id} not found")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def add_new_order(base_url):
    print("\n=== Add new order ===")
    customer_id = input("Enter customer ID: ")
    order_date = input("Enter order date (YYYY-MM-DD HH:MM:SS): ")
    ship_amount = input("Enter ship amount: ")
    ship_address_id = input("Enter ship address ID: ")
    card_number = input("Enter card number: ")
    billing_address_id = input("Enter billing address ID: ")

    order_data = {
        "customer_id": int(customer_id),
        "order_date": order_date,
        "ship_amount": float(ship_amount),
        "ship_address_id": int(ship_address_id),
        "card_number": card_number,
        "billing_address_id": int(billing_address_id),
    }

    try:
        response = requests.put(f"{base_url}/orders", json=order_data)
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result['message']}")
            print(f"New order ID: {result['order_id']}")
        elif response.status_code == 404:
            print("Error: Customer not found")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def delete_order(base_url):
    print("\n=== Delete order ===")
    order_id = input("Enter order ID to delete: ")
    confirm = input(
        f"Are you sure you want to delete order {order_id}? (y/n): "
    )

    if confirm.lower() == "y":
        try:
            response = requests.delete(f"{base_url}/orders/{order_id}")
            if response.status_code == 200:
                result = response.json()
                print(f"Success: {result['message']}")
            elif response.status_code == 404:
                print(f"Order with ID {order_id} not found")
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
    else:
        print("Delete operation cancelled")
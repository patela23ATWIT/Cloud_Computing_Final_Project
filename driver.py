import requests
import json
from driver import vendors  # Add this import
from driver import inventory  # Add this import
from driver import products
from driver import customers  # Add this import
from driver import orders  # Add this import


def driver():
    print("Welcome to the Sporting Shop API Driver!")

    command_map = {
        "1": lambda url: vendors.get_all_vendors(url),
        "2": lambda url: vendors.get_vendor_by_id(url),
        "3": lambda url: vendors.add_new_vendor(url),
        "4": lambda url: vendors.delete_vendor(url),
        "5": lambda url: products.get_all_products(url),
        "6": lambda url: products.get_product_by_code(url),
        "7": lambda url: products.add_new_product(url),
        "8": lambda url: products.delete_product(url),
        "9": lambda url: customers.get_all_customers(url),
        "10": lambda url: customers.get_customer_by_id(url),
        "11": lambda url: customers.add_new_customer(url),
        "12": lambda url: customers.delete_customer(url),
        "13": lambda url: orders.get_all_orders(url),
        "14": lambda url: orders.get_order_by_id(url),
        "15": lambda url: orders.add_new_order(url),
        "16": lambda url: orders.delete_order(url),
        "17": lambda url: inventory.get_all_inventory(url),
        "18": lambda url: inventory.get_inventory_by_id(url),
        "19": lambda url: inventory.add_inventory(url),
        "20": lambda url: inventory.remove_inventory(url),
    }

    continueToLoop = True

    while continueToLoop:
        print("\nSelect a command to test:")
        print("0: Exit")
        print("1: Get all vendors")
        print("2: Get vendor by ID")
        print("3: Add new vendor")
        print("4: Delete vendor")
        print("5: Get all products")
        print("6: Get product by code")
        print("7: Add new product")
        print("8: Delete product")
        print("9: Get all customers")
        print("10: Get customer by ID")
        print("11: Add new customer")
        print("12: Delete customer")
        print("13: Get all orders")
        print("14: Get order by ID")
        print("15: Add new order")
        print("16: Delete order")
        print("17: Get all inventory")
        print("18: Get inventory by ID")
        print("19: Add inventory item")
        print("20: Remove inventory item")

        command = input("Enter a command: ")
        base_url = "http://localhost:8000"

        if command == "0":
            continueToLoop = False
        elif command in command_map:
            command_map[command](base_url)
        else:
            print("Invalid Input, Try again.")


if __name__ == "__main__":
    driver()

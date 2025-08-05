import requests
import json
from driver import vendors  # Add this import
from driver import inventory  # Add this import
from driver import products
from driver import customers  # Add this import
from driver import orders  # Add this import
from driver import admins  # Add this import
from driver import categories  # Add this import

VENDOR_PORT = 8000
INVENTORY_PORT = 8001
PRODUCTS_PORT = 8002
CUSTOMERS_PORT = 8003
ORDERS_PORT = 8004
ADMINS_PORT = 8005
CATEGORIES_PORT = 8006

def driver():
    print("Welcome to the Sporting Shop API Driver!")

    command_map = {
        "1": lambda url: vendors.get_all_vendors(url + f":{VENDOR_PORT}"),
        "2": lambda url: vendors.get_vendor_by_id(url + f":{VENDOR_PORT}"),
        "3": lambda url: vendors.add_new_vendor(url + f":{VENDOR_PORT}"),
        "4": lambda url: vendors.delete_vendor(url + f":{VENDOR_PORT}"),
        "5": lambda url: products.get_all_products(url + f":{PRODUCTS_PORT}"),
        "6": lambda url: products.get_product_by_code(url + f":{PRODUCTS_PORT}"),
        "7": lambda url: products.add_new_product(url + f":{PRODUCTS_PORT}"),
        "8": lambda url: products.delete_product(url + f":{PRODUCTS_PORT}"),
        "9": lambda url: customers.get_all_customers(url + f":{CUSTOMERS_PORT}"),
        "10": lambda url: customers.get_customer_by_id(url + f":{CUSTOMERS_PORT}"),
        "11": lambda url: customers.add_new_customer(url + f":{CUSTOMERS_PORT}"),
        "12": lambda url: customers.delete_customer(url + f":{CUSTOMERS_PORT}"),
        "13": lambda url: orders.get_all_orders(url + f":{ORDERS_PORT}"),
        "14": lambda url: orders.get_order_by_id(url + f":{ORDERS_PORT}"),
        "15": lambda url: orders.add_new_order(url + f":{ORDERS_PORT}"),
        "16": lambda url: orders.delete_order(url + f":{ORDERS_PORT}"),
        "17": lambda url: inventory.get_all_inventory(url + f":{INVENTORY_PORT}"),
        "18": lambda url: inventory.get_inventory_by_id(url + f":{INVENTORY_PORT}"),
        "19": lambda url: inventory.add_inventory(url + f":{INVENTORY_PORT}"),
        "20": lambda url: inventory.remove_inventory(url + f":{INVENTORY_PORT}"),
        "21": lambda url: admins.get_all_admins(url + f":{ADMINS_PORT}"),
        "22": lambda url: admins.get_admin_by_id(url + f":{ADMINS_PORT}"),
        "23": lambda url: admins.add_new_admin(url + f":{ADMINS_PORT}"),
        "24": lambda url: admins.delete_admin(url + f":{ADMINS_PORT}"),
        "25": lambda url: categories.get_all_categories(url + f":{CATEGORIES_PORT}"),
        "26": lambda url: categories.get_category_by_id(url + f":{CATEGORIES_PORT}"),
        "27": lambda url: categories.add_new_category(url + f":{CATEGORIES_PORT}"),
        "28": lambda url: categories.delete_category(url + f":{CATEGORIES_PORT}"),
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
        print("21: Get all admins")
        print("22: Get admin by ID")
        print("23: Add new admin")
        print("24: Delete admin")
        print("25: Get all categories")
        print("26: Get category by ID")
        print("27: Add new category")
        print("28: Delete category")

        command = input("Enter a command: ")
        base_url = "http://localhost"

        if command == "0":
            continueToLoop = False
        elif command in command_map:
            command_map[command](base_url)
        else:
            print("Invalid Input, Try again.")


if __name__ == "__main__":
    driver()

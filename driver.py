import requests
import json
import vendors
import inventory  # Add this import

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
        print("8: ")
        print("9: ")
        print("10: ")
        print("11: ")
        print("13: Get all inventory")
        print("14: Get inventory by ID")
        print("15: Add inventory item")
        print("16: Remove inventory item")

        command = input("Enter a command: ")
        base_url = "http://localhost:8000"

        if command == "0":
            continueToLoop = False
        elif command == "1":
            vendors.get_all_vendors(base_url)
        elif command == "2":
            vendors.get_vendor_by_id(base_url)
        elif command == "3":
            vendors.add_new_vendor(base_url)
        elif command == "4":
            vendors.delete_vendor(base_url)
        elif command == "13":
            inventory.get_all_inventory()
        elif command == "14":
            product_id = input("Enter product ID: ")
            inventory.get_inventory_by_id(product_id)
        elif command == "15":
            category_id = int(input("Category ID: "))
            product_code = input("Product code: ")
            product_name = input("Product name: ")
            description = input("Description: ")
            list_price = float(input("List price: "))
            inv = int(input("Inventory: "))
            discount_percent = float(input("Discount percent (default 0.0): ") or 0.0)
            inventory.add_inventory(category_id, product_code, product_name, description, list_price, inv, discount_percent)
        elif command == "16":
            product_id = input("Enter product ID to remove: ")
            inventory.remove_inventory(product_id)
        else:
            print("Invalid Input, Try again.")

if __name__ == "__main__":
    driver()
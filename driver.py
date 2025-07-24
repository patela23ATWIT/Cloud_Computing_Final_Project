import requests
import json
import vendors

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
        else:
            print("Invalid Input, Try again.")

if __name__ == "__main__":
    driver()
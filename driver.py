import requests
import json

def driver():
    print("Welcome to the Guitar Shop FastAPI Driver!")

    continueToLoop = True

    while continueToLoop:
        print("\nSelect a command to test:")
        print("0: Exit")
        print("1: ")
        print("2: ")
        print("3: ")
        print("4: ")
        print("5: ")
        print("6: ")
        print("7: ")
        print("8: ")
        print("9: ")
        print("10: ")
        print("11: ")

        command = input("Enter a command: ")
        base_url = "http://localhost:8000"


        if command == "0":
            continueToLoop = False
        elif command == "1":
            print("EXAMPLE 1")
        else:
            print("Invalid Input, Try again.")


if __name__ == "__main__":
    driver()

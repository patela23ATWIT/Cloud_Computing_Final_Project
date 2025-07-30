import requests

def get_all_categories(base_url):
    # Get all categories
    print("\n=== Getting all categories ===")
    try:
        response = requests.get(f"{base_url}/categories")
        if response.status_code == 200:
            categories = response.json()
            print("Categories found:")
            for category in categories["categories"]:
                print(f"ID: {category['category_id']}, Name: {category['category_name']}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def get_category_by_id(base_url):
    # Get category by ID
    print("\n=== Get category by ID ===")
    category_id = input("Enter category ID: ")
    try:
        response = requests.get(f"{base_url}/categories/{category_id}")
        if response.status_code == 200:
            category = response.json()["category"]
            print(f"Category found:")
            print(f"ID: {category['category_id']}")
            print(f"Name: {category['category_name']}")
        elif response.status_code == 404:
            print(f"Category with ID {category_id} not found")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def add_new_category(base_url):
    # Add new category
    print("\n=== Add new category ===")
    category_name = input("Enter category name: ")
    
    category_data = {
        "category_name": category_name
    }
    
    try:
        response = requests.put(f"{base_url}/categories", json=category_data)
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result['message']}")
            print(f"New category ID: {result['category_id']}")
        elif response.status_code == 400:
            print(f"Error: Category '{category_name}' already exists")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def delete_category(base_url):
    # Delete category
    print("\n=== Delete category ===")
    category_id = input("Enter category ID to delete: ")
    confirm = input(f"Are you sure you want to delete category {category_id}? (y/n): ")
    
    if confirm.lower() == 'y':
        try:
            response = requests.delete(f"{base_url}/categories/{category_id}")
            if response.status_code == 200:
                result = response.json()
                print(f"Success: {result['message']}")
            elif response.status_code == 404:
                print(f"Category with ID {category_id} not found")
            elif response.status_code == 400:
                print(f"Error: {response.text}")
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
    else:
        print("Delete operation cancelled")

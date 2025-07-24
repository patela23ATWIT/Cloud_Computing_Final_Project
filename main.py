from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel
from typing import Optional
import mysql.connector
import os

app = FastAPI()

class Product(BaseModel):
    category_id: int
    product_code: str
    product_name: str
    description: Optional[str] = None
    list_price: float
    inventory: int
    discount_percent: float

class Customer(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class Address(BaseModel):
    line1: str
    city: str
    state: str
    zip_code: str

class Vendor(BaseModel):
    vendor_name: str
    product_id: int

# Database connection
def connect_to_db():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("MYSQL_PASSWORD", ""),
            database="my_sporting_shop"
        )
        print("Successfully connected to MySQL database!")

    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")

    return mydb


# Get Query string parameter: /
@app.get("/")
async def root():
    return {"message": "Welcome to the Sporting Shop!"}

# VENDOR MANAGEMENT ENDPOINTS
# GET /vendors - Get all vendors
@app.get("/vendors")
async def get_vendors():
    mydb = connect_to_db()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM vendors"
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row)
    cursor.close()
    mydb.close()
    return {"vendors": results}

# GET /vendors/{vendor_id} - Get a specific vendor by ID
@app.get("/vendors/{vendor_id}")
async def get_vendor(vendor_id: int):
    mydb = connect_to_db()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM vendors WHERE vendor_id = %s"
    cursor.execute(query, (vendor_id,))
    result = cursor.fetchone()
    cursor.close()
    mydb.close()
    
    if result is None:
        raise HTTPException(status_code=404, detail=f"Vendor with ID {vendor_id} not found")
    return {"vendor": result}

# PUT /vendors - Add a new vendor
@app.put("/vendors")
async def add_vendor(vendor: Vendor):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    
    # First check if the product exists
    check_query = "SELECT product_id FROM products WHERE product_id = %s"
    cursor.execute(check_query, (vendor.product_id,))
    if cursor.fetchone() is None:
        cursor.close()
        mydb.close()
        raise HTTPException(status_code=404, detail=f"Product with ID {vendor.product_id} not found")
    
    query = """
        INSERT INTO vendors (product_id, vendor_name)
        VALUES (%s, %s)
    """
    cursor.execute(query, (
        vendor.product_id,
        vendor.vendor_name
    ))
    mydb.commit()
    vendor_id = cursor.lastrowid
    cursor.close()
    mydb.close()
    return {"message": f"Vendor added successfully", "vendor_id": vendor_id}

# DELETE /vendors/{vendor_id} - Remove a vendor
@app.delete("/vendors/{vendor_id}")
async def delete_vendor(vendor_id: int):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    
    # First check if vendor exists
    check_query = "SELECT vendor_id FROM vendors WHERE vendor_id = %s"
    cursor.execute(check_query, (vendor_id,))
    if cursor.fetchone() is None:
        cursor.close()
        mydb.close()
        raise HTTPException(status_code=404, detail=f"Vendor with ID {vendor_id} not found")
    
    query = "DELETE FROM vendors WHERE vendor_id = %s"
    cursor.execute(query, (vendor_id,))
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": f"Vendor {vendor_id} deleted successfully"}

# PRODUCT MANAGEMENT ENDPOINTS
# GET /products - Get all products
@app.get("/products")
async def get_products():
    mydb = connect_to_db()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM products"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    mydb.close()
    return {"products": results}

# GET /products/{product_code} - Get a specific product by code
@app.get("/products/{product_code}")
async def get_product(product_code: str):
    mydb = connect_to_db()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM products WHERE product_code = %s"
    cursor.execute(query, (product_code,))
    result = cursor.fetchone()
    cursor.close()
    mydb.close()
    if result is None:
        raise HTTPException(status_code=404, detail=f"Product with code {product_code} not found")
    return {"product": result}

# PUT /products - Add a new product
@app.put("/products")
async def add_product(product: Product):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    
    # First check if the category exists
    check_query = "SELECT category_id FROM categories WHERE category_id = %s"
    cursor.execute(check_query, (product.category_id,))
    if cursor.fetchone() is None:
        cursor.close()
        mydb.close()
        raise HTTPException(status_code=404, detail=f"Category with ID {product.category_id} not found")
    
    # Check if product code already exists
    code_check_query = "SELECT product_id FROM products WHERE product_code = %s"
    cursor.execute(code_check_query, (product.product_code,))
    if cursor.fetchone() is not None:
        cursor.close()
        mydb.close()
        raise HTTPException(status_code=400, detail=f"Product with code {product.product_code} already exists")

    query = """
        INSERT INTO products (category_id, product_code, product_name, description, list_price, inventory, discount_percent)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        product.category_id,
        product.product_code,
        product.product_name,
        product.description,
        product.list_price,
        product.inventory,
        product.discount_percent
    ))
    mydb.commit()
    product_id = cursor.lastrowid
    cursor.close()
    mydb.close()
    return {"message": f"Product added successfully", "product_id": product_id}

# DELETE /products/{product_code} - Remove a product
@app.delete("/products/{product_code}")
async def delete_product(product_code: str):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    
    # First check if product exists
    check_query = "SELECT product_id FROM products WHERE product_code = %s"
    cursor.execute(check_query, (product_code,))
    result = cursor.fetchone()
    if result is None:
        cursor.close()
        mydb.close()
        raise HTTPException(status_code=404, detail=f"Product with code {product_code} not found")
    
    product_id = result[0]
    
    # Delete product records in proper order to avoid foreign key constraints
    # Delete order items that reference this product
    delete_order_items_query = "DELETE FROM order_items WHERE product_id = %s"
    cursor.execute(delete_order_items_query, (product_id,))
    
    # Delete vendors that reference this product
    delete_vendors_query = "DELETE FROM vendors WHERE product_id = %s"
    cursor.execute(delete_vendors_query, (product_id,))
    
    # Delete the product
    delete_product_query = "DELETE FROM products WHERE product_code = %s"
    cursor.execute(delete_product_query, (product_code,))
    
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": f"Product {product_code} and all related records deleted successfully"}

# CUSTOMER MANAGEMENT ENDPOINTS
# GET /customers - Get all customers
@app.get("/customers")
async def get_customers():
    mydb = connect_to_db()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM customers"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    mydb.close()
    return {"customers": results}

# GET /customers/{customer_id} - Get a specific customer by ID
@app.get("/customers/{customer_id}")
async def get_customer(customer_id: int):
    mydb = connect_to_db()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM customers WHERE customer_id = %s"
    cursor.execute(query, (customer_id,))
    result = cursor.fetchone()
    cursor.close()
    mydb.close()
    
    if result is None:
        raise HTTPException(status_code=404, detail=f"Customer with ID {customer_id} not found")
    return {"customer": result}

# PUT /customers - Add a new customer
@app.put("/customers")
async def add_customer(customer: Customer):
    mydb = connect_to_db()
    cursor = mydb.cursor()

    # First check if the email already exists
    check_query = "SELECT customer_id FROM customers WHERE email_address = %s"
    cursor.execute(check_query, (customer.email,))
    if cursor.fetchone() is not None:
        cursor.close()
        mydb.close()
        raise HTTPException(status_code=400, detail=f"Customer with email {customer.email} already exists")

    query = """
        INSERT INTO customers (email_address, password, first_name, last_name)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (
        customer.email,
        customer.password,
        customer.first_name,
        customer.last_name
    ))
    mydb.commit()
    customer_id = cursor.lastrowid
    cursor.close()
    mydb.close()
    return {"message": f"Customer added successfully", "customer_id": customer_id}

# DELETE /customers/{customer_id} - Remove a customer
@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    
    # First check if customer exists
    check_query = "SELECT customer_id FROM customers WHERE customer_id = %s"
    cursor.execute(check_query, (customer_id,))
    if cursor.fetchone() is None:
        cursor.close()
        mydb.close()
        raise HTTPException(status_code=404, detail=f"Customer with ID {customer_id} not found")
    
    # Delete customer records in proper order to avoid foreign key constraints
    # Delete order_items for all orders of this customer
    delete_order_items_query = """
        DELETE oi FROM order_items oi
        INNER JOIN orders o ON oi.order_id = o.order_id
        WHERE o.customer_id = %s
    """
    cursor.execute(delete_order_items_query, (customer_id,))
    
    # Delete orders for this customer
    delete_orders_query = "DELETE FROM orders WHERE customer_id = %s"
    cursor.execute(delete_orders_query, (customer_id,))
    
    # Delete addresses for this customer
    delete_addresses_query = "DELETE FROM addresses WHERE customer_id = %s"
    cursor.execute(delete_addresses_query, (customer_id,))
    
    # Delete the customer
    delete_customer_query = "DELETE FROM customers WHERE customer_id = %s"
    cursor.execute(delete_customer_query, (customer_id,))
    
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": f"Customer {customer_id} and all related records deleted successfully"}
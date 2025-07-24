from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import mysql.connector
import os

app = FastAPI()

# In-memory "database" for demonstration
inventory_db = []
product_id_counter = 1

class Product(BaseModel):
    product_id: Optional[int] = None
    category_id: int
    product_code: str
    product_name: str
    description: str
    list_price: float
    inventory: int
    discount_percent: float = 0.0

class Customer(BaseModel):
    first_name: str
    last_name: str
    email: str

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
        return mydb  # <-- Move this inside the try block!
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None  # Explicitly return None if connection fails


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
@app.get("/inventory")
def get_all_inventory():
    mydb = None
    cursor = None
    try:
        mydb = connect_to_db()
        cursor = mydb.cursor(dictionary=True)
        query = "SELECT * FROM products"
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(row)
        return {"inventory": results}
    finally:
        if cursor:
            cursor.close()
        if mydb:
            mydb.close()

@app.get("/inventory/{product_id}")
def get_inventory_by_id(product_id: int):
    mydb = None
    cursor = None
    try:
        mydb = connect_to_db()
        cursor = mydb.cursor(dictionary=True)
        query = "SELECT * FROM products WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        result = cursor.fetchone()
        print(result)
        if result:
            return {"product": result}
        raise HTTPException(status_code=404, detail="Product not found")
    finally:
        if cursor:
            cursor.close()
        if mydb:
            mydb.close()

@app.post("/inventory", status_code=201)
def add_inventory(product: Product):
    mydb = None
    cursor = None
    try:
        mydb = connect_to_db()
        cursor = mydb.cursor()
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
        print({"message": "Product added", "product_id": product_id})
        return {"message": "Product added", "product_id": product_id}
    finally:
        if cursor:
            cursor.close()
        if mydb:
            mydb.close()

@app.delete("/inventory/{product_id}")
def remove_inventory(product_id: int):
    mydb = None
    cursor = None
    try:
        mydb = connect_to_db()
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        print(product)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        mydb.commit()
        return {"message": "Product removed", "product_id": product_id}
    finally:
        if cursor:
            cursor.close()
        if mydb:
            mydb.close()
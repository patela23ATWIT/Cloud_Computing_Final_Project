from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel
from typing import Optional
import mysql.connector
import os

app = FastAPI()

class Product(BaseModel):
    product_code: str
    product_name: str
    list_price: float
    discount_percent: float

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
#
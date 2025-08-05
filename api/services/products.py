from api.db import connect_to_db
from fastapi import HTTPException, FastAPI, Header
from api.types import Product
from api.auth import verify_cookie

app = FastAPI()

# PRODUCT MANAGEMENT ENDPOINTS
# GET /products - Get all products
@app.get("/products")
async def get_products(
    email_address: str = Header(..., alias="X-Email-Address"),
    cookie: str = Header(..., alias="X-Session-Cookie"),
):
    if not await verify_cookie(email_address, cookie):
        raise HTTPException(status_code=401, detail="Invalid or expired cookie")
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
async def get_product(
    product_code: str,
    email_address: str = Header(..., alias="X-Email-Address"),
    cookie: str = Header(..., alias="X-Session-Cookie"),
):
    if not await verify_cookie(email_address, cookie):
        raise HTTPException(status_code=401, detail="Invalid or expired cookie")
    mydb = connect_to_db()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM products WHERE product_code = %s"
    cursor.execute(query, (product_code,))
    result = cursor.fetchone()
    cursor.close()
    mydb.close()
    if result is None:
        raise HTTPException(
            status_code=404, detail=f"Product with code {product_code} not found"
        )
    return {"product": result}


# PUT /products - Add a new product
@app.put("/products")
async def add_product(
    product: Product,
    email_address: str = Header(..., alias="X-Email-Address"),
    cookie: str = Header(..., alias="X-Session-Cookie"),
):
    if not await verify_cookie(email_address, cookie):
        raise HTTPException(status_code=401, detail="Invalid or expired cookie")
    mydb = connect_to_db()
    cursor = mydb.cursor()

    # First check if the category exists
    check_query = "SELECT category_id FROM categories WHERE category_id = %s"
    cursor.execute(check_query, (product.category_id,))
    if cursor.fetchone() is None:
        cursor.close()
        mydb.close()
        raise HTTPException(
            status_code=404, detail=f"Category with ID {product.category_id} not found"
        )

    # Check if product code already exists
    code_check_query = "SELECT product_id FROM products WHERE product_code = %s"
    cursor.execute(code_check_query, (product.product_code,))
    if cursor.fetchone() is not None:
        cursor.close()
        mydb.close()
        raise HTTPException(
            status_code=400,
            detail=f"Product with code {product.product_code} already exists",
        )

    query = """
        INSERT INTO products (category_id, product_code, product_name, description, list_price, inventory, discount_percent)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(
        query,
        (
            product.category_id,
            product.product_code,
            product.product_name,
            product.description,
            product.list_price,
            product.inventory,
            product.discount_percent,
        ),
    )
    mydb.commit()
    product_id = cursor.lastrowid
    cursor.close()
    mydb.close()
    return {"message": f"Product added successfully", "product_id": product_id}


# DELETE /products/{product_code} - Remove a product
@app.delete("/products/{product_code}")
async def delete_product(
    product_code: str,
    email_address: str = Header(..., alias="X-Email-Address"),
    cookie: str = Header(..., alias="X-Session-Cookie"),
):
    if not await verify_cookie(email_address, cookie):
        raise HTTPException(status_code=401, detail="Invalid or expired cookie")
    mydb = connect_to_db()
    cursor = mydb.cursor()

    # First check if product exists
    check_query = "SELECT product_id FROM products WHERE product_code = %s"
    cursor.execute(check_query, (product_code,))
    result = cursor.fetchone()
    if result is None:
        cursor.close()
        mydb.close()
        raise HTTPException(
            status_code=404, detail=f"Product with code {product_code} not found"
        )

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
    return {
        "message": f"Product {product_code} and all related records deleted successfully"
    }


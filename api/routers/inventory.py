from api.db import connect_to_db
from fastapi import HTTPException, APIRouter
from api.types import Product

router = APIRouter()


@router.get("/inventory")
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


@router.get("/inventory/{product_id}")
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


@router.post("/inventory", status_code=201)
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
        print({"message": "Product added", "product_id": product_id})
        return {"message": "Product added", "product_id": product_id}
    finally:
        if cursor:
            cursor.close()
        if mydb:
            mydb.close()


@router.delete("/inventory/{product_id}")
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

from api.db import connect_to_db
from fastapi import HTTPException, FastAPI
from api.types import Order
from fastapi import HTTPException, FastAPI, Header
from api.auth import verify_cookie

app = FastAPI()

# ORDER MANAGEMENT ENDPOINTS
# GET /orders - Get all orders
@app.get("/orders")
async def get_orders(email_address: str = Header(..., alias="X-Email-Address"),
    cookie: str = Header(..., alias="X-Session-Cookie"),
):
    if not await verify_cookie(email_address, cookie):
        raise HTTPException(status_code=401, detail="Invalid or expired cookie")
    mydb = connect_to_db()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM orders"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    mydb.close()
    return {"orders": results}


# GET /orders/{order_id} - Get a specific order by ID
@app.get("/orders/{order_id}")
async def get_order(order_id: int,email_address: str = Header(..., alias="X-Email-Address"),
    cookie: str = Header(..., alias="X-Session-Cookie"),
):
    if not await verify_cookie(email_address, cookie):
        raise HTTPException(status_code=401, detail="Invalid or expired cookie")
    mydb = connect_to_db()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM orders WHERE order_id = %s"
    cursor.execute(query, (order_id,))
    result = cursor.fetchone()
    cursor.close()
    mydb.close()

    if result is None:
        raise HTTPException(
            status_code=404, detail=f"Order with ID {order_id} not found"
        )
    return {"order": result}


# PUT /orders - Add a new order
@app.put("/orders")
async def add_order(order: Order,email_address: str = Header(..., alias="X-Email-Address"),
    cookie: str = Header(..., alias="X-Session-Cookie"),
):
    if not await verify_cookie(email_address, cookie):
        raise HTTPException(status_code=401, detail="Invalid or expired cookie")
    mydb = connect_to_db()
    cursor = mydb.cursor()

    # First check if the customer exists
    check_query = "SELECT customer_id FROM customers WHERE customer_id = %s"
    cursor.execute(check_query, (order.customer_id,))
    if cursor.fetchone() is None:
        cursor.close()
        mydb.close()
        raise HTTPException(
            status_code=404, detail=f"Customer with ID {order.customer_id} not found"
        )

    query = """
        INSERT INTO orders (customer_id, order_date, ship_amount, ship_address_id, card_number, billing_address_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(
        query,
        (
            order.customer_id,
            order.order_date,
            order.ship_amount,
            order.ship_address_id,
            order.card_number,
            order.billing_address_id,
        ),
    )
    mydb.commit()
    order_id = cursor.lastrowid
    cursor.close()
    mydb.close()
    return {"message": f"Order added successfully", "order_id": order_id}


# DELETE /orders/{order_id} - Remove an order
@app.delete("/orders/{order_id}")
async def delete_order(order_id: int,email_address: str = Header(..., alias="X-Email-Address"),
    cookie: str = Header(..., alias="X-Session-Cookie"),
):
    if not await verify_cookie(email_address, cookie):
        raise HTTPException(status_code=401, detail="Invalid or expired cookie")
    mydb = connect_to_db()
    cursor = mydb.cursor()

    # First check if order exists
    check_query = "SELECT order_id FROM orders WHERE order_id = %s"
    cursor.execute(check_query, (order_id,))
    if cursor.fetchone() is None:
        cursor.close()
        mydb.close()
        raise HTTPException(
            status_code=404, detail=f"Order with ID {order_id} not found"
        )

    # Delete order records in proper order to avoid foreign key constraints
    # Delete order items for this order
    delete_order_items_query = "DELETE FROM order_items WHERE order_id = %s"
    cursor.execute(delete_order_items_query, (order_id,))

    # Delete the order
    delete_order_query = "DELETE FROM orders WHERE order_id = %s"
    cursor.execute(delete_order_query, (order_id,))

    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": f"Order {order_id} and all related records deleted successfully"}

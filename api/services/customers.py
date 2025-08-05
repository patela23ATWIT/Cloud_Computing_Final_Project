from api.db import connect_to_db
from fastapi import HTTPException, FastAPI, Header
from api.types import Customer
from api.auth import verify_cookie

app = FastAPI()


# CUSTOMER MANAGEMENT ENDPOINTS
# GET /customers - Get all customers
@app.get("/customers")
async def get_customers(
    email_address: str = Header(..., alias="X-Email-Address"),
    cookie: str = Header(..., alias="X-Session-Cookie"),
):
    if not await verify_cookie(email_address, cookie):
        raise HTTPException(status_code=401, detail="Invalid or expired cookie")
    mydb = connect_to_db()
    if mydb is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM customers"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    mydb.close()
    return {"customers": results}


# GET /customers/{customer_id} - Get a specific customer by ID
@app.get("/customers/{customer_id}")
async def get_customer(
    customer_id: int,
    email_address: str = Header(..., alias="X-Email-Address"),
    cookie: str = Header(..., alias="X-Session-Cookie"),
):
    if not await verify_cookie(email_address, cookie):
        raise HTTPException(status_code=401, detail="Invalid or expired cookie")
    mydb = connect_to_db()
    if mydb is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM customers WHERE customer_id = %s"
    cursor.execute(query, (customer_id,))
    result = cursor.fetchone()
    cursor.close()
    mydb.close()

    if result is None:
        raise HTTPException(
            status_code=404, detail=f"Customer with ID {customer_id} not found"
        )
    return {"customer": result}


# PUT /customers - Add a new customer
@app.put("/customers")
async def add_customer(
    customer: Customer,
    email_address: str = Header(..., alias="X-Email-Address"),
    cookie: str = Header(..., alias="X-Session-Cookie"),
):
    if not await verify_cookie(email_address, cookie):
        raise HTTPException(status_code=401, detail="Invalid or expired cookie")
    mydb = connect_to_db()
    if mydb is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    cursor = mydb.cursor()

    # First check if the email already exists
    check_query = "SELECT customer_id FROM customers WHERE email_address = %s"
    cursor.execute(check_query, (customer.email,))
    if cursor.fetchone() is not None:
        cursor.close()
        mydb.close()
        raise HTTPException(
            status_code=400,
            detail=f"Customer with email {customer.email} already exists",
        )

    query = """
        INSERT INTO customers (email_address, password, first_name, last_name)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(
        query,
        (customer.email, customer.password, customer.first_name, customer.last_name),
    )
    mydb.commit()
    customer_id = cursor.lastrowid
    cursor.close()
    mydb.close()
    return {"message": f"Customer added successfully", "customer_id": customer_id}


# DELETE /customers/{customer_id} - Remove a customer
@app.delete("/customers/{customer_id}")
async def delete_customer(
    customer_id: int,
    email_address: str = Header(..., alias="X-Email-Address"),
    cookie: str = Header(..., alias="X-Session-Cookie"),
):
    if not await verify_cookie(email_address, cookie):
        raise HTTPException(status_code=401, detail="Invalid or expired cookie")
    mydb = connect_to_db()
    if mydb is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    cursor = mydb.cursor()

    # First check if customer exists
    check_query = "SELECT customer_id FROM customers WHERE customer_id = %s"
    cursor.execute(check_query, (customer_id,))
    if cursor.fetchone() is None:
        cursor.close()
        mydb.close()
        raise HTTPException(
            status_code=404, detail=f"Customer with ID {customer_id} not found"
        )

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
    return {
        "message": f"Customer {customer_id} and all related records deleted successfully"
    }


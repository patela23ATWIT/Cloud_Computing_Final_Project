from fastapi import APIRouter, HTTPException
from api.types import Admin
from api.db import connect_to_db

router = APIRouter()

# GET /admins - Get all admins
@router.get("/admins")
async def get_admins():
    mydb = connect_to_db()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM administrators"
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row)
    cursor.close()
    mydb.close()
    return {"admins": results}

# GET /admins/{admin_id} - Get a specific admin by ID
@router.get("/admins/{admin_id}")
async def get_admin(admin_id: int):
    mydb = connect_to_db()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM administrators WHERE admin_id = %s"
    cursor.execute(query, (admin_id,))
    result = cursor.fetchone()
    cursor.close()
    mydb.close()
    
    if result is None:
        raise HTTPException(status_code=404, detail=f"Admin with ID {admin_id} not found")
    return {"admin": result}

# PUT /admins - Add a new admin
@router.put("/admins")
async def add_admin(admin: Admin):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    
    # First check if the email already exists
    check_query = "SELECT admin_id FROM administrators WHERE email_address = %s"
    cursor.execute(check_query, (admin.email_address,))
    if cursor.fetchone() is not None:
        cursor.close()
        mydb.close()
        raise HTTPException(status_code=400, detail=f"Admin with email {admin.email_address} already exists")
    
    query = """
        INSERT INTO administrators (email_address, password, first_name, last_name)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (
        admin.email_address,
        admin.password,
        admin.first_name,
        admin.last_name
    ))
    mydb.commit()
    admin_id = cursor.lastrowid
    cursor.close()
    mydb.close()
    return {"message": f"Admin added successfully", "admin_id": admin_id}

# DELETE /admins/{admin_id} - Remove an admin
@router.delete("/admins/{admin_id}")
async def delete_admin(admin_id: int):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    
    # First check if admin exists
    check_query = "SELECT admin_id FROM administrators WHERE admin_id = %s"
    cursor.execute(check_query, (admin_id,))
    if cursor.fetchone() is None:
        cursor.close()
        mydb.close()
        raise HTTPException(status_code=404, detail=f"Admin with ID {admin_id} not found")
    
    query = "DELETE FROM administrators WHERE admin_id = %s"
    cursor.execute(query, (admin_id,))
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": f"Admin {admin_id} deleted successfully"}

from api.db import connect_to_db
from fastapi import HTTPException, APIRouter
from api.types import Vendor

router = APIRouter()


# VENDOR MANAGEMENT ENDPOINTS
# GET /vendors - Get all vendors
@router.get("/vendors")
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
@router.get("/vendors/{vendor_id}")
async def get_vendor(vendor_id: int):
    mydb = connect_to_db()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM vendors WHERE vendor_id = %s"
    cursor.execute(query, (vendor_id,))
    result = cursor.fetchone()
    cursor.close()
    mydb.close()

    if result is None:
        raise HTTPException(
            status_code=404, detail=f"Vendor with ID {vendor_id} not found"
        )
    return {"vendor": result}


# PUT /vendors - Add a new vendor
@router.put("/vendors")
async def add_vendor(vendor: Vendor):
    mydb = connect_to_db()
    cursor = mydb.cursor()

    # First check if the product exists
    check_query = "SELECT product_id FROM products WHERE product_id = %s"
    cursor.execute(check_query, (vendor.product_id,))
    if cursor.fetchone() is None:
        cursor.close()
        mydb.close()
        raise HTTPException(
            status_code=404, detail=f"Product with ID {vendor.product_id} not found"
        )

    query = """
        INSERT INTO vendors (product_id, vendor_name)
        VALUES (%s, %s)
    """
    cursor.execute(query, (vendor.product_id, vendor.vendor_name))
    mydb.commit()
    vendor_id = cursor.lastrowid
    cursor.close()
    mydb.close()
    return {"message": f"Vendor added successfully", "vendor_id": vendor_id}


# DELETE /vendors/{vendor_id} - Remove a vendor
@router.delete("/vendors/{vendor_id}")
async def delete_vendor(vendor_id: int):
    mydb = connect_to_db()
    cursor = mydb.cursor()

    # First check if vendor exists
    check_query = "SELECT vendor_id FROM vendors WHERE vendor_id = %s"
    cursor.execute(check_query, (vendor_id,))
    if cursor.fetchone() is None:
        cursor.close()
        mydb.close()
        raise HTTPException(
            status_code=404, detail=f"Vendor with ID {vendor_id} not found"
        )

    query = "DELETE FROM vendors WHERE vendor_id = %s"
    cursor.execute(query, (vendor_id,))
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": f"Vendor {vendor_id} deleted successfully"}

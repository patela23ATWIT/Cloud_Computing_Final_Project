from fastapi import APIRouter, HTTPException
from api.types import Category
from api.db import connect_to_db

router = APIRouter()

# GET /categories - Get all categories
@router.get("/categories")
async def get_categories():
    mydb = connect_to_db()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM categories"
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row)
    cursor.close()
    mydb.close()
    return {"categories": results}

# GET /categories/{category_id} - Get a specific category by ID
@router.get("/categories/{category_id}")
async def get_category(category_id: int):
    mydb = connect_to_db()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM categories WHERE category_id = %s"
    cursor.execute(query, (category_id,))
    result = cursor.fetchone()
    cursor.close()
    mydb.close()
    
    if result is None:
        raise HTTPException(status_code=404, detail=f"Category with ID {category_id} not found")
    return {"category": result}

# PUT /categories - Add a new category
@router.put("/categories")
async def add_category(category: Category):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    
    # First check if the category name already exists
    check_query = "SELECT category_id FROM categories WHERE category_name = %s"
    cursor.execute(check_query, (category.category_name,))
    if cursor.fetchone() is not None:
        cursor.close()
        mydb.close()
        raise HTTPException(status_code=400, detail=f"Category '{category.category_name}' already exists")
    
    query = """
        INSERT INTO categories (category_name)
        VALUES (%s)
    """
    cursor.execute(query, (category.category_name,))
    mydb.commit()
    category_id = cursor.lastrowid
    cursor.close()
    mydb.close()
    return {"message": f"Category added successfully", "category_id": category_id}

# DELETE /categories/{category_id} - Remove a category
@router.delete("/categories/{category_id}")
async def delete_category(category_id: int):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    
    # First check if category exists
    check_query = "SELECT category_id, category_name FROM categories WHERE category_id = %s"
    cursor.execute(check_query, (category_id,))
    category_result = cursor.fetchone()
    if category_result is None:
        cursor.close()
        mydb.close()
        raise HTTPException(status_code=404, detail=f"Category with ID {category_id} not found")
    
    category_name = category_result[1]
    
    # Check if any products exist in this category
    products_check_query = "SELECT COUNT(*) FROM products WHERE category_id = %s"
    cursor.execute(products_check_query, (category_id,))
    product_count = cursor.fetchone()[0]
    
    if product_count > 0:
        cursor.close()
        mydb.close()
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete category '{category_name}'. {product_count} products are still assigned to this category. Please reassign or delete these products first."
        )
    
    # Delete the category
    query = "DELETE FROM categories WHERE category_id = %s"
    cursor.execute(query, (category_id,))
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": f"Category '{category_name}' deleted successfully"}

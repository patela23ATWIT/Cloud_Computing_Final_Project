from fastapi import FastAPI, Query, Path, HTTPException
from api.types import *
from api.routers.vendors import router as vendor_router
from api.routers.products import router as product_router
from api.routers.customers import router as customer_router
from api.routers.orders import router as order_router
from api.routers.inventory import router as inventory_router
from api.routers.admins import router as admin_router
from api.routers.categories import router as category_router


app = FastAPI()

# In-memory "database" for demonstration
inventory_db = []
product_id_counter = 1


# Get Query string parameter: /
@app.get("/")
async def root():
    return {"message": "Welcome to the Sporting Shop!"}


# add routers
app.include_router(vendor_router)
app.include_router(product_router)
app.include_router(customer_router)
app.include_router(order_router)
app.include_router(inventory_router)
app.include_router(admin_router)
app.include_router(category_router)
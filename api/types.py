from pydantic import BaseModel
from typing import Optional, List

class Product(BaseModel):
    product_id: Optional[int] = None
    category_id: int
    product_code: str
    product_name: str
    description: Optional[str] = None
    list_price: float
    inventory: int
    discount_percent: float = 0.0


class Customer(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class Address(BaseModel):
    line1: str
    city: str
    state: str
    zip_code: str


class Vendor(BaseModel):
    vendor_name: str
    product_id: int


class Order(BaseModel):
    customer_id: int
    order_date: str
    ship_amount: float
    ship_address_id: int
    card_number: str
    billing_address_id: int
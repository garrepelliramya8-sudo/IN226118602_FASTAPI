from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Product Model
class Product(BaseModel):
    id: int
    name: str
    price: int
    category: str
    in_stock: bool


# Initial Data
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Keyboard", "price": 799, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 599, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 199, "category": "Stationery", "in_stock": True}
]

# ==============================
# Q1 — POST /products
# ==============================
@app.post("/products", status_code=201)
def add_product(product: Product):

    for p in products:
        if p["name"].lower() == product.name.lower():
            raise HTTPException(status_code=400, detail="Product already exists")

    products.append(product.dict())

    return {
        "message": "Product added successfully",
        "product": product
    }


# ==============================
# Q5 — GET /products/audit
# MUST BE ABOVE /products/{product_id}
# ==============================
@app.get("/products/audit")
def audit_products():

    total_products = len(products)

    in_stock = len([p for p in products if p["in_stock"]])
    out_stock = len([p for p in products if not p["in_stock"]])

    total_stock_value = sum(p["price"] for p in products)

    most_expensive = max(products, key=lambda x: x["price"])

    return {
        "total_products": total_products,
        "in_stock": in_stock,
        "out_of_stock": out_stock,
        "total_stock_value": total_stock_value,
        "most_expensive_product": most_expensive
    }


# ==============================
#  BONUS — PUT /products/discount
# MUST BE ABOVE /products/{product_id}
# ==============================
@app.put("/products/discount")
def apply_discount(category: str, discount_percent: int):

    updated_products = []

    for p in products:
        if p["category"].lower() == category.lower():

            discount_amount = p["price"] * (discount_percent / 100)
            p["price"] = int(p["price"] - discount_amount)

            updated_products.append(p)

    return {
        "message": f"{discount_percent}% discount applied to {category}",
        "updated_products": updated_products
    }


# ==============================
# Q2 — PUT /products/{product_id}
# ==============================
@app.put("/products/{product_id}")
def update_product(product_id: int, price: Optional[int] = None, in_stock: Optional[bool] = None):

    for p in products:
        if p["id"] == product_id:

            if price is not None:
                p["price"] = price

            if in_stock is not None:
                p["in_stock"] = in_stock

            return {
                "message": "Product updated successfully",
                "product": p
            }

    raise HTTPException(status_code=404, detail="Product not found")


# ==============================
# Q3 — DELETE /products/{product_id}
# ==============================
@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    for p in products:
        if p["id"] == product_id:
            products.remove(p)

            return {
                "message": f"{p['name']} removed successfully"
            }

    raise HTTPException(status_code=404, detail="Product not found")


# ==============================
# Q4 — GET /products/{product_id}
# ==============================
@app.get("/products/{product_id}")
def get_product(product_id: int):

    for p in products:
        if p["id"] == product_id:
            return p

    raise HTTPException(status_code=404, detail="Product not found")

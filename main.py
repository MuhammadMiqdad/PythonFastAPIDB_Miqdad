from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from typing import List

app = FastAPI()

# In-memory store
products = {}

class Product(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(ge=0)
    stock: int = Field(ge=0)
    category: str = Field(min_length=1)

class ProductData(Product):
    id: UUID

class ProductResponse(BaseModel):
    message: str
    product: ProductData

# CREATE product
@app.post("/products", response_model=ProductResponse)
def add_product(product: Product):
    product_id = str(uuid4())
    products[product_id] = product.dict()
    return {
        "message": "Product created successfully",
        "product": {
            "id": UUID(product_id),
            **products[product_id]
        }
    }

# READ all products
@app.get("/products", response_model=List[ProductData])
def get_all_products():
    return [{"id": UUID(pid), **pdata} for pid, pdata in products.items()]

# READ product by ID
@app.get("/products/{product_id}", response_model=ProductData)
def get_product(product_id: UUID):
    pid = str(product_id)
    product = products.get(pid)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"id": product_id, **product}

# UPDATE product
@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: UUID, updated: Product):
    pid = str(product_id)
    if pid not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    products[pid] = updated.dict()
    return {
        "message": "Product updated successfully",
        "product": {
            "id": product_id,
            **products[pid]
        }
    }

# DELETE product
@app.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product(product_id: UUID):
    pid = str(product_id)
    product = products.get(pid)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    deleted_data = {
        "message": "Product deleted successfully",
        "product": {
            "id": product_id,
            **product
        }
    }

    del products[pid]
    return deleted_data

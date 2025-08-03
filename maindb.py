from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from typing import List

from database import SessionLocal, engine
import models

# Inisialisasi FastAPI
app = FastAPI()

# Buat tabel jika belum ada
models.Base.metadata.create_all(bind=engine)

# Dependency untuk koneksi DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SCHEMAS
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

# ROUTES
# CREATE
@app.post("/products", response_model=ProductResponse)
def create_product(product: Product, db: Session = Depends(get_db)):
    new_product = models.ProductModel(
        id=str(uuid4()),
        name=product.name,
        price=product.price,
        stock=product.stock,
        category=product.category
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {
        "message": "Product created successfully",
        "product": new_product
    }

# READ all
@app.get("/products", response_model=List[ProductData])
def get_all_products(db: Session = Depends(get_db)):
    return db.query(models.ProductModel).all()

# READ by ID
@app.get("/products/{product_id}", response_model=ProductData)
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    product = db.query(models.ProductModel).filter(models.ProductModel.id == str(product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# UPDATE
@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: UUID, updated: Product, db: Session = Depends(get_db)):
    product = db.query(models.ProductModel).filter(models.ProductModel.id == str(product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.name = updated.name
    product.price = updated.price
    product.stock = updated.stock
    product.category = updated.category
    db.commit()
    db.refresh(product)
    return {
        "message": "Product updated successfully",
        "product": product
    }

# DELETE
@app.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product(product_id: UUID, db: Session = Depends(get_db)):
    product = db.query(models.ProductModel).filter(models.ProductModel.id == str(product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {
        "message": "Product deleted successfully",
        "product": product
    }
from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.dialects.mysql import CHAR
from uuid import uuid4
from database import Base

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    category = Column(String(100), nullable=False)
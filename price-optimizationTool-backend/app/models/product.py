from sqlalchemy import Column, Integer, String, Float,  DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)  # FK to Category table
    cost_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    stock_available = Column(Integer, nullable=False)
    units_sold = Column(Integer, default=0)
    customer_rating = Column(Float, default=0.0)
    demand_forecast = Column(Float, nullable=True)
    optimized_price = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    updated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    category = relationship("Category", back_populates="products")
class Category(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(255), nullable=False)
    profit_margin = Column(Float, nullable=False)
    # products = relationship("Product", back_populates="category")
    products = relationship("Product", back_populates="category")

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int
    cost_price: float
    selling_price: float
    stock_available: int
    units_sold: Optional[int] = 0
    customer_rating: Optional[float] = 0.0
    created_by_user_id: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    cost_price: Optional[float] = None
    selling_price: Optional[float] = None
    stock_available: Optional[int] = None
    units_sold: Optional[int] = None
    customer_rating: Optional[float] = None
    demand_forecast: Optional[float] = None
    optimized_price: Optional[float] = None
    updated_by_user_id: int

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    category_id: int
    cost_price: float
    selling_price: float
    stock_available: int
    units_sold: int
    customer_rating: float
    demand_forecast: Optional[float] = None
    optimized_price: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by_user_id: int
    updated_by_user_id: Optional[int] = None

    class Config:
        orm_mode = True
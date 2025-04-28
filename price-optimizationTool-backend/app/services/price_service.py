import math
from sqlalchemy.orm import Session
from app.models.product import Product, Category
from app.core.constants import (
    DEFAULT_MARGIN_FACTOR,
    MIN_PROFIT_MARGIN,
    DEMAND_ELASTICITY_EXP
)

def calculate_optimized_price(product: Product, db: Session) -> float:
    category_obj = db.query(Category).filter(Category.category_id == product.category_id).first()
    margin_factor = category_obj.profit_margin if category_obj else DEFAULT_MARGIN_FACTOR

    if product.units_sold == 0:
        return round(product.cost_price * margin_factor, 2)

    demand_ratio = product.demand_forecast / max(product.units_sold, 1)
    demand_adjustment = math.pow(demand_ratio, DEMAND_ELASTICITY_EXP)

    optimized_price = product.cost_price * margin_factor * demand_adjustment
    min_price = product.cost_price * MIN_PROFIT_MARGIN

    return round(min(max(optimized_price, min_price), product.selling_price), 2)

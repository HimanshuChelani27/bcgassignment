import math
from sqlalchemy.orm import Session
from app.models.product import Product
from app.core.constants import (
    DEFAULT_AVG_SALES,
    SEASONAL_FACTOR,
    BASE_PRICE_MULTIPLIER
)

def calculate_demand_forecast(product: Product, db: Session) -> int:
    if product.units_sold == 0:
        similar_products = db.query(Product).filter(
            Product.category == product.category,
            Product.units_sold > 0
        ).all()
        if similar_products:
            total_sales = sum(p.units_sold for p in similar_products)
            avg_sales = total_sales / len(similar_products)
        else:
            avg_sales = DEFAULT_AVG_SALES
        return round(avg_sales * SEASONAL_FACTOR)
    else:
        base_price = product.cost_price * BASE_PRICE_MULTIPLIER
        price_elasticity = math.sqrt(base_price / max(product.selling_price, 0.01))
        forecast = product.units_sold * SEASONAL_FACTOR * price_elasticity
        return round(forecast)

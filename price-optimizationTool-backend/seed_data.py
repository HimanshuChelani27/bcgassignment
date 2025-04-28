from app.database import SessionLocal
from app.models.product import Product, Category
from app.models.roles import Role
from app.models.users import User
from datetime import datetime
import bcrypt

db = SessionLocal()

# Helper to hash passwords
def hash_password(plain_password):
    return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def seed_data():
    try:
        # Seed Roles
        if not db.query(Role).first():
            roles = [
                Role(name="admin"),
                Role(name="buyer"),
                Role(name="supplier"),
            ]
            db.add_all(roles)
            db.commit()
            print("✅ Roles seeded.")

        # Fetch roles for FK
        role_map = {role.name: role.id for role in db.query(Role).all()}

        # Seed Users
        if not db.query(User).first():
            users = [
                User(email="admin@example.com", password=hash_password("demo@123"), role_id=role_map["admin"], is_verified=True, name="Admin User"),
                User(email="buyer@example.com", password=hash_password("demo@123"), role_id=role_map["buyer"], is_verified=True, name="Buyer User"),
                User(email="supplier@example.com", password=hash_password("demo@123"), role_id=role_map["supplier"], is_verified=True, name="Supplier User"),
            ]
            db.add_all(users)
            db.commit()
            print("✅ Users seeded.")

        # Fetch users for FK
        user_map = {user.email: user.id for user in db.query(User).all()}

        # Seed Categories
        if not db.query(Category).first():
            categories = [
                Category(category_name="Electronics", profit_margin=2),
                Category(category_name="Apparel", profit_margin=2.5),
                Category(category_name="Wearables", profit_margin=2.2),
                Category(category_name="Outdoor & Sports", profit_margin=1.8),
                Category(category_name="Home Automation", profit_margin=2),
                Category(category_name="Transportation", profit_margin=1.5),
            ]
            db.add_all(categories)
            db.commit()
            print("✅ Categories seeded.")

        # Fetch categories for FK
        category_map = {cat.category_name: cat.category_id for cat in db.query(Category).all()}

        # Seed Products
        if not db.query(Product).first():
            now = datetime.now()
            products = [
                Product(
                    name="Wireless Mouse",
                    description="Ergonomic wireless mouse with USB receiver.",
                    cost_price=10.5,
                    selling_price=19.99,
                    stock_available=150,
                    units_sold=40,
                    customer_rating=4.2,
                    demand_forecast=180,
                    optimized_price=18.50,
                    created_at=now,
                    updated_at=now,
                    created_by_user_id=user_map["admin@example.com"],
                    updated_by_user_id=user_map["admin@example.com"],
                    category_id=category_map["Electronics"]
                ),
                Product(
                    name="Eco-Friendly Water Bottle",
                    description="A sustainable, reusable water bottle made from recycled materials.",
                    cost_price=5,
                    selling_price=12.99,
                    stock_available=500,
                    units_sold=220,
                    customer_rating=4.0,
                    demand_forecast=300,
                    optimized_price=18,
                    created_at=now,
                    updated_at=now,
                    created_by_user_id=user_map["buyer@example.com"],
                    updated_by_user_id=user_map["buyer@example.com"],
                    category_id=category_map["Apparel"]
                ),
                Product(
                    name="Wireless Earbuds",
                    description="Bluetooth 5.0 wireless earbuds with noise cancellation and long battery life.",
                    cost_price=25,
                    selling_price=59.99,
                    stock_available=300,
                    units_sold=180,
                    customer_rating=5.0,
                    demand_forecast=280,
                    optimized_price=53,
                    created_at=now,
                    updated_at=now,
                    created_by_user_id=user_map["supplier@example.com"],
                    updated_by_user_id=user_map["supplier@example.com"],
                    category_id=category_map["Wearables"]
                ),
            ]
            db.add_all(products)
            db.commit()
            print("✅ Products seeded.")

    finally:
        db.close()

if __name__ == "__main__":
    seed_data()

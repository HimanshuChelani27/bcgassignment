from datetime import datetime
import math
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from app.database import get_db
from app.models.product import Category, Product
from app.models.users import User
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.models.response import APIResponse
from fastapi.encoders import jsonable_encoder
from app.utils.exception_handlers import require_roles
from app.services.forecast_service import calculate_demand_forecast
from app.services.price_service import calculate_optimized_price
from sqlalchemy.orm import joinedload
router = APIRouter()

# Get products for a specific user.
# Admins and buyers can see all products; suppliers (role_id == 3) see only their own.
@router.get("/by-user", response_model=APIResponse, 
    description="""
    Retrieves a list of products associated with a specific user.

    - Requires authentication and role-based access control (roles: Admin, Buyer, Supplier).
    - Admins and Buyers (role_id 1 and 2) can view all products.
    - Suppliers (role_id 3) can only view products they've created.

    Query Parameters:
    - user_id: ID of the user whose products should be retrieved.

    Responses:
    - 200: Returns a list of products.
    - 404: User not found.
    - 403: Unauthorized access if role is not allowed.
    """,
    tags=["Products"])
def get_products_by_user_id(
    user_id: int = Query(..., description="ID of the user whose products to retrieve"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_roles([1, 2, 3], current_user)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return APIResponse(
            status_code=404,
            status="error",
            message="User not found",
            data=None,
            error="User not found"
        )
    
    # If user is Admins and buyers, no filter i.e all products can be seen
    query = db.query(Product).outerjoin(Category).options(joinedload(Product.category))

    # If user is suppliers (role_id = 3), restrict by their own products
    if user.role_id == 3:
        query = query.filter(Product.created_by_user_id == user_id)

    products = query.all()

    # Add category_name to each product dictionary
    products_data = []
    for product in products:
        product_dict = product.__dict__.copy()
        # Change here: get category_name instead of category_id
        product_dict['category_name'] = product.category.category_name if product.category else None
        products_data.append(product_dict)


    return APIResponse(
        status_code=200,
        status="success",
        message="Product list retrieved successfully",
        data=jsonable_encoder(products_data),
        error=None
    )

# API FOR CREATING A PRODUCT
@router.post("/create", response_model=APIResponse, 
             summary="Create a New Product",
    description="""
    Creates a new product and automatically calculates its demand forecast and optimized price.

    - Only users with roles Admin (1) or Supplier (3) are allowed to create products.
    - Forecast and pricing are computed after temporarily adding the product to the DB session (without committing).
    - Returns the newly created product with all calculated fields.

    Steps:
    1. Accept product input from the client.
    2. Add the product to the session (not committed yet).
    3. Compute demand forecast using internal logic.
    4. Use the forecast to calculate an optimized price.
    5. Commit the product to the database and return it.

    Returns:
    - 200: Successfully created product with forecast and pricing.
    - 403: If user doesn't have permission to create.
    """,
    tags=["Products"])
def create_product(product_data: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    require_roles([1, 3], current_user)
    print(current_user.role_id)
    # Step 1: Create the Product instance (without demand_forecast and optimized_price yet)
    db_product = Product(
        **product_data.dict(),
        created_at=datetime.utcnow(),  # Set current UTC time
        updated_at=None  # Set updated_at to None initially
    )

    # Step 2: Temporarily add the product to the session for forecast computation
    db.add(db_product)
    db.flush()  # Don't commit yet, just get a DB ID if needed

    # Step 3: Calculate demand forecast
    db_product.demand_forecast = calculate_demand_forecast(db_product, db)

    # Step 4: Calculate optimized price based on forecast
    db_product.optimized_price = calculate_optimized_price(db_product, db)

    # Step 5: Commit and return
    db.commit()
    db.refresh(db_product)
    # return db_product
    return APIResponse(
        status_code=200,
        status="success",
        message="Product list retrieved successfully",
        data=jsonable_encoder(db_product),
        error=None
    )


# API FOR GET PRODUCT BY PRODUCT ID
@router.get("/get-product-by-id/{product_id}", response_model=APIResponse, 
            summary="Get Product by ID",
    description="""
    Fetches a single product by its unique ID.

    - Accessible to Admins, Buyers, and Suppliers (roles 1, 2, 3).
    - Returns detailed information about the product if it exists.
    - If the product is not found, returns a 404 response.

    Path Parameters:
    - product_id: The unique identifier of the product.

    Responses:
    - 200: Product found and returned.
    - 404: No product exists with the given ID.
    """,
    tags=["Products"])
def get_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    require_roles([1,2,3], current_user)
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        # IF PRODUCT NOT FOUND
        return APIResponse(
            status_code=404,
            status="error",
            message="Product Not Fount",
            data=None,
            error="Product Not found"
        )
    # RETURN PRODUCT IF FOUND
    return APIResponse(
        status_code=200,
        status="success",
        message="Product list retrieved successfully",
        data=jsonable_encoder(product),
        error=None
    )

# # UPDATE PRODUCT BY PRODUCT ID
# @router.put("/update-product-by-id/{product_id}", response_model=APIResponse, 
#             summary="Update Product by ID",
#     description="""
#     Updates the details of an existing product based on its ID.

#     - Only Admins and Suppliers (roles 1 and 3) are allowed to update products.
#     - If the product is found, all provided fields will be updated.
#     - Returns the updated product data on success.

#     Path Parameters:
#     - product_id: ID of the product to update

#     Request Body:
#     - Partial or full product data to update (matches `ProductUpdate` schema)

#     Responses:
#     - 200: Product updated successfully
#     - 404: Product not found
#     """,
#     tags=["Products"])
# def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     require_roles([1, 3], current_user)
#     product = db.query(Product).filter(Product.id == product_id).first()
#     if not product:
#         return APIResponse(
#             status_code=404,
#             status="error",
#             message="Product Not Fount",
#             data=None,
#             error="Product Not found"
#         )
#     for key, value in product_data.dict().items():
#         setattr(product, key, value)
#     db.commit()
#     db.refresh(product)
#     # return product
#     return APIResponse(
#         status_code=200,
#         status="success",
#         message="Product is updated successfully",
#         data=jsonable_encoder(product),
#         error=None
#     )
@router.put("/update-product-by-id/{product_id}", response_model=APIResponse, 
    summary="Update Product by ID",
    description="""
    Updates the details of an existing product based on its ID.

    - Only Admins and Suppliers (roles 1 and 3) are allowed to update products.
    - If the product is found, all provided fields will be updated.
    - Returns the updated product data on success.

    Path Parameters:
    - product_id: ID of the product to update

    Request Body:
    - Partial or full product data to update (matches `ProductUpdate` schema)

    Responses:
    - 200: Product updated successfully
    - 404: Product not found
    """,
    tags=["Products"])
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_roles([1, 3], current_user)
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return APIResponse(
            status_code=404,
            status="error",
            message="Product Not Found",
            data=None,
            error="Product Not found"
        )

    # Update fields
    for key, value in product_data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    # Recalculate demand forecast and optimized price
    product.demand_forecast = calculate_demand_forecast(product, db)
    product.optimized_price = calculate_optimized_price(product, db)
    print(product.optimized_price, "OPTIMIZED PRICE AFTER UPDATE")

    # Commit changes
    db.commit()
    db.refresh(product)

    return APIResponse(
        status_code=200,
        status="success",
        message="Product is updated successfully",
        data=jsonable_encoder(product),
        error=None
    )


# DELETE PRODUCT BY PRODUCT ID
@router.delete("/delete-product-by-id/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), 
                   summary="Delete Product by ID",
    description="""
    Deletes a product from the system by its ID.

    - Only Admins and Suppliers (roles 1 and 3) are allowed to delete products.
    - If the product exists, it is removed from the database.
    - Returns the deleted product's data for confirmation.

    Path Parameters:
    - product_id: The ID of the product to delete

    Responses:
    - 200: Product deleted successfully
    - 404: Product not found
    """,
    tags=["Products"]
                   ):
    require_roles([1, 3], current_user)
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return APIResponse(
            status_code=404,
            status="error",
            message="Product Not Found",
            data=None,
            error="Product Not Found"
        )
    db.delete(product)
    db.commit()
    return APIResponse(
        status_code=200,
        status="success",
        message="Product deleted successfully",
        data=jsonable_encoder(product),
        error=None
    )

@router.get("/get-all-category", response_model=APIResponse, 
             summary="Get All Categories",
    description="""
    Retrieves a list of all available product categories.

    - Only Admins and Suppliers (roles 1 and 3) are authorized to access this endpoint.
    - Returns all categories from the database.
    - If no categories exist, a 404 error is returned.

    Responses:
    - 200: Successfully fetched list of categories
    - 404: No categories found in the database
    """,
    tags=["Categories"])
def get_all_catergory(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    require_roles([1, 3], current_user)
    category = db.query(Category).all()
    if not category:
        return APIResponse(
            status_code=404,
            status="error",
            message="No Categories are available",
            data=None,
            error="No Categories are available"
        )
    return APIResponse(
        status_code=200,
        status="success",
        message="Categories fetched successfully",
        data=jsonable_encoder(category),
        error=None
    )
    

    
from fastapi import FastAPI
from app.routes.product_routes import router as product_router
from app.database import Base, engine  # 👈 make sure these are correctly imported
from app.models.product import Product        # 👈 import your model module to register tables
from app.models.users import User
from app.models.roles import Role
from app.routes.auth_routes import router as auth_router
from app.utils.exception_handlers import http_exception_handler, generic_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
app = FastAPI(title="Price Optimization API")

from fastapi.middleware.cors import CORSMiddleware
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all (use only for dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables when the app starts
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(auth_router, prefix="/auth",tags=["Authentication"])


app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


@app.get("/")
def root():
    return {"message": "Welcome to the Price Optimization API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

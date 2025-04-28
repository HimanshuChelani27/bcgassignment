from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.users import User
from app.models.roles import Role
from app.models.response import APIResponse
from app.schemas.user import  UserCreate, UserLogin
from app.core.auth import create_access_token, get_current_user, verify_password, get_password_hash

from app.core.auth import generate_verification_token
from app.core.email_utils import send_verification_email
from app.core.auth import decode_verification_token
from app.core.settings import settings
router = APIRouter()


sender_email = settings.SENDER_EMAIL
email_password = settings.EMAIL_APP_PASSWORD
ngrokURL = settings.URL

# API TO GET ALL THE ROLES 
@router.get("/get-all-roles", response_model=APIResponse, 
             summary="Get All Roles",
   
    tags=["Roles"])
def get_all_catergory(db: Session = Depends(get_db)):

    role = db.query(Role).all()
    if not role:
        return APIResponse(
            status_code=404,
            status="error",
            message="No Roles are available",
            data=None,
            error="No Roles are available"
        )
    return APIResponse(
        status_code=200,
        status="success",
        message="Roles fetched successfully",
        data=jsonable_encoder(role),
        error=None
    )    
# API FOR REGISTER USER
@router.post("/register", response_model=APIResponse, 
               summary="User Registration Endpoint",
    description="""
    Registers a new user account.

    - Checks if the email is already registered.
    - Hashes the user's password before storing.
    - Sends a verification email with a unique token.
    - Returns a verification token in the response for frontend tracking.

    Request Body:
    - `email`: User's email address (must be unique)
    - `password`: Plaintext password (will be hashed)
    - `name`: Full name
    - `role_id`: Role identifier for assigning user roles

    Response:
    - 200: Successful registration with access token
    - 400: Email already registered
    """,
    tags=["Authentication"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if db_user:
        return APIResponse(
            status_code=400,
            status="error",
            message="Username already registered",
            data=None,
            error="Username already registered"
        )
        # Check if role exists
    role = db.query(Role).filter(Role.id == user.role_id).first()
    if not role:
        return APIResponse(
            status_code=400,
            status="error",
            message="Invalid role ID",
            data=None,
            error="Role ID does not exist"
        )

    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        password=hashed_password,
        role_id=user.role_id,
        name=user.name
    )
    db.add(new_user)
    db.commit()
    token = generate_verification_token(new_user.email)
    verification_link = f"{ngrokURL}/auth/verify-email?token={token}"
    send_verification_email(sender_email, new_user.email, email_password, verification_link, new_user.name)
 

    return APIResponse(
        status_code=200,
        status="success",
        message="User added successfully",
        data={"access_token": token},
        error=None
    )

# API FOR LOGIN USER
@router.post("/login", response_model=APIResponse)
def login(user_login: UserLogin, db: Session = Depends(get_db), 
          summary="User Login Endpoint",
    description="""
    Authenticates a user using email and password. 

    - Returns an error if the user does not exist or the password is incorrect.
    - Verifies if the user's email is confirmed before allowing login.
    - On successful login, returns an access token along with basic user information.
    
    Response includes:
    - `userId`: User's ID
    - `userName`: Full name
    - `userRoleId`: Assigned role
    - `userEmail`: Email address
    - `access_token`: JWT token
    - `token_type`: Typically "bearer"
    
    Possible Errors:
    - 400: Invalid credentials
    - 403: Email not verified
    """):
    user = db.query(User).filter(User.email == user_login.email).first()
    # Check if user exists and password is correct
    if not user or not verify_password(user_login.password, user.password):
            return APIResponse(
            status_code=400,
            status="error",
            message="Incorrect username or password",
            data=None,
            error="Invalid credentials"
        )
    # Check if the user is verified
    if not user.is_verified:
         return APIResponse(
            status_code=403,
            status="error",
            message="Email not verified",
            data=None,
            error="Whoa there! Looks like you forgot to verify your email. 🕵️‍♂️ No secret agent access without the golden click! Check your inbox and complete the ritual. 🔑📬"
        )


    # Create and return access token
    access_token = create_access_token(data={"sub": user.email})
    return APIResponse(
        status_code=200,
        status="success",
        message="Login successful",
        data={
             "userId": user.id,
             "userName": user.name,
             "userRoleId": user.role_id,
             "userEmail": user.email,
             "access_token": access_token, 
             "token_type": "bearer"},
        error=None
    )


# API FOR VERIFYING USER
@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db), 
                     summary="Email Verification Endpoint",
    description="""
    Verifies a user's email address using a token sent via email.

    - The token should be provided as a query parameter.
    - If the token is valid and corresponds to an existing user, the user's email is marked as verified.
    - If the token is invalid or expired, returns an appropriate error response.

    Query Parameters:
    - `token`: A verification token (typically a JWT) sent to the user's email.

    Possible Responses:
    - 200: Email verified successfully.
    - 400: Invalid or expired token.
    """,
    tags=["Authentication"]):
    try:
        payload = decode_verification_token(token)
        email = payload.get("sub")
    except Exception:
        return APIResponse(
        status_code=400,
        status="error",
        message="Invalid or expired token",
        data={},
        error="Invalid or expired token"
    )

    user = db.query(User).filter(User.email == email).first()
    if not user:
        return APIResponse(
        status_code=400,
        status="error",
        message="Invalid or expired token",
        data={},
        error="Invalid or expired token"
    )
         
    user.is_verified = True
    db.commit()
    return APIResponse(
        status_code=200,
        status="success",
        message="✅ Email verified successfully!",
        data={""},
        error=None
    )


    return APIResponse(
        status_code=200,
        status="success",
        message=f"Hello , your token is valid and you are verified!",
        data={"user_email": current_user.email, "user_id": current_user.id},
        error=None
    )
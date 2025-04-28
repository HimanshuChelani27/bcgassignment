# app/utils/exception_handlers.py
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from app.models.response import APIResponse
from app.models.users import User

def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            status_code=exc.status_code,
            status="error",
            message=exc.detail,
            data=None,
            error=str(exc)
        ).dict()
    )

def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=APIResponse(
            status_code=500,
            status="error",
            message="Internal Server Error",
            data=None,
            error=str(exc)
        ).dict()
    )


def require_roles(allowed_roles: list[int], current_user: User):
    if current_user.role_id not in allowed_roles:
        print(allowed_roles)
        print(current_user.role_id, current_user.name, current_user.email)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
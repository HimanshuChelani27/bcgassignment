from pydantic import BaseModel
from typing import Any, Optional

class APIResponse(BaseModel):
    status_code: int
    status: str  # "success" or "error"
    message: str
    data: Optional[Any] = None
    error: Optional[Any] = None

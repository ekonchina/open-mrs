from typing import List, Dict, Any, Optional
from src.api.models.base_model import BaseModel
from src.api.models.responses.create_acoount_response import AccountResponse


class UserProfileResponse(BaseModel):
    id: int
    username:str|List[str]
    password: str
    name: Optional[str]
    role: str
    accounts: List[AccountResponse]

class CreateUserValidationErrorResponse(BaseModel):
    username: Optional[List[str]] = None
    password: Optional[List[str]] = None
    name: Optional[List[str]] = None

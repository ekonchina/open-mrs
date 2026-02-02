from typing import List, Optional
from src.api.models.base_model import BaseModel

#TODO: Тут генерировать данные
class PersonNameRequest(BaseModel):
    givenName: str
    familyName: str
    middleName: Optional[str] = None


class CreatePersonRequest(BaseModel):
    names: List[PersonNameRequest]
    gender: str  # "M" / "F" / "U"
    age: Optional[int] = None
    birthdate: Optional[str] = None  # "YYYY-MM-DD"
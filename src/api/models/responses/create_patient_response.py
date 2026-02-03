from typing import List, Optional, Any
from src.api.models.base_model import BaseModel


class Link(BaseModel):
    rel: str
    uri: str
    resourceAlias: Optional[str] = None


class PatientIdentifierResponse(BaseModel):
    uuid: str
    display: Optional[str] = None
    identifier: Optional[str] = None
    preferred: Optional[bool] = None
    # OpenMRS часто возвращает identifierType/location как объект или ссылку (разные reps),
    # поэтому делаем мягко:
    identifierType: Optional[Any] = None
    location: Optional[Any] = None


class PatientCreateResponse(BaseModel):
    uuid: str
    display: str
    identifiers: Optional[List[PatientIdentifierResponse]] = None
    links: Optional[List[Link]] = None

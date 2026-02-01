from src.api.models.base_model import BaseModel


class FundDepositRequest(BaseModel):
    id:int
    balance: float
from typing import List, Dict, Any, Optional
from src.api.models.base_model import BaseModel
from src.api.models.responses.transaction_response import TransactionResponse


class AccountResponse(BaseModel):
    id: int
    accountNumber:str
    balance: float
    transactions: List[TransactionResponse]
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Dict

from src.api.models.base_model import BaseModel


class Requester(ABC):
    def __init__(self, request_spec: Dict[str, str], response_spec: Callable):
        self.headers = request_spec.get('headers')
        self.base_url = request_spec.get('base_url', 'http://localhost:4111')
        self.response_spec = response_spec

    @abstractmethod
    def post(self, model:BaseModel|None):...
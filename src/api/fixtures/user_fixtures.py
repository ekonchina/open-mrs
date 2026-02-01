import pytest

from src.api.classes.api_manager import ApiManager
from src.api.generators.random_model_generator import RandomModelGenerator
from src.api.models.requests.create_user_request import CreateUserRequest


@pytest.fixture
def user_request(api_manager: ApiManager) -> CreateUserRequest:
    user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_valid_user(user_data)
    return user_data


@pytest.fixture
def admin_user_request() -> CreateUserRequest:
    return CreateUserRequest(username="admin", password="admin", role='ADMIN')

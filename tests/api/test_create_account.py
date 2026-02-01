import pytest

from src.api.classes.api_manager import ApiManager
from src.api.models.requests.create_user_request import CreateUserRequest



@pytest.mark.api
class TestCreateAccount:

    def test_create_valid_account(self, user_request: CreateUserRequest, api_manager: ApiManager):
        api_manager.user_steps.create_account(create_user_request=user_request)







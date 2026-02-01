import pytest

from src.api.classes.api_manager import ApiManager
from src.api.models.requests.create_user_request import CreateUserRequest


@pytest.mark.api
class TestLogin:

    #сравнение полей

    def test_get_customer_profile(self, user_request: CreateUserRequest, api_manager: ApiManager):
        api_manager.user_steps.get_customer_profile(create_user_request=user_request)


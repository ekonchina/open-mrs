import pytest

from src.api.classes.api_manager import ApiManager
from src.api.models.requests.create_user_request import CreateUserRequest


@pytest.mark.api
class TestLogin:

    def test_login_user(self, user_request: CreateUserRequest, api_manager: ApiManager):
        api_manager.user_steps.login(user_request=user_request)


    def test_login_admin_user(self, api_manager: ApiManager, admin_user_request: CreateUserRequest):
        api_manager.user_steps.login(user_request=admin_user_request)



import pytest

from src.api.generators.random_data import RandomData
from src.api.generators.random_model_generator import RandomModelGenerator
from src.api.models.requests.create_user_request import CreateUserRequest


class RandomGenerator:
    pass


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize('create_user_request', [RandomModelGenerator.generate(CreateUserRequest)])
    def test_create_valid_user(self, api_manager, create_user_request):
        api_manager.admin_steps.create_valid_user(create_user_request=create_user_request)





    @pytest.mark.parametrize(argnames="username,password, role, error_key, error_value",
                             argvalues=[
                                 ("", RandomData.get_valid_password(), "USER", 'username',
                                   'Username must be between 3 and 15 characters'),
                                 ("qwerty@",RandomData.get_valid_password(),"USER", 'username','Username must contain only letters, digits, dashes, underscores, and dots'),
                                 ("ka",RandomData.get_valid_password(),"USER", 'username','Username must be between 3 and 15 characters'),
                                 ("kakakakakakakaka", RandomData.get_valid_password(), "USER", 'username',
                                  'Username must be between 3 and 15 characters'),
                             ])
    def test_create_invalid_user(self,username: str,password: str, role: str, error_key: str, error_value:str, api_manager):
        create_user_request = CreateUserRequest(username=username, password=password, role=role)
        api_manager.admin_steps.create_invalid_user(create_user_request=create_user_request, error_key=error_key, error_value=error_value)


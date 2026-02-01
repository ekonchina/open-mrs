import pytest

from src.api.classes.api_manager import ApiManager
from src.api.generators.random_model_generator import RandomModelGenerator
from src.api.models.requests.create_user_request import CreateUserRequest
from src.api.models.requests.update_profile_request import UpdateProfileRequest


@pytest.mark.api
class TestUpdateCustomerProfile:

    @pytest.mark.parametrize('update_profile_request', [RandomModelGenerator.generate(UpdateProfileRequest)])
    def test_update_user_name(self, user_request: CreateUserRequest, api_manager: ApiManager, update_profile_request:UpdateProfileRequest):
        api_manager.user_steps.update_customer_profile(create_user_request=user_request, update_profile_request = update_profile_request)


    #TODO: воозращает plain/text - точно ли это ок. Сейчас считаем что ок
    @pytest.mark.parametrize(
        argnames="name, error_key, error_value",
        argvalues=[
            ("", "name", "Name must contain two words with letters only"),
            ("John", "name", "Name must contain two words with letters only"),
            ("John Doe Jr", "name", "Name must contain two words with letters only"),
            ("John1 Doe", "name", "Name must contain two words with letters only"),
            ("John Doe!", "name", "Name must contain two words with letters only"),
            ("Иван Иванов", "name", "Name must contain two words with letters only"),
            ("John  Doe", "name", "Name must contain two words with letters only"),
        ]
    )
    def test_update_user_name_invalid(
        self,
        user_request: CreateUserRequest,
        api_manager: ApiManager,
        name: str,
        error_key: str,
        error_value: str
    ):
        api_manager.user_steps.invalid_update_customer_profile(create_user_request=user_request, name = name, error_key = error_key, error_value = error_value)




import pytest

from src.api.classes.api_manager import ApiManager
from src.api.models.requests.create_user_request import CreateUserRequest


@pytest.mark.api
class TestFundDeposit:
    #TODO: если укажем неправильный айди
    # проверить что удаляем пользователя
    # сравнение полей
    # негативные тест кейсы подумать еще
    def test_fund_deposit(self, user_request: CreateUserRequest, api_manager: ApiManager):
        response = api_manager.user_steps.fund_deposit(create_user_request=user_request)


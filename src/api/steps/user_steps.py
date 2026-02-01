from typing import Dict

from src.api.models.comparison.model_assertions import ModelAssertions
from src.api.models.requests.create_user_request import CreateUserRequest
from src.api.models.requests.fund_deposit_request import FundDepositRequest
from src.api.models.requests.login_user_request import LoginUserRequest
from src.api.models.requests.update_profile_request import UpdateProfileRequest
from src.api.models.responses.create_acoount_response import AccountResponse
from src.api.models.responses.create_user_response import UserProfileResponse
from src.api.models.responses.login_user_response import LoginUserResponse
from src.api.requests.sceleton.endpoint import Endpoint
from src.api.requests.sceleton.requesters.crud_requester import CrudRequester
from src.api.requests.sceleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.api.specs.request_spec import RequestSpecs
from src.api.specs.response_spec import ResponseSpecs
from src.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    # --- helpers ---
    def _auth_headers(self, user: CreateUserRequest) -> Dict[str, str]:
        return RequestSpecs.user_auth_spec(user.username, user.password)

    def _get_profile(self, headers: Dict[str, str]) -> UserProfileResponse:
        return ValidatedCrudRequester(
            request_spec=headers,
            endpoint=Endpoint.GET_CUSTOMER_PROFILE,
            response_spec=ResponseSpecs.request_returns_ok()
        ).get()

    # --- steps ---
    def login(self, user_request: CreateUserRequest) -> LoginUserResponse:
        login_request = LoginUserRequest(username=user_request.username, password=user_request.password)

        login_user_response: LoginUserResponse = ValidatedCrudRequester(
            request_spec=RequestSpecs.unauth_spec(),
            endpoint=Endpoint.LOGIN_USER,
            response_spec=ResponseSpecs.request_returns_ok()
        ).post(login_request)

        ModelAssertions(login_request, login_user_response).match()

        self.created_objects.append(login_user_response)
        return login_user_response

    def create_account(self, create_user_request: CreateUserRequest) -> AccountResponse:
        headers = self._auth_headers(create_user_request)

        create_account_response: AccountResponse = ValidatedCrudRequester(
            request_spec=headers,
            endpoint=Endpoint.CREATE_ACCOUNT,
            response_spec=ResponseSpecs.entity_was_created()
        ).post()

        assert create_account_response.balance == 0.0
        assert create_account_response.transactions == []
        assert create_account_response.id

        return create_account_response

    def fund_deposit(self, create_user_request: CreateUserRequest) -> AccountResponse:
        headers = self._auth_headers(create_user_request)

        create_account_response: AccountResponse = ValidatedCrudRequester(
            request_spec=headers,
            endpoint=Endpoint.CREATE_ACCOUNT,
            response_spec=ResponseSpecs.entity_was_created()
        ).post()

        assert create_account_response.balance == 0.0
        assert create_account_response.transactions == []
        assert create_account_response.id

        fund_deposit_request = FundDepositRequest(id=create_account_response.id, balance=100.00)

        deposit_response: AccountResponse = ValidatedCrudRequester(
            request_spec=headers,
            endpoint=Endpoint.FUND_DEPOSIT,
            response_spec=ResponseSpecs.request_returns_ok()
        ).post(fund_deposit_request)

        return deposit_response

    def get_customer_profile(self, create_user_request: CreateUserRequest) -> UserProfileResponse:
        headers = self._auth_headers(create_user_request)
        return self._get_profile(headers)

    def update_customer_profile(
        self,
        create_user_request: CreateUserRequest, update_profile_request: UpdateProfileRequest
    ) -> UserProfileResponse:

        headers = self._auth_headers(create_user_request)

        profile_response_before_update = self._get_profile(headers)
        assert profile_response_before_update.name is None

        CrudRequester(
            request_spec=headers,
            endpoint=Endpoint.UPDATE_CUSTOMER_PROFILE,
            response_spec=ResponseSpecs.request_returns_ok()
        ).update(update_profile_request)

        profile_response_after_update = self._get_profile(headers)
        assert profile_response_after_update.name == update_profile_request.name

        return profile_response_after_update

    def invalid_update_customer_profile(
        self,
        create_user_request: CreateUserRequest, name: str, error_key: str, error_value: str
    ):

        update_profile_request = UpdateProfileRequest(name= name)

        CrudRequester(
            request_spec=RequestSpecs.user_auth_spec(create_user_request.username, create_user_request.password),
            endpoint=Endpoint.UPDATE_CUSTOMER_PROFILE,
            response_spec=ResponseSpecs.request_returns_bad_request(error_key=error_key, error_value=error_value)
        ).update(update_profile_request)
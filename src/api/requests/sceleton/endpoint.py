from dataclasses import dataclass
from enum import Enum
from typing import Optional

from src.api.models.base_model import BaseModel
from src.api.models.requests.create_user_request import CreateUserRequest
from src.api.models.requests.fund_deposit_request import FundDepositRequest
from src.api.models.requests.login_user_request import LoginUserRequest
from src.api.models.requests.update_profile_request import UpdateProfileRequest
from src.api.models.responses.create_acoount_response import AccountResponse
from src.api.models.responses.create_user_response import UserProfileResponse
from src.api.models.responses.get_location_response import LocationListResponse
from src.api.models.responses.get_roles_response import RoleListResponse
from src.api.models.responses.login_user_response import LoginUserResponse


@dataclass(frozen=True)
class EndpointConfig:
    url:str
    request_model:Optional[BaseModel]
    response_model:Optional[BaseModel]

class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfig(url="/admin/users", request_model=CreateUserRequest, response_model=UserProfileResponse)
    ADMIN_DELETE_USER = EndpointConfig(url="/admin/users",request_model=None,response_model=None)
    LOGIN_USER = EndpointConfig(url="/auth/login", request_model=LoginUserRequest, response_model=LoginUserResponse)
    CREATE_ACCOUNT = EndpointConfig(url="/accounts", request_model=None, response_model=AccountResponse)
    FUND_DEPOSIT = EndpointConfig(url="/accounts/deposit", request_model=FundDepositRequest, response_model=AccountResponse)
    GET_CUSTOMER_PROFILE = EndpointConfig(url="/customer/profile", request_model=None, response_model=UserProfileResponse)
    UPDATE_CUSTOMER_PROFILE = EndpointConfig(url="/customer/profile", request_model=UpdateProfileRequest, response_model=None)
    GET_ROLES = EndpointConfig(
        url="/role",
        request_model=None,
        response_model=RoleListResponse
    )

    GET_LOCATIONS = EndpointConfig(
        url="/location",
        request_model=None,
        response_model=LocationListResponse
    )
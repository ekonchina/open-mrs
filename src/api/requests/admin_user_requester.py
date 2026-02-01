from http import HTTPStatus
from typing import Union

import requests

from src.api.models.requests.create_user_request import CreateUserRequest
from src.api.models.responses.create_user_response import UserProfileResponse, CreateUserValidationErrorResponse
from src.api.requests.requester import Requester


class AdminUserRequester(Requester):

    def post(self, create_user_request:CreateUserRequest) -> Union[UserProfileResponse, None]:
        url = f"{self.base_url}/admin/users"
        response = requests.post(url=url, headers=self.headers, json=create_user_request.model_dump())
        self.response_spec(response)

        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
            return UserProfileResponse(**response.json())
        return None

    def delete(self, id: int):
        url = f"{self.base_url}/admin/users/{id}"
        response = requests.delete(url=url, headers=self.headers, )
        self.response_spec(response)
        return response



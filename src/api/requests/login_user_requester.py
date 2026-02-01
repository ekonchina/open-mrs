import requests

from src.api.models.requests.login_user_request import LoginUserRequest
from src.api.models.responses.login_user_response import LoginUserResponse
from src.api.requests.requester import Requester



class LoginUserRequester(Requester):

    def post(self, login_user_request: LoginUserRequest) -> LoginUserResponse:
        url = f"{self.base_url}/auth/login"
        response = requests.post(url=url, headers=self.headers, json=login_user_request.model_dump())
        self.response_spec(response)
        return LoginUserResponse(**response.json())



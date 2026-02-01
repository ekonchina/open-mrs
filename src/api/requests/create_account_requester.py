import requests

from src.api.models.responses.create_user_response import UserProfileResponse
from src.api.requests.requester import Requester


class CreateAccountRequester(Requester):

    def post(self) -> UserProfileResponse:
        url = f"{self.base_url}/accounts"
        response = requests.post(url=url, headers=self.headers)
        self.response_spec(response)
        return UserProfileResponse(**response.json())



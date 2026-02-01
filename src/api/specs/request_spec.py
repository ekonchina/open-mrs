import base64
import logging

import requests

from src.api.configs.config import Config
from src.api.models.requests.login_user_request import LoginUserRequest
from src.api.requests.sceleton.endpoint import Endpoint
from src.api.requests.sceleton.requesters.crud_requester import CrudRequester
from src.api.specs.response_spec import ResponseSpecs


class RequestSpecs:
    _BASE_URL = Config.get('backendUrl')

    @staticmethod
    def default_request_headers():
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
        }

    @staticmethod
    def unauth_spec():
        return RequestSpecs.default_request_headers()

    @staticmethod
    def admin_auth_spec():
        raw = "admin:Admin123"
        token = base64.b64encode(raw.encode()).decode()
        headers = RequestSpecs.default_request_headers()
        headers["authorization"] = f"Basic {token}"
        return headers

    @staticmethod
    def user_auth_spec(username: str, password: str):
        try:
            response = (
                CrudRequester(RequestSpecs.unauth_spec(), endpoint=Endpoint.LOGIN_USER, response_spec=ResponseSpecs.request_returns_ok())
                .post(LoginUserRequest(username=username, password=password)))

        except:
            logging.error(f"Authentification failed for {username} with status {response.status_code}")
            raise Exception(f"Authentification failed for {username} with status {response.status_code}")

        else:
            if response.status_code == 200:
                headers = RequestSpecs.default_request_headers()
                headers['Authorization'] = response.headers.get('Authorization')
                return headers



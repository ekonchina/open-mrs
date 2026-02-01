from typing import Union

from src.api.generators.random_model_generator import RandomModelGenerator
from src.api.models.comparison.model_assertions import ModelAssertions
from src.api.models.requests.create_user_request import CreateUserRequest
from src.api.models.responses.create_user_response import UserProfileResponse
from src.api.requests.sceleton.endpoint import Endpoint
from src.api.requests.sceleton.requesters.crud_requester import CrudRequester
from src.api.requests.sceleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.api.specs.request_spec import RequestSpecs
from src.api.specs.response_spec import ResponseSpecs
from src.api.steps.base_steps import BaseSteps





class AdminSteps(BaseSteps):

    def create_valid_user(self, create_user_request:CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)) -> Union[UserProfileResponse, None]:


        create_user_response: UserProfileResponse = ValidatedCrudRequester(
            request_spec=RequestSpecs.admin_auth_spec(),
            endpoint=Endpoint.ADMIN_CREATE_USER,
            response_spec=ResponseSpecs.entity_was_created()
        ).post(create_user_request)


        ModelAssertions(create_user_request,create_user_response).match()

        self.created_objects.append(create_user_response)

        return create_user_response

    def create_invalid_user(self, create_user_request:CreateUserRequest, error_key, error_value):

        CrudRequester(
            request_spec=RequestSpecs.admin_auth_spec(),
            endpoint=Endpoint.ADMIN_CREATE_USER,
            response_spec=ResponseSpecs.request_returns_bad_request(error_key,error_value)
        ).post(create_user_request)


    def delete_user(self,user_id: int):

        CrudRequester(
            request_spec=RequestSpecs.admin_auth_spec(),
            endpoint=Endpoint.ADMIN_DELETE_USER,
            response_spec=ResponseSpecs.entity_was_deleted()
        ).delete(user_id)

    def get_roles(self):
        return ValidatedCrudRequester(
            request_spec=RequestSpecs.admin_auth_spec(),
            endpoint=Endpoint.GET_ROLES,
            response_spec=ResponseSpecs.request_returns_ok()
        ).get()

    def get_locations(self):
        return ValidatedCrudRequester(
            request_spec=RequestSpecs.admin_auth_spec(),
            endpoint=Endpoint.GET_LOCATIONS,
            response_spec=ResponseSpecs.request_returns_ok()
        ).get()





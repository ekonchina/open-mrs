from typing import Union

from src.api.generators.random_model_generator import RandomModelGenerator
from src.api.models.comparison.model_assertions import ModelAssertions
from src.api.models.requests.create_patient_from_person_request import CreatePatientFromPersonRequest, \
    PatientIdentifierRequest
from src.api.models.requests.create_person_request import CreatePersonRequest, CreatePersonInvalidRequest
from src.api.models.requests.create_user_request import CreateUserRequest
from src.api.models.responses.create_patient_response import PatientCreateResponse
from src.api.models.responses.create_person_response import CreatPersonResponse, PersonFullResponse
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

    def get_patient_identifier_types(self):
        return ValidatedCrudRequester(
            request_spec=RequestSpecs.admin_auth_spec(),
            endpoint=Endpoint.GET_PATIENT_IDENTIFIER_TYPES,
            response_spec=ResponseSpecs.request_returns_ok()
        ).get()

    def create_person(self, create_person_request: CreatePersonRequest) -> CreatPersonResponse:
        person = ValidatedCrudRequester(
            request_spec=RequestSpecs.admin_auth_spec(),
            endpoint=Endpoint.CREATE_PERSON,
            response_spec=ResponseSpecs.entity_was_created()
        ).post(create_person_request)

        full = self.get_person_full(person.uuid)
        ModelAssertions(create_person_request, full).match()
        self.created_objects.append(person)
        return person

    def get_person_full(self, person_uuid: str) -> PersonFullResponse:
        return ValidatedCrudRequester(
            request_spec=RequestSpecs.admin_auth_spec(),
            endpoint=Endpoint.GET_PERSON,
            response_spec=ResponseSpecs.request_returns_ok()
        ).get(id=person_uuid, params={"v": "full"})

    def delete_person(self, person_uuid: str, purge: bool = True):
        params = {"purge": "true"} if purge else None

        CrudRequester(
            request_spec=RequestSpecs.admin_auth_spec(),
            endpoint=Endpoint.DELETE_PERSON,
            response_spec=ResponseSpecs.entity_was_deleted()
        ).delete_with_params(id=person_uuid, params=params)

    def create_patient_from_person(self, req: CreatePatientFromPersonRequest) -> PatientCreateResponse:
        patient = ValidatedCrudRequester(
            request_spec=RequestSpecs.admin_auth_spec(),
            endpoint=Endpoint.CREATE_PATIENT_FROM_PERSON,
            response_spec=ResponseSpecs.entity_was_created()
        ).post(req)

        self.created_objects.append(patient)
        return patient

    def delete_patient(self, patient_uuid: str, purge: bool = True):
        params = {"purge": "true"} if purge else None
        CrudRequester(
            request_spec=RequestSpecs.admin_auth_spec(),
            endpoint=Endpoint.DELETE_PATIENT,
            response_spec=ResponseSpecs.entity_was_deleted()
        ).delete_with_params(id=patient_uuid, params=params)

    def create_invalid_person(self, create_person_request: CreatePersonInvalidRequest, error_key, error_value):
        CrudRequester(
            request_spec=RequestSpecs.admin_auth_spec(),
            endpoint=Endpoint.CREATE_PERSON,
            response_spec=ResponseSpecs.request_returns_bad_request(error_key, error_value),
        ).post(create_person_request)

    def create_patient_from_existing_person(
        self,
        create_person_request: CreatePersonRequest | None = None,
        identifier_request: PatientIdentifierRequest | None = None,
    ):
        # 1) person
        create_person_request = create_person_request or RandomModelGenerator.generate(CreatePersonRequest)
        created_person = self.create_person(create_person_request)

        # 2) справочники
        types = self.get_patient_identifier_types()
        identifier_type_uuid = types.results[0].uuid

        locations = self.get_locations()
        location_uuid = locations.results[0].uuid

        # 3) identifier
        identifier = identifier_request or RandomModelGenerator.generate(PatientIdentifierRequest)
        identifier.identifierType = identifier_type_uuid
        identifier.location = location_uuid
        identifier.preferred = True

        # 4) patient
        req = CreatePatientFromPersonRequest(person=created_person.uuid, identifiers=[identifier])
        created_patient = self.create_patient_from_person(req)

        # 5) минимальные ассерты (по аналогии с create_valid_user)
        assert created_patient.uuid
        assert created_patient.display

        return created_patient







import logging

import pytest

from src.api.fixtures.api_fixtures import *
from src.api.fixtures.user_fixtures import *
from src.api.fixtures.objects_fixture import *
from src.api.models.responses.create_patient_response import PatientCreateResponse
from src.api.models.responses.create_person_response import CreatPersonResponse

from src.api.models.responses.create_user_response import UserProfileResponse


def cleanup_object(objects: list):
    api_manager = ApiManager(objects)
    for obj in objects:
        if isinstance(obj, UserProfileResponse):
            api_manager.admin_steps.delete_user(obj.id)
        elif isinstance(obj, CreatPersonResponse):
            api_manager.admin_steps.delete_person(obj.uuid, purge=True)
        elif isinstance(obj, PatientCreateResponse):
            api_manager.admin_steps.delete_patient(obj.uuid, purge=True)
        else:
            logging.warning(f'Object type: {type(obj)} is not deleted')


@pytest.fixture
def created_objects():
    objects: list = []
    yield objects
    cleanup_object(objects)





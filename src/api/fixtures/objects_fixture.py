import logging

import pytest

from src.api.classes.api_manager import ApiManager
from src.api.models.responses.create_user_response import UserProfileResponse


def cleanup_object(objects: list):
    api_manager = ApiManager(objects)
    for obj in objects:
        if isinstance(obj, UserProfileResponse):
            api_manager.admin_steps.delete_user(obj.id)
        else:
            logging.warning(f'Object type: {type(obj)} is not deleted')


@pytest.fixture
def created_objects():
    objects: list = []
    yield objects
    cleanup_object(objects)

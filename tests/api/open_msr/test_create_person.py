import pytest


from src.api.generators.random_model_generator import RandomModelGenerator
from src.api.models.requests.create_person_request import CreatePersonRequest

@pytest.mark.api
def test_create_person(api_manager):
    req = RandomModelGenerator.generate(CreatePersonRequest)
    created = api_manager.admin_steps.create_person(req)

    #TODO: убрать куда-нибудь
    assert created.uuid
    assert created.voided is False
    assert created.preferredName.uuid
    full = api_manager.admin_steps.get_person_full(created.uuid)

    # TODO: убрать куда-нибудь
    assert full.uuid == created.uuid


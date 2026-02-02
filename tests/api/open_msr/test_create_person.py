import pytest

from src.api.models.requests import create_person_request
from src.api.models.requests.create_person_request import CreatePersonRequest, PersonNameRequest
from src.api.generators.random_model_generator import RandomModelGenerator
from src.api.models.requests.create_person_request import CreatePersonRequest
#TODO: автоматическая генерация данных
# Сравнение полей
# удаление персон
@pytest.mark.api
def test_create_person_generated(api_manager):


    req = RandomModelGenerator.generate(CreatePersonRequest)

    # если хочешь строго "как в примере доки" — оставь addresses как есть (он сгенерится либо None либо list)
    # если хочешь всегда адрес:
    if req.addresses is None:
        # можно заставить — но проще выставить probability в генераторе
        pass

    created = api_manager.admin_steps.create_person(req)

    assert created.uuid
    assert created.gender == req.gender
    assert created.uuid
    assert created.display
    #assert created.gender == create_person_request.
    assert created.voided is False
    assert created.preferredName and created.preferredName.uuid
    assert created.links and any(l.rel == "self" for l in created.links)

    # 2) GET FULL
    full = api_manager.admin_steps.get_person_full(created.uuid)

    assert full.uuid == created.uuid
    #assert full.gender == create_person_request.gender
    assert full.voided is False
    assert isinstance(full.names, list) and full.names


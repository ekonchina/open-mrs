import pytest


from src.api.generators.random_model_generator import RandomModelGenerator
from src.api.models.requests.create_person_request import CreatePersonRequest
#TODO: автоматическая генерация данных
# Сравнение полей
# удаление персон
@pytest.mark.api
def test_create_person(api_manager):


    create_person_request_data = RandomModelGenerator.generate(CreatePersonRequest)

    created_person = api_manager.admin_steps.create_person(create_person_request_data)

    assert created_person.uuid
    assert created_person.gender == create_person_request_data.gender
    assert created_person.uuid
    assert created_person.display
    #assert created.gender == create_person_request.
    assert created_person.voided is False
    assert created_person.preferredName and created_person.preferredName.uuid
    assert created_person.links and any(l.rel == "self" for l in created_person.links)

    # 2) GET FULL
    full = api_manager.admin_steps.get_person_full(created_person.uuid)

    assert full.uuid == created_person.uuid
    #assert full.gender == create_person_request.gender
    assert full.voided is False
    assert isinstance(full.names, list) and full.names


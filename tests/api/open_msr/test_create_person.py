import pytest


from src.api.generators.random_model_generator import RandomModelGenerator
from src.api.models.requests.create_person_request import CreatePersonRequest
#TODO: автоматическая генерация данных
# Сравнение полей
# удаление персон
@pytest.mark.api
def test_create_person(api_manager):
    # 1) CREATE
    create_person_request_data = RandomModelGenerator.generate(CreatePersonRequest)
    created_person = api_manager.admin_steps.create_person(create_person_request_data)

    # минимально "железные" проверки создания
    assert created_person.uuid, "Expected non-empty uuid for created person"
    assert created_person.voided is False, "Newly created person should not be voided"
    assert created_person.gender == create_person_request_data.gender, "Gender in response should match request"

    # полезные, но не сверх-хрупкие проверки репрезентации
    assert created_person.display, "Expected non-empty display"
    assert created_person.preferredName and created_person.preferredName.uuid, "Expected preferredName with uuid"
    assert created_person.links and any(l.rel == "self" for l in created_person.links), "Expected self link in links"

    # 2) GET FULL
    full = api_manager.admin_steps.get_person_full(created_person.uuid)

    assert full.uuid == created_person.uuid
    assert full.voided is False
    assert isinstance(full.names, list) and full.names, "Expected non-empty names in full representation"


import pytest

from src.api.models.requests.create_person_request import CreatePersonRequest, PersonNameRequest

#TODO: автоматическая генерация данных
# Сравнение полей
# удаление персон
@pytest.mark.api
@pytest.mark.parametrize(
    "create_person_request",
    [
        CreatePersonRequest(
            names=[PersonNameRequest(givenName="John", familyName="Doe")],
            gender="M"
        ),
        CreatePersonRequest(
            names=[PersonNameRequest(givenName="Alice", familyName="Smith")],
            gender="F",
            age=30
        ),
        CreatePersonRequest(
            names=[PersonNameRequest(givenName="Bob", familyName="Brown")],
            gender="M",
            birthdate="1990-01-15"
        ),
    ]
)
def test_create_person_full_validation(api_manager, create_person_request: CreatePersonRequest):
    # 1) CREATE
    created = api_manager.admin_steps.create_person(create_person_request)

    assert created.uuid
    assert created.display
    assert created.gender == create_person_request.gender
    assert created.voided is False
    assert created.preferredName and created.preferredName.uuid
    assert created.links and any(l.rel == "self" for l in created.links)

    # 2) GET FULL
    full = api_manager.admin_steps.get_person_full(created.uuid)

    assert full.uuid == created.uuid
    assert full.gender == create_person_request.gender
    assert full.voided is False
    assert isinstance(full.names, list) and full.names

    # проверим, что exact given+family реально присутствуют в names
    exp_given = create_person_request.names[0].givenName
    exp_family = create_person_request.names[0].familyName

    found = any(
        (n.get("givenName") == exp_given and n.get("familyName") == exp_family and n.get("voided") is False)
        for n in full.names
        if isinstance(n, dict)
    )
    assert found, f"Expected name not found: {exp_given} {exp_family}; names={full.names}"
ч
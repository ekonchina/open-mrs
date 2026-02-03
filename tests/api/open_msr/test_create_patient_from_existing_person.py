import pytest

from src.api.generators.random_model_generator import RandomModelGenerator
from src.api.models.requests.create_person_request import CreatePersonRequest
from src.api.models.requests.create_patient_from_person_request import (
    CreatePatientFromPersonRequest,
    PatientIdentifierRequest,
)


@pytest.mark.api
def test_create_patient_from_existing_person_generated(api_manager):
    # 1) Создаём person
    create_person_request_data = RandomModelGenerator.generate(CreatePersonRequest)
    created_person = api_manager.admin_steps.create_person(create_person_request_data)

    assert created_person.uuid
    assert created_person.voided is False

    # 2) Берём валидные справочники с сервера
    types = api_manager.admin_steps.get_patient_identifier_types()
    assert types.results and types.results[0].uuid
    identifier_type_uuid = types.results[0].uuid

    locations = api_manager.admin_steps.get_locations()
    assert locations.results and locations.results[0].uuid
    location_uuid = locations.results[0].uuid

    # 3) Собираем request на patient из существующего person
    identifier = RandomModelGenerator.generate(PatientIdentifierRequest)
    identifier.identifierType = identifier_type_uuid
    identifier.location = location_uuid
    identifier.preferred = True

    create_patient_req = CreatePatientFromPersonRequest(
        person=created_person.uuid,
        identifiers=[identifier],
    )

    # 4) Создаём patient
    created_patient = api_manager.admin_steps.create_patient_from_person(create_patient_req)

    # 5) Ассерты “минимально железные”
    assert created_patient.uuid
    assert created_patient.display

    # identifiers в ответе могут быть не всегда/зависит от rep, но если есть — проверим
    if created_patient.identifiers:
        assert any(i.uuid for i in created_patient.identifiers)

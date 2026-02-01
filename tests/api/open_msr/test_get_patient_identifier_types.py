import pytest


@pytest.mark.api
class TestPatientIdentifierTyped:
    def test_patient_identifier_types(self, api_manager):
        types = api_manager.admin_steps.get_patient_identifier_types()
        assert types.results
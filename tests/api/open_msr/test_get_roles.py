import pytest


@pytest.mark.api
class TestGetRoles:
    def test_get_roles(self, api_manager):
        roles = api_manager.admin_steps.get_roles()
        assert roles.results
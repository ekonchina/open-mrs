import pytest


@pytest.mark.api
def test_get_locations(api_manager):
    locations = api_manager.admin_steps.get_locations()

    assert locations.results
    assert locations.results[0].uuid
    assert locations.results[0].display

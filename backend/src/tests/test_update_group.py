import pytest
from src.service.exceptions.users_exceptions import *
from src.service.exceptions.users_exceptions import *
from src.service.exceptions.groups_exceptions import *
from src.tests import duplicate_tests
from src.tests.util_functions import *

@pytest.mark.anyio
async def test_update_group_with_unregistered_user(client):
    # GIVEN

    # WHEN
    response = await client.put("/groups/1", json=group_update_to_json(GroupUpdate(name="NewName")))

    # THEN
    assert response.status_code == 401

@pytest.mark.anyio
async def test_update_unexistent_group(client):
    # GIVEN
    headers = await duplicate_tests.register_user_1(client)

    # WHEN
    response = await client.put("/groups/1", json=group_update_to_json(GroupUpdate(name="NewName")), headers=headers)

    # THEN
    assert response.status_code == 404

@pytest.mark.anyio
async def test_update_with_invalid_fields(client):
    # GIVEN
    headers = await duplicate_tests.single_participant_event(client)

    # WHEN
    response = await client.put("/groups/1", json=group_update_to_json(GroupUpdate(name="")), headers=headers)

    # THEN
    assert response.status_code == 400

@pytest.mark.anyio
async def test_update_group(client):
    # GIVEN
    headers = await duplicate_tests.single_participant_event(client)

    # WHEN
    await client.put("/groups/1", json=group_update_to_json(GroupUpdate(name="NewName")), headers=headers)

    # THEN
    result_group = await client.get("/groups/1", headers=headers)
    assert result_group.status_code == 200
    group = json_to_group(result_group.json())

    assert group.name == "NewName"

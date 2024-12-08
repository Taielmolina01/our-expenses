import pytest
from src.tests import duplicate_tests
from src.tests.util_functions import *

@pytest.mark.anyio
async def test_see_groups(client):
    # GIVEN 
    headers = await duplicate_tests.event_with_payments(client)

    # WHEN

    # THEN
    response_group = await client.get("/users/test@example.com/groups/data", headers=headers)

    assert response_group.status_code == 200

    json = response_group.json()

    assert json[0]["group_name"] == "MyGroup"    
    assert json[0]["group_id"] == 1
    assert json[0]["balance"] == -100
    assert json[0]["user_email"] == "test@example.com"

@pytest.mark.anyio
async def test_not_see_groups(client):
    # GIVEN 
    await duplicate_tests.not_part_of_event(client)

    # WHEN

    # THEN
    response = await log_in_user(client, create_user_model_not_registered())
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response_group = await client.get("/users/non_member@example.com/groups", headers=headers)

    assert response_group.status_code == 200

    groups = json_to_groups(response_group.json())

    assert len(groups) == 0


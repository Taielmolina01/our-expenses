import pytest
from src.service.exceptions.groups_exceptions import *
from src.tests.util_functions import *
from src.tests import duplicate_tests

@pytest.mark.anyio
async def test_create_group_without_being_registered(client):
        # GIVEN

        # WHEN
        response = await client.post("/groups", json=group_to_json(create_group_model()))

        # THEN
        assert response.status_code == 401
        
@pytest.mark.anyio
async def test_create_group_without_name(client):
        # GIVEN
        headers = await duplicate_tests.register_user_1(client)

        # WHEN
        response = await client.post("/groups", json=group_to_json(create_group_model_without_name()), headers=headers)

        # THEN
        assert response.status_code == 400

@pytest.mark.anyio
async def test_create_group_with_valid_name(client):
        # GIVEN
        headers = await duplicate_tests.register_user_2(client)

        # WHEN
        await client.post("/groups", json=group_to_json(create_group_model()), headers=headers)

        # THEN
        response_group = await client.get("/groups/1", headers=headers)
        assert response_group.status_code == 200

        group_base = response_group.json()

        assert group_base['name'] == "MyGroup"
        assert group_base['group_id'] == 1

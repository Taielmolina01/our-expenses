import pytest
from src.service.exceptions.groups_exceptions import *
from src.tests.util_functions import *
from src.tests import duplicate_tests

@pytest.mark.anyio
async def test_delete_group_unregistered(client):
        # GIVEN

        # WHEN
        await client.post("/groups", json=group_to_json(create_group_model()))

        response = await client.delete("/groups/1")

        # THEN
        assert response.status_code == 401

@pytest.mark.anyio
async def test_delete_group_without_group(client):
        # GIVEN
        headers = await duplicate_tests.register_user_1(client)

        # WHEN
        await client.post("/groups", json=group_to_json(create_group_model()), headers=headers)

        user_2 = create_user_model_2()
        await client.post("/users", json=user_to_json(user_2))

        response = await log_in_user(client, user_2)
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        response = await client.delete("/groups/1", headers=headers)

        # THEN
        assert response.status_code == 403

@pytest.mark.anyio
async def test_delete_group(client):
        # GIVEN
        headers = await duplicate_tests.register_user_2(client)

        # WHEN
        group_json = group_to_json(create_group_model_2())

        await client.post("/groups", json=group_json, headers=headers)

        await client.delete("/groups/1", headers=headers)

        # THEN
        result_group = await client.get("/groups/1", headers=headers)

        assert result_group.status_code == 404

import pytest
from src.tests.util_functions import *
from src.models.payment import Category
from src.tests import duplicate_tests

@pytest.mark.anyio
async def test_not_part_of_event(client):
        # GIVEN
        headers = await duplicate_tests.not_part_of_event(client)

        # WHEN
        response_group = await client.get("/groups/1", headers=headers) 

        assert response_group.status_code == 200
        group_base = json_to_group(response_group.json())
        
        response_user = await client.get("/users/non_member@example.com")
        assert response_user.status_code == 200
        payer = json_to_user(response_user.json())

        payer_model = create_user_model_not_registered()
        response = await log_in_user(client, payer_model)

        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        response_group = await client.get("/groups/1/users", headers=headers)

        payment_json = payment_to_json(create_payment_model(payer, group_base, Category.ENTERTAINMENT), {payer.email: 1})
        final_response = await client.post("/payments", json=payment_json, headers=headers)

        # THEN
        assert final_response.status_code == 403

@pytest.mark.anyio
async def test_single_participant_event(client):
        # GIVEN
        headers = await duplicate_tests.single_participant_event(client)

        # WHEN
        response_user = await client.get("/users/test@example.com")
        response_group = await client.get("/groups/1", headers=headers) 

        assert response_user.status_code == 200
        assert response_group.status_code == 200

        user_base = json_to_user(response_user.json())
        group_base = json_to_group(response_group.json())
        payment_json = payment_to_json(create_payment_model(user_base, group_base, Category.ENTERTAINMENT), {user_base.email: 0.5, user_base.email: 0.5})
        
        await client.post("/payments", json=payment_json, headers=headers)

        # THEN
        response = await client.get("/users/test@example.com")

        assert response.status_code == 200

        user = response.json()


        balance_user_1_group_1 = await client.get(f"/groups/{group_base.group_id}/users/{user["email"]}", headers=headers)

        balance_user_1_group_1 = balance_user_1_group_1.json()

        assert balance_user_1_group_1['balance'] == 0
        assert user['email'] == "test@example.com"
        assert user['name'] == "MyUser1"

@pytest.mark.anyio
async def test_multiple_participants_event(client):
        # GIVEN
        headers = await duplicate_tests.multiple_participants_event(client)

        # WHEN
        response_user_1 = await client.get("/users/test@example.com")
        response_user_2 = await client.get("/users/test2@example.com")
        response_group = await client.get("/groups/1", headers=headers)

        assert response_user_1.status_code == 200
        assert response_user_2.status_code == 200
        assert response_group.status_code == 200

        user_base_1 = json_to_user(response_user_1.json())
        user_base_2 = json_to_user(response_user_2.json())
        group_base = json_to_group(response_group.json())
        payment_json = payment_to_json(create_payment_model(user_base_1, group_base, Category.ENTERTAINMENT), {user_base_1.email: 0.5, user_base_2.email: 0.5})

        payment_response = await client.post("/payments", json=payment_json, headers=headers)

        print(payment_response)

        # THEN
        await duplicate_tests.verify_debt(client, 100, headers)

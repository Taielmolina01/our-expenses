import pytest
from src.tests import duplicate_tests
from src.tests.util_functions import *
from src.service.exceptions.debts_exceptions import *

@pytest.mark.anyio
async def test_pay_without_group(client):
    # GIVEN
    headers = await duplicate_tests.not_part_of_event(client)

    # WHEN
    response = await client.put("/debts/1", json=update_debt_to_json(DebtState.PAID), headers=headers)

    # THEN
    assert response.status_code == 404

@pytest.mark.anyio
async def test_pay_single_participants(client):
    # GIVEN
    headers = await duplicate_tests.single_participant_event(client)

    # WHEN
    response_user_1 = await client.get("/users/test@example.com")
    response_group = await client.get("/groups/1", headers=headers)

    assert response_user_1.status_code == 200
    assert response_group.status_code == 200

    user_base_1 = json_to_user(response_user_1.json())
    group_base = json_to_group(response_group.json())
    
    payment_json = payment_to_json(create_payment_model(user_base_1, group_base, Category.ENTERTAINMENT), {user_base_1.email: 1})
    await client.post("/payments", json=payment_json, headers=headers)

    response = await client.put("/debts/1", json=update_debt_to_json(DebtState.PAID), headers=headers)

    # THEN
    assert response.status_code == 404

    response_user = await client.get("/users/test@example.com")

    assert response_user.status_code == 200

    user_base = response_user.json()

    balance_user_1_group_1 = await client.get(f"/groups/{group_base.group_id}/users/{user_base["email"]}", headers=headers)

    balance_user_1_group_1 = balance_user_1_group_1.json()

    assert balance_user_1_group_1['balance'] == 0

@pytest.mark.anyio
async def test_pay_multiple_participants(client):
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
    response_payment = await client.post("/payments", json=payment_json, headers=headers)
    

    response_debt = await client.put("/debts/1", json=update_debt_to_json(DebtState.PAID), headers=headers)

    response_debt_get = await client.get("/debts/1", headers=headers)


    # THEN
    assert response_debt.status_code == 200
    await duplicate_tests.verify_debt(client, 0, headers)



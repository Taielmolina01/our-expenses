import pytest
from src.tests.util_functions import *
from src.service.exceptions.debts_exceptions import *

@pytest.mark.anyio
async def register_user_1(client):
    user = create_user_model()
    return await register_user(user, client)

@pytest.mark.anyio
async def register_user_2(client):
    user = create_user_model_2()
    return await register_user(user, client)

@pytest.mark.anyio
async def register_user(user, client):
    await client.post("/users", json=user_to_json(user))

    response = await log_in_user(client, user)
    access_token = response.json()["access_token"]

    return {"Authorization": f"Bearer {access_token}"}

@pytest.mark.anyio
async def not_part_of_event(client):
    user_not_in_group = create_user_model_not_registered()
    user = create_user_model()

    await client.post("/users", json=user_to_json(user))
    await client.post("/users", json=user_to_json(user_not_in_group))
    
    response = await log_in_user(client, user)
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    
    group = create_group_model()
    await client.post("/groups", json=group_to_json(group), headers=headers) 
    return headers

@pytest.mark.anyio
async def single_participant_event(client):
    headers = await register_user_1(client)
    
    group_model = create_group_model()
    await client.post("/groups", json=group_to_json(group_model), headers=headers)
    return headers

@pytest.mark.anyio
async def multiple_participants_event(client):
    user_model_1 = create_user_model()
    user_model_2 = create_user_model_2()
    await client.post("/users", json=user_to_json(user_model_1))
    await client.post("/users", json=user_to_json(user_model_2))

    response = await log_in_user(client, user_model_1)
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    group_model = create_group_model()
    result_group = await client.post("/groups", json=group_to_json(group_model), headers=headers)

    group = json_to_group(result_group.json())

    addition_2 = create_user_in_group_model(user_model_2, group)
    
    myId = result_group.json().get("group_id")
    await client.post(f"/groups/{myId}/users/{user_model_2.email}", json=user_in_group_to_json(addition_2), headers=headers)
    return headers

@pytest.mark.anyio
async def verify_debt(client, debt: int, headers):
    response_user_1 = await client.get("/users/test@example.com")
    response_user_2 = await client.get("/users/test2@example.com")
    response_group = await client.get("/groups/1", headers=headers)

    assert response_user_1.status_code == 200
    assert response_user_2.status_code == 200
    assert response_group.status_code == 200

    user_base_1 = json_to_user(response_user_1.json())
    user_base_2 = json_to_user(response_user_2.json())
    group_base = json_to_group(response_group.json())

    params_creditor = {"role": "creditor"}
    params_debtor = {"role": "debtor"}
    response_debt_creditor = await client.get(f"/debts/user/{user_base_1.email}", params=params_creditor, headers=headers)
    response_debt_debtor = await client.get(f"/debts/user/{user_base_2.email}", params=params_debtor, headers=headers)

    print(response_debt_creditor)

    assert response_debt_creditor.status_code == 200
    assert response_debt_debtor.status_code == 200

    debt_by_creditor = json_to_debts(response_debt_creditor.json())[0]
    debt_by_debtor = json_to_debts(response_debt_debtor.json())[0]

    assert debt_by_creditor.group_id == debt_by_debtor.group_id == group_base.group_id
    assert debt_by_creditor.creditor_email == debt_by_debtor.creditor_email == user_base_1.email
    assert debt_by_creditor.debtor_email == debt_by_debtor.debtor_email == user_base_2.email
    assert debt_by_creditor.debt_id == debt_by_debtor.debt_id == 1
    assert debt_by_creditor.payment_id == debt_by_debtor.payment_id == 1
    assert debt_by_creditor.percentage == debt_by_debtor.percentage == 0.5

    balance_user_1_group_1 = await client.get(f"/groups/{group_base.group_id}/users/{user_base_1.email}", headers=headers)
    balance_user_2_group_1 = await client.get(f"/groups/{group_base.group_id}/users/{user_base_2.email}", headers=headers)

    balance_user_1_group_1 = balance_user_1_group_1.json()
    balance_user_2_group_1 = balance_user_2_group_1.json()

    assert balance_user_1_group_1["balance"] == -debt
    assert balance_user_2_group_1["balance"] == debt

@pytest.mark.anyio
async def event_with_payments(client):
    user_model_1 = create_user_model()
    user_model_2 = create_user_model_2()
    response_user_1 = await client.post("/users", json=user_to_json(user_model_1))
    response_user_2 = await client.post("/users", json=user_to_json(user_model_2))

    user_base_1 = json_to_user(response_user_1.json())
    user_base_2 = json_to_user(response_user_2.json())

    response = await log_in_user(client, user_model_1)
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    group_model = create_group_model()
    result_group = await client.post("/groups", json=group_to_json(group_model), headers=headers)

    group = json_to_group(result_group.json())

    addition_2 = create_user_in_group_model(user_model_2, group)
    
    myId = result_group.json().get("group_id")
    await client.post(f"/groups/{myId}/users/{user_model_2.email}", json=user_in_group_to_json(addition_2), headers=headers)
    
    payment_json = payment_to_json(create_payment_model(user_base_1, group, Category.ENTERTAINMENT), {user_base_1.email: 0.5, user_base_2.email: 0.5})
    await client.post("/payments", json=payment_json, headers=headers)
    
    return headers
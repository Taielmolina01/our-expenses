import pytest
from src.service.exceptions.groups_exceptions import *
from datetime import date
from src.tests import duplicate_tests
from src.tests.util_functions import *

@pytest.mark.anyio
async def test_invite_unloged(client):
    # GIVEN
    await client.post("/users", json=user_to_json(create_user_model()))

    # WHEN
    response = await invite_guest(client, {})

    # THEN
    assert response.status_code == 401

@pytest.mark.anyio
async def test_invite_unregistered_members(client):
    # GIVEN
    headers = await duplicate_tests.register_user_1(client)

    # WHEN
    response_user = await client.get("/users/test@example.com")
    assert response_user.status_code == 200
    host = json_to_user(response_user.json())

    await client.post("/groups", json=group_to_json(create_group_model()))

    response = await client.post("/invitations", json=invitation_to_json(create_invitation_model(host.email, "not_registed@example.com")), headers=headers)

    # THEN
    assert response.status_code == 404

@pytest.mark.anyio
async def test_invite_registered_members(client):
    # GIVEN
    headers = await duplicate_tests.register_user_1(client)

    # WHEN
    await invite_guest(client, headers)

    # THEN
    result_invitation = await client.get("/invitations/test2@example.com", headers=headers)
    assert result_invitation.status_code == 200

    invitations = json_to_invitation(result_invitation.json())
    invitation = invitations[0]

    assert invitation.invitation_id == 1
    assert invitation.invitator_email == "test@example.com"
    assert invitation.guest_email == "test2@example.com"
    assert invitation.group_id == 1
    assert invitation.send_date == date(2024, 10, 21)
    assert invitation.expire_date == date(2024, 10, 28)

@pytest.mark.anyio
async def invite_guest(client, headers):
    group_model = create_group_model()
    await client.post("/groups", json=group_to_json(group_model), headers=headers)

    guest = create_user_model_2()
    await client.post("/users", json=user_to_json(guest))

    response_user = await client.get("/users/test@example.com")
    assert response_user.status_code == 200
    host = json_to_user(response_user.json())

    return await client.post("/invitations", json=invitation_to_json(create_invitation_model(host.email, guest.email)), headers=headers)

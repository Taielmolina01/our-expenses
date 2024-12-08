import pytest
from src.service.exceptions.users_exceptions import *
from src.service.exceptions.users_exceptions import *
from src.tests.util_functions import *


@pytest.mark.anyio
async def test_not_registered(client):
    # GIVEN
    user = create_user_model()

    # WHEN
    response = await log_in_user(client, user)

    # THEN

    assert response.status_code == 404

@pytest.mark.anyio
async def test_registered_and_wrong_password(client):
    # GIVEN
    user = create_user_model()
    await client.post("/users", json=user_to_json(user))

    # WHEN
    data = {
        "username": user.email,
        "password": "wrongpassword"
    }
    response = await client.post("/login", data=data)

    # THEN
    assert response.status_code == 401

@pytest.mark.anyio
async def test_registered_and_correct_password(client):
    # GIVEN
    user = create_user_model()
    await client.post("/users", json=user_to_json(user))

    # WHEN
    data = {
        "username": "test@example.com",
        "password": "securepassword1"
    }
    response = await client.post("/login", data=data)

    # THEN
    assert response.status_code == 200

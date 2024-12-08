import pytest
from src.service.exceptions.users_exceptions import *
from src.service.exceptions.users_exceptions import *
from src.tests import duplicate_tests
from src.tests.util_functions import *

@pytest.mark.anyio
async def test_update_unregistered_user(client):
    # GIVEN

    # WHEN
    update = {
        "name": "Unregistered User"
    }
    response = await client.put("/users/test@example.com", json=update)

    # THEN
    assert response.status_code == 404

@pytest.mark.anyio
async def test_update_with_invalid_fields(client):
    # GIVEN
    await duplicate_tests.register_user_1(client)

    # WHEN
    update = {
        "name": ""
    }
    response = await client.put("/users/test@example.com", json=update)

    # THEN
    assert response.status_code == 422
    
    result_user = await client.get("/users/test@example.com")
    assert result_user.status_code == 200
    user = json_to_user(result_user.json())
    
    assert user.email == "test@example.com"
    assert user.name == "MyUser1"

@pytest.mark.anyio
async def test_update_user(client):
    # GIVEN
    await duplicate_tests.register_user_1(client)

    # WHEN
    update = {
        "name": "MyNewName"
    }
    response = await client.put("/users/test@example.com", json=update)

    # THEN
    assert response.status_code == 200
    
    result_user = await client.get("/users/test@example.com")
    assert result_user.status_code == 200
    user = json_to_user(result_user.json())
    
    assert user.email == "test@example.com"
    assert user.name == "MyNewName"

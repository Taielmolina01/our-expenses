import pytest
from src.service.exceptions.users_exceptions import *
from src.service.exceptions.users_exceptions import *
from src.tests.util_functions import *
from src.utils.login_utils import verify_password

@pytest.mark.anyio
async def test_register_with_existing_email(client):
        # GIVEN

        # WHEN
        user_model_1 = create_user_model()
        await client.post("/users", json=user_to_json(user_model_1))
        await client.post("/users", json=user_to_json(user_model_1))
        response = await client.post("/users", json=user_to_json(user_model_1))

        # THEN
        assert response.status_code == 400

@pytest.mark.anyio
async def test_register_with_valid_email_and_password(client):
        # GIVEN

        # WHEN
        user_model_1 = create_user_model()
        await client.post("/users", json=user_to_json(user_model_1))

        # THEN
        response_user = await client.get("/users/test@example.com")
        assert response_user.status_code == 200
        user = json_to_user(response_user.json())

        assert user.email == "test@example.com"
        assert user.name == "MyUser1"
        assert verify_password("securepassword1", user.password) == True

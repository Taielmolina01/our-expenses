import pytest
from src.tests.util_functions import *
from src.models.payment import Category
from src.tests import duplicate_tests

@pytest.mark.anyio
async def test_get_payment_categories(client):
        # GIVEN
        headers = await duplicate_tests.not_part_of_event(client)

        # WHEN
        request = await client.get("/payments/options", headers=headers)


        # THEN
        assert request.status_code == 200
        assert request.json() == [c.name for c in Category]

@pytest.mark.anyio
async def test_get_payment_categories_unlogged(client):
        # GIVEN

        # WHEN
        request = await client.get("/payments/options", headers={})

        # THEN
        assert request.status_code == 401
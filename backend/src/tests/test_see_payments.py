import pytest
from src.tests import duplicate_tests
from src.tests.util_functions import *

@pytest.mark.anyio
async def test_see_group_with_payments(client):
    # GIVEN
    headers = await duplicate_tests.event_with_payments(client)

    # WHEN
    result_payments = await client.get("/groups/1/payments", headers=headers)

    assert result_payments.status_code == 200

    payments = result_payments.json()

    # THEN
    payments = json_to_payments(payments)
    assert len(payments) == 1
    assert payments[0].category == Category.ENTERTAINMENT.value

@pytest.mark.anyio
async def test_see_group_without_payments(client):
    # GIVEN
    headers = await duplicate_tests.multiple_participants_event(client)

    # WHEN
    result_payments = await client.get("/groups/1/payments", headers=headers)

    assert result_payments.status_code == 200

    payments = result_payments.json()

    # THEN
    assert len(payments) == 0

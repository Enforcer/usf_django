import pytest
from djmoney.money import Money
from insurance.services import get_insurance_fee


@pytest.mark.parametrize(
    "price, expected_fee",
    [
        (Money(1, "USD"), Money(2, "USD")),
        (Money(5, "USD"), Money(2, "USD")),
        (Money(9.99, "USD"), Money(2, "USD")),
        (Money(10, "USD"), Money(2, "USD")),
    ],
)
def test_insurance_fee_is_2_for_all_items_priced_lte_10(
    price: Money, expected_fee: Money
) -> None:
    fee = get_insurance_fee(price)

    assert fee == expected_fee


@pytest.mark.parametrize(
    "price, expected_fee",
    [
        (Money(20, "USD"), Money(4, "USD")),
        (Money(10.01, "USD"), Money(3, "USD")),
        (Money(16.99, "USD"), Money(3.7, "USD")),
        (Money(100, "USD"), Money(12, "USD")),
    ],
)
def test_insurance_fee_is_2_plus_10_percent_for_items_priced_above_10(
    price: Money, expected_fee: Money
) -> None:
    fee = get_insurance_fee(price)

    assert fee == expected_fee

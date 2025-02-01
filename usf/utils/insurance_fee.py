from decimal import Decimal

from moneyed import Money


def get_insurance_fee(price: Money) -> Money:
    if price.amount <= 10:
        return Money(2, price.currency)
    else:
        rounded_ten_percent = round(price.amount * Decimal("0.1"), 2)
        return Money(rounded_ten_percent + 2, price.currency)

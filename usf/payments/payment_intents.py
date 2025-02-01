import stripe
from moneyed import Money
from stripe import PaymentIntent


def create_payment_intent(amount: Money) -> PaymentIntent:
    return stripe.PaymentIntent.create(
        amount=int(amount.amount * 100),
        currency=amount.currency.code,
        automatic_payment_methods={"enabled": True},
    )

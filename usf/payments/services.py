from moneyed import Money
from utils.payment_id import PaymentId
from utils.user_id import UserId

from payments.models import Payment
from payments.payment_intents import create_payment_intent


def start_payment(amount: Money, payer_id: UserId) -> PaymentId:
    payment_intent = create_payment_intent(amount)
    payment = Payment(
        amount=amount.amount,
        amount_currency=amount.currency.code,
        created_by_id=payer_id,
        payment_intent_id=payment_intent.id,
        client_secret=str(payment_intent.client_secret),
    )
    payment.save()
    return payment.pk

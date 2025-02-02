from dataclasses import dataclass

from shared.payment_id import PaymentId


@dataclass(frozen=True)
class PaymentFinalized:
    payment_id: PaymentId

from ext.typed_signal import TypedSignal

from payments.events import PaymentFinalized

payment_finalized = TypedSignal[PaymentFinalized]()

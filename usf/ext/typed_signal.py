from typing import Any, Protocol

from django.dispatch import Signal

type Response = Any


class Receiver[TEvent](Protocol):
    def __call__(self, event: TEvent, **kwargs: Any) -> Any: ...


class TypedSignal[TEvent](Signal):
    def publish(self, event: TEvent) -> list[tuple[Receiver[TEvent], Response]]:
        return self.send(sender=None, event=event)

    def subscribe(self, receiver: Receiver[TEvent]) -> None:
        self.connect(receiver)

"""Small contracts for future channel adapters; no Discord dependency is required."""

from dataclasses import dataclass
from typing import Literal, Protocol

from app.domain import User


@dataclass(frozen=True)
class ChannelMessage:
    provider: str
    event_id: str
    conversation_id: str
    external_sender_id: str
    kind: Literal["group", "dm"]
    text: str


@dataclass(frozen=True)
class OutboundMessage:
    provider: str
    destination: str
    text: str
    deduplication_key: str


class MessagingAdapter(Protocol):
    """Verify identities at ingress and distinguish accepted from delivered messages.

    Implementations must map external identities to approved backend users; they
    must not accept caller-supplied roles. Provider scopes must remain separate.
    """

    async def resolve_sender(self, message: ChannelMessage) -> User | None: ...

    async def send(self, message: OutboundMessage) -> str:
        """Return the provider delivery ID; preserve uncertainty on interrupted sends."""
        ...

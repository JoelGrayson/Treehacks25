"""WebSocket event router and handler."""

from typing import Dict, Any
from fastapi import WebSocket
from dataclasses import asdict
from app.models import BitEvent, StateBit
from app.keyboard.textual_toy import AutocorrectEngine
from app.api.bit import handle


class WebSocketHandler:
    def __init__(self):
        self.autocorrect = AutocorrectEngine()
        self.current_bits = ""

    async def handle_connection(self, websocket: WebSocket):
        """Handle incoming WebSocket connection and route events."""
        await websocket.accept()

        while True:
            message = await websocket.receive_json()
            event_type = message.get("event")
            assert event_type, "Event type is required"
            data = message.get("data", {})

            response = await self.route_event(event_type, data)
            if response:
                await websocket.send_json(response)

    async def route_event(
        self, event_type: str, data: Dict[str, Any]
    ) -> Dict[str, Any] | None:
        """Route events to appropriate handlers based on event type."""
        if event_type == "bit":
            bit_event = BitEvent(**data)
            self.current_bits, word_event = await handle(
                StateBit(bit_event.bit),
                self.current_bits,
                self.autocorrect,
            )
            return asdict(word_event)

        return None  # Unhandled event type

from typing import Literal
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from textual.app import App
from textual.widgets import Static
from textual.reactive import reactive
from app.models import BitEvent, WordEvent
from app.api.ws_handler import WebSocketHandler
from app.config.settings import settings
from app.keyboard.utils import binary_to_word, pad_coding
import uvicorn
import asyncio

# Initialize FastAPI
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# TUI Message Display App
class MessageDisplay(App):
    """Textual application for displaying bit streams and word suggestions."""

    current_bits = reactive("")
    suggestions = reactive([])
    complete_word = reactive(None)

    def compose(self):
        """Create and yield widgets for the app."""
        yield Static(id="bit_display")
        yield Static(id="suggestions")

    def watch_current_bits(self, bits: str) -> None:
        """Update bit display with padded visualization."""
        if not bits:
            self.query_one("#bit_display").update("")
            return

        if self.complete_word:
            code, text = pad_coding(self.complete_word)
            display = f"Bits: {bits}\nWord: {self.complete_word}\n{code}\n{text}"
        else:
            display = f"Bits: {bits}"
        self.query_one("#bit_display").update(display)

    def watch_suggestions(self, suggestions: list) -> None:
        """Update suggestions display."""
        if not suggestions:
            self.query_one("#suggestions").update("")
            return

        display = "Suggestions:\n" + "\n".join(f"- {s}" for s in suggestions)
        self.query_one("#suggestions").update(display)

    def watch_complete_word(self, word: str) -> None:
        """Trigger bit display update when word completes."""
        self.watch_current_bits(self.current_bits)


# Global bridge for message passing
bridge = {"app": None}


# Initialize WebSocket handler with bridge
class BridgedWebSocketHandler(WebSocketHandler):
    # Intercepts WS handler response to force display on TUI
    """WebSocket handler that updates TUI display."""

    async def route_event(self, event_type: str, data: dict) -> dict | None:
        """Route events and update TUI display."""
        response = await super().route_event(event_type, data)

        if event_type == "bit" and bridge["app"] and response:
            word_event = WordEvent(**response)
            app = bridge["app"]
            app.current_bits = word_event.bits
            app.suggestions = word_event.suggestions
            app.complete_word = word_event.complete_word

        return response


ws_handler = BridgedWebSocketHandler()


@app.post("/print")
async def print_message(binary: str):
    """Endpoint to receive binary strings and display word conversions."""
    if not all(c in "01" for c in binary):
        return {"error": "Input must be a binary string"}

    word = binary_to_word(binary)
    if word is None:
        word = f"[No word match for {binary}]"

    if bridge["app"]:
        bridge["app"].messages = bridge["app"].messages + [f"{binary} -> {word}"]
    return {"status": "ok", "word": word}


@app.get("/")
async def home():
    return RedirectResponse(url="/index.html")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for streaming events to web client"""
    await ws_handler.handle_connection(websocket)


async def run_server():
    """Run FastAPI server in the background."""
    print("start fastapi")
    config = uvicorn.Config(app, host="0.0.0.0", port=settings.PORT, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    """Run Textual app with API in background."""
    # Start FastAPI
    server_task = asyncio.create_task(run_server())
    await asyncio.sleep(1)  # Give FastAPI time to start

    # Start Textual app
    app = MessageDisplay()
    bridge["app"] = app

    try:
        print("start textual")
        await app.run_async()
    finally:
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass


if __name__ == "__main__":
    # print(f"BCI App Server Active on {settings.ENV} 🚀")
    asyncio.run(main())

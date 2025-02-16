from fastapi import FastAPI
from textual.app import App
from textual.widgets import Static
from textual.reactive import reactive
import uvicorn
import asyncio


class MessageDisplay(App):
    """Main Textual application for displaying messages."""

    messages = reactive([])

    def compose(self):
        """Create and yield widgets for the app."""
        yield Static(id="message_field")

    def watch_messages(self, messages: list) -> None:
        """Update display when messages list changes."""
        self.query_one("#message_field").update("\n".join(messages))


# Global bridge for message passing
bridge = {"app": None}
api = FastAPI()


@api.post("/print")
async def print_message(message: str):
    """Endpoint to receive and display messages."""
    if bridge["app"]:
        bridge["app"].messages = bridge["app"].messages + [message]
    return {"status": "ok"}


def run_api():
    """Run FastAPI in a separate process."""
    print("DEBUG: Starting FastAPI server...")  # Debug print
    uvicorn.run(api, host="0.0.0.0", port=8000, log_level="info")
    print("DEBUG: FastAPI server stopped")  # Debug print


async def main():
    """Run Textual app with API in background."""
    print("DEBUG: Starting main...")  # Debug print

    # Start FastAPI first and wait a bit to ensure it's running
    api_process = asyncio.create_task(asyncio.to_thread(run_api))
    await asyncio.sleep(1)  # Give FastAPI time to start

    print("DEBUG: Starting Textual app...")  # Debug print
    app = MessageDisplay()
    bridge["app"] = app

    try:
        await app.run_async()
    finally:
        print("DEBUG: Shutting down...")  # Debug print
        api_process.cancel()
        try:
            await api_process
        except asyncio.CancelledError:
            pass


if __name__ == "__main__":
    asyncio.run(main())

import time
from typing import Optional

from google.genai import Client

from .config import settings


TERMINAL_STATES = {
    "completed",
    "failed",
    "cancelled",
}


def start_background_interaction(
    client: Client,
    prompt: str,
):
    """
    Start a Gemini background interaction.
    """

    interaction = client.interactions.create(
        model=settings.model,
        input=prompt,
        background=True,
    )

    return interaction


def get_interaction(
    client: Client,
    interaction_id: str,
):
    """
    Retrieve an existing interaction.
    """

    return client.interactions.get(
        id=interaction_id
    )


def wait_for_interaction(
    client: Client,
    interaction_id: str,
    poll_seconds: Optional[int] = None,
):
    """
    Poll until the interaction reaches a terminal state.
    """

    interval = (
        poll_seconds
        if poll_seconds is not None
        else settings.poll_seconds
    )

    for _ in range(settings.max_polls):
        result = get_interaction(
            client,
            interaction_id,
        )

        print(f"Status: {result.status}")

        if result.status in TERMINAL_STATES:
            return result

        time.sleep(interval)

    raise TimeoutError(
        "Gemini interaction did not complete "
        f"within {settings.max_polls} polling attempts."
    )


def cancel_interaction(
    client: Client,
    interaction_id: str,
):
    """
    Cancel a running interaction.
    """

    return client.interactions.cancel(
        id=interaction_id
    )

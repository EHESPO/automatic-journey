import os
import time

from google import genai


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "ehepso-nonprofit-eb1db")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")


def create_client() -> genai.Client:
    """Create a Gemini client using Vertex AI."""

    return genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION,
    )


def run_background_interaction(
    client: genai.Client,
    prompt: str,
    poll_seconds: int = 3,
):
    """Create and monitor a background Gemini interaction."""

    interaction = client.interactions.create(
        model=MODEL,
        input=prompt,
        background=True,
    )

    interaction_id = interaction.id

    print(f"Created interaction: {interaction_id}")

    while True:
        result = client.interactions.get(id=interaction_id)

        print(f"Status: {result.status}")

        if result.status in ("completed", "succeeded"):
            print("\n--- Gemini Output ---\n")
            print(result.output_text)
            return result

        if result.status in ("failed", "cancelled"):
            raise RuntimeError(
                f"Gemini interaction ended with status: {result.status}"
            )

        time.sleep(poll_seconds)


def main():
    client = create_client()

    prompt = """
You are the EHEPS AI engineering assistant.

Create a technical guide explaining how EHEPS can use
Gemini Background Interactions for long-running AI tasks.

Include:
1. Architecture
2. Authentication
3. Google Cloud requirements
4. Python implementation
5. Error handling
6. Monitoring
7. Security considerations
8. Example production use cases

Do not invent Google Cloud APIs or capabilities.
Clearly distinguish confirmed functionality from recommendations.
"""

    run_background_interaction(client, prompt)


if __name__ == "__main__":
    main()

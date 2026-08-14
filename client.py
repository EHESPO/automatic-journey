from google import genai

from .config import settings


def create_client() -> genai.Client:
    """
    Create a Gemini client using Vertex AI configuration.
    """

    return genai.Client(
        vertexai=True,
        project=settings.project_id,
        location=settings.location,
    )

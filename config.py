from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    project_id: str = os.getenv(
        "GOOGLE_CLOUD_PROJECT",
        "ehepso-nonprofit-eb1db",
    )

    project_number: str = os.getenv(
        "GOOGLE_CLOUD_PROJECT_NUMBER",
        "286452521627",
    )

    location: str = os.getenv(
        "GOOGLE_CLOUD_LOCATION",
        "us-central1",
    )

    model: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.6-flash",
    )

    poll_seconds: int = int(
        os.getenv("GEMINI_POLL_SECONDS", "5")
    )

    max_polls: int = int(
        os.getenv("GEMINI_MAX_POLLS", "120")
    )


settings = Settings()

import argparse

from .client import create_client
from .cloud_links import CLOUD_LINKS
from .config import settings
from .interactions import (
    start_background_interaction,
    wait_for_interaction,
)


DEFAULT_PROMPT = """
You are the EHEPS AI engineering assistant.

Analyze the active EHEPS Google Cloud environment and produce
a technical architecture report covering:

1. Gemini and Agent Platform
2. BigQuery
3. IAM
4. Identity and access management
5. Security
6. Asset inventory
7. Recommended architecture
8. Risks and controls

Do not claim that you accessed a Google Cloud resource unless
the application actually retrieved that resource.

Do not request or expose passwords, API keys, OAuth tokens,
service-account private keys, wallet secret keys, or recovery
phrases.

Clearly distinguish confirmed information from assumptions.
"""


def print_environment():
    print()
    print("EHEPS Gemini Environment")
    print("========================")
    print(f"Project ID:     {settings.project_id}")
    print(f"Project Number: {settings.project_number}")
    print(f"Location:       {settings.location}")
    print(f"Model:          {settings.model}")
    print()

    print("Google Cloud Console")
    print("--------------------")
    print(f"Agent Studio:    {CLOUD_LINKS.agent_studio}")
    print(f"Agent Platform:  {CLOUD_LINKS.agent_platform}")
    print(f"BigQuery:        {CLOUD_LINKS.bigquery}")
    print(f"IAP:             {CLOUD_LINKS.iap}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="EHEPS Gemini Background Interaction CLI"
    )

    parser.add_argument(
        "--prompt",
        default=DEFAULT_PROMPT,
        help="Prompt sent to Gemini.",
    )

    parser.add_argument(
        "--environment",
        action="store_true",
        help="Display configured Google Cloud resources.",
    )

    args = parser.parse_args()

    if args.environment:
        print_environment()
        return

    client = create_client()

    interaction = start_background_interaction(
        client,
        args.prompt,
    )

    print(
        f"Created background interaction: "
        f"{interaction.id}"
    )

    result = wait_for_interaction(
        client,
        interaction.id,
    )

    print()
    print("========== RESULT ==========")
    print()

    if result.status == "completed":
        print(result.output_text)
    else:
        print(f"Interaction ended: {result.status}")

        if hasattr(result, "error"):
            print(result.error)


if __name__ == "__main__":
    main()

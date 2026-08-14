"""
EHEPS Google Cloud Console Links
Project: ehepso-nonprofit-eb1db
Project number: 286452521627
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class GoogleCloudLinks:
    project_id: str = "ehepso-nonprofit-eb1db"
    project_number: str = "286452521627"

    agent_studio: str = (
        "https://console.cloud.google.com/"
        "agent-platform/studio?project=ehepso-nonprofit-eb1db"
    )

    agent_platform: str = (
        "https://console.cloud.google.com/"
        "agent-platform?project=ehepso-nonprofit-eb1db"
    )

    bigquery: str = (
        "https://console.cloud.google.com/"
        "bigquery?project=ehepso-nonprofit-eb1db"
    )

    iap: str = (
        "https://console.cloud.google.com/"
        "iam-admin/iap?project=ehepso-nonprofit-eb1db"
    )

    asset_inventory_green_tract: str = (
        "https://console.cloud.google.com/"
        "iam-admin/asset-inventory"
        "?organizationId=&project=green-tract-492313-q2&folder="
    )

    asset_inventory_gen_lang: str = (
        "https://console.cloud.google.com/"
        "iam-admin/asset-inventory"
        "?organizationId=&project=gen-lang-client-0185746302&folder="
    )

    asset_inventory_green_tract_alt: str = (
        "https://console.cloud.google.com/"
        "iam-admin/asset-inventory"
        "?project=green-tract-492313-q2&folder=&organizationId="
    )

    asset_inventory_education: str = (
        "https://console.cloud.google.com/"
        "iam-admin/asset-inventory"
        "?project=education-and-hu-1775216724036&folder=&organizationId="
    )

    asset_inventory_ehepso: str = (
        "https://console.cloud.google.com/"
        "iam-admin/asset-inventory"
        "?project=gen-lang-client-0185746302"
        "&folder=&organizationId="
        "firebase-adminsdk-fbsvc@ehepso-nonprofit-eb1db.iam.gserviceaccount.com"
    )


LINKS = GoogleCloudLinks()


def print_links() -> None:
    print(f"Project ID:     {LINKS.project_id}")
    print(f"Project Number: {LINKS.project_number}")
    print()

    links = {
        "Agent Studio": LINKS.agent_studio,
        "Agent Platform": LINKS.agent_platform,
        "BigQuery": LINKS.bigquery,
        "IAP": LINKS.iap,
        "Asset Inventory — green-tract": LINKS.asset_inventory_green_tract,
        "Asset Inventory — gen-lang": LINKS.asset_inventory_gen_lang,
        "Asset Inventory — green-tract (alternate)": (
            LINKS.asset_inventory_green_tract_alt
        ),
        "Asset Inventory — education": LINKS.asset_inventory_education,
        "Asset Inventory — EHEPS": LINKS.asset_inventory_ehepso,
    }

    for name, url in links.items():
        print(f"{name}:")
        print(f"  {url}")
        print()


if __name__ == "__main__":
    print_links()

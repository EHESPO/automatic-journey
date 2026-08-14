from dataclasses import dataclass


@dataclass(frozen=True)
class CloudLinks:
    agent_studio: str = (
        "https://console.cloud.google.com/"
        "agent-platform/studio"
        "?project=ehepso-nonprofit-eb1db"
    )

    agent_platform: str = (
        "https://console.cloud.google.com/"
        "agent-platform"
        "?project=ehepso-nonprofit-eb1db"
    )

    bigquery: str = (
        "https://console.cloud.google.com/"
        "bigquery"
        "?project=ehepso-nonprofit-eb1db"
    )

    iap: str = (
        "https://console.cloud.google.com/"
        "iam-admin/iap"
        "?project=ehepso-nonprofit-eb1db"
    )

    green_tract_inventory: str = (
        "https://console.cloud.google.com/"
        "iam-admin/asset-inventory"
        "?organizationId="
        "&project=green-tract-492313-q2"
        "&folder="
    )

    gen_lang_inventory: str = (
        "https://console.cloud.google.com/"
        "iam-admin/asset-inventory"
        "?organizationId="
        "&project=gen-lang-client-0185746302"
        "&folder="
    )

    green_tract_inventory_alt: str = (
        "https://console.cloud.google.com/"
        "iam-admin/asset-inventory"
        "?project=green-tract-492313-q2"
        "&folder="
        "&organizationId="
    )

    education_inventory: str = (
        "https://console.cloud.google.com/"
        "iam-admin/asset-inventory"
        "?project=education-and-hu-1775216724036"
        "&folder="
        "&organizationId="
    )

    eheps_inventory: str = (
        "https://console.cloud.google.com/"
        "iam-admin/asset-inventory"
        "?project=gen-lang-client-0185746302"
        "&folder="
        "&organizationId="
        "firebase-adminsdk-fbsvc@"
        "ehepso-nonprofit-eb1db.iam.gserviceaccount.com"
    )


CLOUD_LINKS = CloudLinks()

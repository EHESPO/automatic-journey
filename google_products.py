"""
EHEPS Google Cloud / Gemini Product Registry.

Project:
    ehepso-nonprofit-eb1db

Domains:
    https://eheps.com
    https://eheps.org

This registry stores navigation/documentation links only.
It does not grant permissions or modify Google Cloud resources.
"""

from dataclasses import dataclass


PROJECT_ID = "ehepso-nonprofit-eb1db"
PROJECT_NUMBER = "286452521627"
REGION = "us-central1"

EHEPS_DOMAINS = {
    "primary": "https://eheps.com",
    "organization": "https://eheps.org",
}


@dataclass(frozen=True)
class GoogleProduct:
    name: str
    category: str
    website: str
    documentation: str
    console: str | None = None


def console_url(path: str) -> str:
    """Build a Google Cloud Console URL for the EHEPS project."""
    separator = "&" if "?" in path else "?"
    return (
        f"https://console.cloud.google.com/"
        f"{path}{separator}project={PROJECT_ID}"
    )


GOOGLE_PRODUCTS = {
    "gemini": GoogleProduct(
        name="Gemini",
        category="AI",
        website="https://gemini.google.com/",
        documentation="https://ai.google.dev/gemini-api/docs",
    ),

    "genai_sdk": GoogleProduct(
        name="Google GenAI SDK",
        category="AI / Developer",
        website="https://ai.google.dev/",
        documentation="https://googleapis.github.io/python-genai/",
    ),

    "vertex_ai": GoogleProduct(
        name="Vertex AI",
        category="AI / ML",
        website="https://cloud.google.com/vertex-ai",
        documentation="https://cloud.google.com/vertex-ai/docs",
        console=console_url("vertex-ai"),
    ),

    "agent_platform": GoogleProduct(
        name="Gemini Enterprise Agent Platform",
        category="AI / Agents",
        website="https://cloud.google.com/products/agent-platform",
        documentation="https://cloud.google.com/agent-platform/docs",
        console=console_url("agent-platform"),
    ),

    "ai_studio": GoogleProduct(
        name="Google AI Studio",
        category="AI / Developer",
        website="https://aistudio.google.com/",
        documentation="https://ai.google.dev/gemini-api/docs",
    ),

    "bigquery": GoogleProduct(
        name="BigQuery",
        category="Data",
        website="https://cloud.google.com/bigquery",
        documentation="https://cloud.google.com/bigquery/docs",
        console=console_url("bigquery"),
    ),

    "cloud_run": GoogleProduct(
        name="Cloud Run",
        category="Application Hosting",
        website="https://cloud.google.com/run",
        documentation="https://cloud.google.com/run/docs",
        console=console_url("run"),
    ),

    "artifact_registry": GoogleProduct(
        name="Artifact Registry",
        category="Developer / Supply Chain",
        website="https://cloud.google.com/artifact-registry",
        documentation="https://cloud.google.com/artifact-registry/docs",
        console=console_url("artifacts"),
    ),

    "cloud_build": GoogleProduct(
        name="Cloud Build",
        category="CI/CD",
        website="https://cloud.google.com/build",
        documentation="https://cloud.google.com/build/docs",
        console=console_url("cloud-build"),
    ),

    "iam": GoogleProduct(
        name="Identity and Access Management",
        category="Security",
        website="https://cloud.google.com/iam",
        documentation="https://cloud.google.com/iam/docs",
        console=console_url("iam-admin"),
    ),

    "cloud_asset_inventory": GoogleProduct(
        name="Cloud Asset Inventory",
        category="Security / Governance",
        website="https://cloud.google.com/asset-inventory",
        documentation="https://cloud.google.com/asset-inventory/docs",
        console=console_url("iam-admin/asset-inventory"),
    ),

    "iap": GoogleProduct(
        name="Identity-Aware Proxy",
        category="Security",
        website="https://cloud.google.com/iap",
        documentation="https://cloud.google.com/iap/docs",
        console=console_url("security/iap"),
    ),

    "secret_manager": GoogleProduct(
        name="Secret Manager",
        category="Security",
        website="https://cloud.google.com/security/products/secret-manager",
        documentation="https://cloud.google.com/secret-manager/docs",
        console=console_url("security/secret-manager"),
    ),

    "cloud_storage": GoogleProduct(
        name="Cloud Storage",
        category="Storage",
        website="https://cloud.google.com/storage",
        documentation="https://cloud.google.com/storage/docs",
        console=console_url("storage/browser"),
    ),

    "cloud_sql": GoogleProduct(
        name="Cloud SQL",
        category="Database",
        website="https://cloud.google.com/sql",
        documentation="https://cloud.google.com/sql/docs",
        console=console_url("sql"),
    ),

    "cloud_dns": GoogleProduct(
        name="Cloud DNS",
        category="Networking",
        website="https://cloud.google.com/dns",
        documentation="https://cloud.google.com/dns/docs",
        console=console_url("net-services/dns/zones"),
    ),

    "logging": GoogleProduct(
        name="Cloud Logging",
        category="Observability",
        website="https://cloud.google.com/logging",
        documentation="https://cloud.google.com/logging/docs",
        console=console_url("logs"),
    ),

    "monitoring": GoogleProduct(
        name="Cloud Monitoring",
        category="Observability",
        website="https://cloud.google.com/monitoring",
        documentation="https://cloud.google.com/monitoring/docs",
        console=console_url("monitoring"),
    ),

    "security_command_center": GoogleProduct(
        name="Security Command Center",
        category="Security",
        website="https://cloud.google.com/security-command-center",
        documentation="https://cloud.google.com/security-command-center/docs",
        console=console_url("security/command-center"),
    ),

    "sensitive_data_protection": GoogleProduct(
        name="Sensitive Data Protection",
        category="Security / DLP",
        website="https://cloud.google.com/sensitive-data-protection",
        documentation="https://cloud.google.com/sensitive-data-protection/docs",
        console=console_url("security/sensitive-data-protection"),
    ),

    "pubsub": GoogleProduct(
        name="Pub/Sub",
        category="Integration",
        website="https://cloud.google.com/pubsub",
        documentation="https://cloud.google.com/pubsub/docs",
        console=console_url("cloudpubsub"),
    ),

    "workflows": GoogleProduct(
        name="Workflows",
        category="Automation",
        website="https://cloud.google.com/workflows",
        documentation="https://cloud.google.com/workflows/docs",
        console=console_url("workflows"),
    ),
}


def get_product(product_id: str) -> GoogleProduct:
    """Return a registered Google product."""
    try:
        return GOOGLE_PRODUCTS[product_id]
    except KeyError as exc:
        raise KeyError(
            f"Unknown Google product: {product_id}"
        ) from exc


def list_products() -> list[GoogleProduct]:
    """Return all registered Google products."""
    return list(GOOGLE_PRODUCTS.values())


def products_by_category(category: str) -> list[GoogleProduct]:
    """Return products belonging to a category."""
    return [
        product
        for product in GOOGLE_PRODUCTS.values()
        if product.category.lower() == category.lower()
    ]


def project_info() -> dict[str, str]:
    """Return EHEPS Google Cloud project metadata."""
    return {
        "project_id": PROJECT_ID,
        "project_number": PROJECT_NUMBER,
        "region": REGION,
        "primary_domain": EHEPS_DOMAINS["primary"],
        "organization_domain": EHEPS_DOMAINS["organization"],
    }


if __name__ == "__main__":
    print("EHEPS Google Product Registry")
    print("=" * 32)

    print(f"Project: {PROJECT_ID}")
    print(f"Region:  {REGION}")
    print()

    for product in list_products():
        print(f"{product.name}")
        print(f"  Website: {product.website}")
        print(f"  Docs:    {product.documentation}")

        if product.console:
            print(f"  Console: {product.console}")

        print()

"""
EHEPS domain configuration.

These domains are configuration values only.
This file does not modify DNS, Cloud Run, certificates,
Google Workspace, or any Google Cloud resource.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class EHEPSDomains:
    primary: str = "eheps.com"
    organization: str = "eheps.org"

    @property
    def primary_url(self) -> str:
        return f"https://{self.primary}"

    @property
    def organization_url(self) -> str:
        return f"https://{self.organization}"

    @property
    def all_domains(self) -> tuple[str, str]:
        return self.primary, self.organization

    @property
    def all_urls(self) -> tuple[str, str]:
        return self.primary_url, self.organization_url


DOMAINS = EHEPSDomains()


def print_domains() -> None:
    """Display configured EHEPS domains."""

    print("EHEPS Domains")
    print("-------------")
    print(f"Primary:      {DOMAINS.primary_url}")
    print(f"Organization: {DOMAINS.organization_url}")


if __name__ == "__main__":
    print_domains()

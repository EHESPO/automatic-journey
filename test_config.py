from eheps_gemini.config import settings


def test_default_project():
    assert settings.project_id == "ehepso-nonprofit-eb1db"


def test_default_project_number():
    assert settings.project_number == "286452521627"


def test_default_location():
    assert settings.location == "us-central1"

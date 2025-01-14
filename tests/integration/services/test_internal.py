import pytest
import requests

from shipyard import config


class TestInitScriptsResource:
    def test_stages_have_completed(self):
        response = requests.get(config.internal_service_url() + "/_shipyard/init")
        assert response.status_code == 200
        doc = response.json()

        assert doc["completed"] == {
            "BOOT": True,
            "START": True,
            "READY": True,
            "SHUTDOWN": False,
        }

    def test_query_nonexisting_stage(self):
        response = requests.get(config.internal_service_url() + "/_shipyard/init/does_not_exist")
        assert response.status_code == 404

    @pytest.mark.parametrize(
        ("stage", "completed"),
        [("boot", True), ("start", True), ("ready", True), ("shutdown", False)],
    )
    def test_query_individual_stage_completed(self, stage, completed):
        response = requests.get(config.internal_service_url() + f"/_shipyard/init/{stage}")
        assert response.status_code == 200
        assert response.json()["completed"] == completed


class TestHealthResource:
    def test_get(self):
        response = requests.get(config.internal_service_url() + "/_shipyard/health")
        assert response.ok
        assert "services" in response.json()
        assert "edition" in response.json()

    def test_head(self):
        response = requests.head(config.internal_service_url() + "/_shipyard/health")
        assert response.ok
        assert not response.text


class TestInfoEndpoint:
    def test_get(self):
        response = requests.get(config.internal_service_url() + "/_shipyard/info")
        assert response.ok
        doc = response.json()

        from shipyard import __version__ as version

        # we're being specifically vague here since we want this test to be robust against pro or community
        assert doc["version"].startswith(str(version))
        assert doc["session_id"]
        assert doc["machine_id"]
        assert doc["system"]
        assert type(doc["is_license_activated"]) == bool

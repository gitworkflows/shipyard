import requests

from shipyard import config
from shipyard.testing.pytest import markers

CLOUDFORMATION_UI_PATH = "/_shipyard.khulnasoft.comformation/deploy"


class TestCloudFormationUi:
    @markers.aws.only_shipyard
    def test_get_cloudformation_ui(self):
        # note: we get the external service url here because the UI is hosted on the external
        # URL, however if `SHIPYARD_HOST` is set to a hostname that does not resolve to
        # `127.0.0.1` this test will fail.
        cfn_ui_url = config.external_service_url() + CLOUDFORMATION_UI_PATH
        response = requests.get(cfn_ui_url)

        # we simply test that the UI is available at the right path and that it returns HTML.
        assert response.ok
        assert "content-type" in response.headers
        # this is a bit fragile but assert that the file returned contains at least something related to the UI
        assert b"Shipyard" in response.content

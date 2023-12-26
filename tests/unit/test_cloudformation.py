from shipyard.services.cloudformation.api_utils import is_local_service_url
from shipyard.services.cloudformation.deployment_utils import (
    PLACEHOLDER_AWS_NO_VALUE,
    remove_none_values,
)


def test_is_local_service_url():
    local_urls = [
        "http://localhost",
        "https://localhost",
        "http://localhost:4566",
        "https://localhost:4566",
        "http://localhost.shipyard.khulnasoft.com:4566",
        "https://s3.localhost.shipyard.khulnasoft.com",
        "http://mybucket.s3.localhost.shipyard.khulnasoft.com:4566",
        "https://mybucket.s3.localhost",
    ]
    remote_urls = [
        "https://mybucket.s3.amazonaws.com",
        "http://mybucket.s3.us-east-1.amazonaws.com",
    ]
    for url in local_urls:
        assert is_local_service_url(url)
    for url in remote_urls:
        assert not is_local_service_url(url)


def test_remove_none_values():
    template = {
        "Properties": {
            "prop1": 123,
            "nested": {"test1": PLACEHOLDER_AWS_NO_VALUE, "test2": None},
            "list": [1, 2, PLACEHOLDER_AWS_NO_VALUE, 3, None],
        }
    }
    result = remove_none_values(template)
    assert result == {"Properties": {"prop1": 123, "nested": {}, "list": [1, 2, 3]}}

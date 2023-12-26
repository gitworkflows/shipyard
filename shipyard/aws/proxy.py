"""
Adapters and other utilities to use ASF together with the edge proxy.
"""
import logging

from shipyard.aws.accounts import (
    get_account_id_from_access_key_id,
)
from shipyard.constants import TEST_AWS_ACCESS_KEY_ID
from shipyard.http import Request
from shipyard.utils.aws.aws_stack import extract_access_key_id_from_auth_header

LOG = logging.getLogger(__name__)


# TODO: consider moving this to `shipyard.utils.aws.request_context`
def get_account_id_from_request(request: Request) -> str:
    access_key_id = (
        extract_access_key_id_from_auth_header(request.headers) or TEST_AWS_ACCESS_KEY_ID
    )

    return get_account_id_from_access_key_id(access_key_id)

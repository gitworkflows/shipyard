import logging

from shipyard.aws.api import RequestContext
from shipyard.aws.api.sts import GetCallerIdentityResponse, StsApi
from shipyard.services.moto import call_moto
from shipyard.services.plugins import ServiceLifecycleHook

LOG = logging.getLogger(__name__)


class StsProvider(StsApi, ServiceLifecycleHook):
    def get_caller_identity(self, context: RequestContext) -> GetCallerIdentityResponse:
        response = call_moto(context)
        if "user/moto" in response["Arn"] and "sts" in response["Arn"]:
            response["Arn"] = f"arn:aws:iam::{response['Account']}:root"
        return response

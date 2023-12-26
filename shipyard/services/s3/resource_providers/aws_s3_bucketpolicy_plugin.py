from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class S3BucketPolicyProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::S3::BucketPolicy"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.s3.resource_providers.aws_s3_bucketpolicy import (
            S3BucketPolicyProvider,
        )

        self.factory = S3BucketPolicyProvider

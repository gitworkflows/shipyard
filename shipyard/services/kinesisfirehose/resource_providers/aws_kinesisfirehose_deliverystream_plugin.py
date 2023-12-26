from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class KinesisFirehoseDeliveryStreamProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::KinesisFirehose::DeliveryStream"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.kinesisfirehose.resource_providers.aws_kinesisfirehose_deliverystream import (
            KinesisFirehoseDeliveryStreamProvider,
        )

        self.factory = KinesisFirehoseDeliveryStreamProvider

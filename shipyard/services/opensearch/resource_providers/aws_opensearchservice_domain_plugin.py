from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class OpenSearchServiceDomainProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::OpenSearchService::Domain"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.opensearch.resource_providers.aws_opensearchservice_domain import (
            OpenSearchServiceDomainProvider,
        )

        self.factory = OpenSearchServiceDomainProvider

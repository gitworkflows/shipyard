from abc import ABC

from shipyard.aws.api.resourcegroupstaggingapi import ResourcegroupstaggingapiApi


class ResourcegroupstaggingapiProvider(ResourcegroupstaggingapiApi, ABC):
    pass

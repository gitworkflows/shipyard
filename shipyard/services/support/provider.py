from abc import ABC

from shipyard.aws.api.support import SupportApi


class SupportProvider(SupportApi, ABC):
    pass

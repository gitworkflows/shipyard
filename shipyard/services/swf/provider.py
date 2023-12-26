from abc import ABC

from shipyard.aws.api.swf import SwfApi


class SWFProvider(SwfApi, ABC):
    pass

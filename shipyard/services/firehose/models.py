from typing import Dict

from shipyard.aws.api.firehose import DeliveryStreamDescription
from shipyard.services.stores import (
    AccountRegionBundle,
    BaseStore,
    CrossRegionAttribute,
    LocalAttribute,
)
from shipyard.utils.tagging import TaggingService


class FirehoseStore(BaseStore):
    # maps delivery stream names to DeliveryStreamDescription
    delivery_streams: Dict[str, DeliveryStreamDescription] = LocalAttribute(default=dict)

    # static tagging service instance
    TAGS = CrossRegionAttribute(default=TaggingService)


firehose_stores = AccountRegionBundle("firehose", FirehoseStore)

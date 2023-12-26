import logging

from shipyard.aws.api.scheduler import SchedulerApi
from shipyard.services.plugins import ServiceLifecycleHook

LOG = logging.getLogger(__name__)


class SchedulerProvider(SchedulerApi, ServiceLifecycleHook):
    pass

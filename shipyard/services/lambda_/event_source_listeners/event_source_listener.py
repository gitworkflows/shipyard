import logging
from typing import Dict, Optional, Type

from shipyard.services.lambda_.event_source_listeners.adapters import (
    EventSourceAdapter,
    EventSourceAsfAdapter,
)
from shipyard.services.lambda_.invocation.lambda_service import LambdaService
from shipyard.utils.bootstrap import is_api_enabled
from shipyard.utils.objects import SubtypesInstanceManager

LOG = logging.getLogger(__name__)


class EventSourceListener(SubtypesInstanceManager):
    INSTANCES: Dict[str, "EventSourceListener"] = {}

    @staticmethod
    def source_type() -> Optional[str]:
        """Type discriminator - to be implemented by subclasses."""
        return None

    def start(self, invoke_adapter: Optional[EventSourceAdapter] = None):
        """Start listener in the background (for polling mode) - to be implemented by subclasses."""
        pass

    @staticmethod
    def start_listeners_for_asf(event_source_mapping: Dict, lambda_service: LambdaService):
        """limited version of start_listeners for the new provider during migration"""
        # force import EventSourceListener subclasses
        # otherwise they will not be detected by EventSourceListener.get(service_type)
        from . import (
            dynamodb_event_source_listener,  # noqa: F401
            kinesis_event_source_listener,  # noqa: F401
            sqs_event_source_listener,  # noqa: F401
        )

        source_arn = event_source_mapping.get("EventSourceArn") or ""
        parts = source_arn.split(":")
        service_type = parts[2] if len(parts) > 2 else ""
        if not service_type:
            self_managed_endpoints = event_source_mapping.get("SelfManagedEventSource", {}).get(
                "Endpoints", {}
            )
            if self_managed_endpoints.get("KAFKA_BOOTSTRAP_SERVERS"):
                service_type = "kafka"
        elif not is_api_enabled(service_type):
            LOG.info(
                "Service %s is not enabled, cannot enable event-source-mapping. Please check your 'SERVICES' configuration variable.",
                service_type,
            )
            return
        instance = EventSourceListener.get(service_type, raise_if_missing=False)
        if instance:
            instance.start(EventSourceAsfAdapter(lambda_service))

    @classmethod
    def impl_name(cls) -> str:
        return cls.source_type()

    @classmethod
    def get_base_type(cls) -> Type:
        return EventSourceListener

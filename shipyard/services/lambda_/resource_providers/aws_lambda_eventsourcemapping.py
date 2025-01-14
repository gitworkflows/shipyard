# Shipyard Resource Provider Scaffolding v2
from __future__ import annotations

from pathlib import Path
from typing import Optional, TypedDict

import shipyard.services.cloudformation.provider_utils as util
from shipyard.services.cloudformation.resource_provider import (
    OperationStatus,
    ProgressEvent,
    ResourceProvider,
    ResourceRequest,
)


class LambdaEventSourceMappingProperties(TypedDict):
    FunctionName: Optional[str]
    AmazonManagedKafkaEventSourceConfig: Optional[AmazonManagedKafkaEventSourceConfig]
    BatchSize: Optional[int]
    BisectBatchOnFunctionError: Optional[bool]
    DestinationConfig: Optional[DestinationConfig]
    DocumentDBEventSourceConfig: Optional[DocumentDBEventSourceConfig]
    Enabled: Optional[bool]
    EventSourceArn: Optional[str]
    FilterCriteria: Optional[FilterCriteria]
    FunctionResponseTypes: Optional[list[str]]
    Id: Optional[str]
    MaximumBatchingWindowInSeconds: Optional[int]
    MaximumRecordAgeInSeconds: Optional[int]
    MaximumRetryAttempts: Optional[int]
    ParallelizationFactor: Optional[int]
    Queues: Optional[list[str]]
    ScalingConfig: Optional[ScalingConfig]
    SelfManagedEventSource: Optional[SelfManagedEventSource]
    SelfManagedKafkaEventSourceConfig: Optional[SelfManagedKafkaEventSourceConfig]
    SourceAccessConfigurations: Optional[list[SourceAccessConfiguration]]
    StartingPosition: Optional[str]
    StartingPositionTimestamp: Optional[float]
    Topics: Optional[list[str]]
    TumblingWindowInSeconds: Optional[int]


class OnFailure(TypedDict):
    Destination: Optional[str]


class DestinationConfig(TypedDict):
    OnFailure: Optional[OnFailure]


class Filter(TypedDict):
    Pattern: Optional[str]


class FilterCriteria(TypedDict):
    Filters: Optional[list[Filter]]


class SourceAccessConfiguration(TypedDict):
    Type: Optional[str]
    URI: Optional[str]


class Endpoints(TypedDict):
    KafkaBootstrapServers: Optional[list[str]]


class SelfManagedEventSource(TypedDict):
    Endpoints: Optional[Endpoints]


class AmazonManagedKafkaEventSourceConfig(TypedDict):
    ConsumerGroupId: Optional[str]


class SelfManagedKafkaEventSourceConfig(TypedDict):
    ConsumerGroupId: Optional[str]


class ScalingConfig(TypedDict):
    MaximumConcurrency: Optional[int]


class DocumentDBEventSourceConfig(TypedDict):
    CollectionName: Optional[str]
    DatabaseName: Optional[str]
    FullDocument: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class LambdaEventSourceMappingProvider(ResourceProvider[LambdaEventSourceMappingProperties]):
    TYPE = "AWS::Lambda::EventSourceMapping"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[LambdaEventSourceMappingProperties],
    ) -> ProgressEvent[LambdaEventSourceMappingProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/Id

        Required properties:
          - FunctionName

        Create-only properties:
          - /properties/EventSourceArn
          - /properties/StartingPosition
          - /properties/StartingPositionTimestamp
          - /properties/SelfManagedEventSource
          - /properties/AmazonManagedKafkaEventSourceConfig
          - /properties/SelfManagedKafkaEventSourceConfig

        Read-only properties:
          - /properties/Id

        IAM permissions required:
          - lambda:CreateEventSourceMapping
          - lambda:GetEventSourceMapping

        """
        model = request.desired_state
        lambda_client = request.aws_client_factory.lambda_

        response = lambda_client.create_event_source_mapping(**model)
        model["Id"] = response["UUID"]

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[LambdaEventSourceMappingProperties],
    ) -> ProgressEvent[LambdaEventSourceMappingProperties]:
        """
        Fetch resource information

        IAM permissions required:
          - lambda:GetEventSourceMapping
        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[LambdaEventSourceMappingProperties],
    ) -> ProgressEvent[LambdaEventSourceMappingProperties]:
        """
        Delete a resource

        IAM permissions required:
          - lambda:DeleteEventSourceMapping
          - lambda:GetEventSourceMapping
        """
        model = request.desired_state
        lambda_client = request.aws_client_factory.lambda_

        lambda_client.delete_event_source_mapping(UUID=model["Id"])

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def update(
        self,
        request: ResourceRequest[LambdaEventSourceMappingProperties],
    ) -> ProgressEvent[LambdaEventSourceMappingProperties]:
        """
        Update a resource

        IAM permissions required:
          - lambda:UpdateEventSourceMapping
          - lambda:GetEventSourceMapping
        """
        raise NotImplementedError

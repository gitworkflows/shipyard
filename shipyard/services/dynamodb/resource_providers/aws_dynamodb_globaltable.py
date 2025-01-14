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


class DynamoDBGlobalTableProperties(TypedDict):
    AttributeDefinitions: Optional[list[AttributeDefinition]]
    KeySchema: Optional[list[KeySchema]]
    Replicas: Optional[list[ReplicaSpecification]]
    Arn: Optional[str]
    BillingMode: Optional[str]
    GlobalSecondaryIndexes: Optional[list[GlobalSecondaryIndex]]
    LocalSecondaryIndexes: Optional[list[LocalSecondaryIndex]]
    SSESpecification: Optional[SSESpecification]
    StreamArn: Optional[str]
    StreamSpecification: Optional[StreamSpecification]
    TableId: Optional[str]
    TableName: Optional[str]
    TimeToLiveSpecification: Optional[TimeToLiveSpecification]
    WriteProvisionedThroughputSettings: Optional[WriteProvisionedThroughputSettings]


class AttributeDefinition(TypedDict):
    AttributeName: Optional[str]
    AttributeType: Optional[str]


class KeySchema(TypedDict):
    AttributeName: Optional[str]
    KeyType: Optional[str]


class Projection(TypedDict):
    NonKeyAttributes: Optional[list[str]]
    ProjectionType: Optional[str]


class TargetTrackingScalingPolicyConfiguration(TypedDict):
    TargetValue: Optional[float]
    DisableScaleIn: Optional[bool]
    ScaleInCooldown: Optional[int]
    ScaleOutCooldown: Optional[int]


class CapacityAutoScalingSettings(TypedDict):
    MaxCapacity: Optional[int]
    MinCapacity: Optional[int]
    TargetTrackingScalingPolicyConfiguration: Optional[TargetTrackingScalingPolicyConfiguration]
    SeedCapacity: Optional[int]


class WriteProvisionedThroughputSettings(TypedDict):
    WriteCapacityAutoScalingSettings: Optional[CapacityAutoScalingSettings]


class GlobalSecondaryIndex(TypedDict):
    IndexName: Optional[str]
    KeySchema: Optional[list[KeySchema]]
    Projection: Optional[Projection]
    WriteProvisionedThroughputSettings: Optional[WriteProvisionedThroughputSettings]


class LocalSecondaryIndex(TypedDict):
    IndexName: Optional[str]
    KeySchema: Optional[list[KeySchema]]
    Projection: Optional[Projection]


class ContributorInsightsSpecification(TypedDict):
    Enabled: Optional[bool]


class ReadProvisionedThroughputSettings(TypedDict):
    ReadCapacityAutoScalingSettings: Optional[CapacityAutoScalingSettings]
    ReadCapacityUnits: Optional[int]


class ReplicaGlobalSecondaryIndexSpecification(TypedDict):
    IndexName: Optional[str]
    ContributorInsightsSpecification: Optional[ContributorInsightsSpecification]
    ReadProvisionedThroughputSettings: Optional[ReadProvisionedThroughputSettings]


class PointInTimeRecoverySpecification(TypedDict):
    PointInTimeRecoveryEnabled: Optional[bool]


class ReplicaSSESpecification(TypedDict):
    KMSMasterKeyId: Optional[str]


class Tag(TypedDict):
    Key: Optional[str]
    Value: Optional[str]


class KinesisStreamSpecification(TypedDict):
    StreamArn: Optional[str]


class ReplicaSpecification(TypedDict):
    Region: Optional[str]
    ContributorInsightsSpecification: Optional[ContributorInsightsSpecification]
    DeletionProtectionEnabled: Optional[bool]
    GlobalSecondaryIndexes: Optional[list[ReplicaGlobalSecondaryIndexSpecification]]
    KinesisStreamSpecification: Optional[KinesisStreamSpecification]
    PointInTimeRecoverySpecification: Optional[PointInTimeRecoverySpecification]
    ReadProvisionedThroughputSettings: Optional[ReadProvisionedThroughputSettings]
    SSESpecification: Optional[ReplicaSSESpecification]
    TableClass: Optional[str]
    Tags: Optional[list[Tag]]


class SSESpecification(TypedDict):
    SSEEnabled: Optional[bool]
    SSEType: Optional[str]


class StreamSpecification(TypedDict):
    StreamViewType: Optional[str]


class TimeToLiveSpecification(TypedDict):
    Enabled: Optional[bool]
    AttributeName: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class DynamoDBGlobalTableProvider(ResourceProvider[DynamoDBGlobalTableProperties]):
    TYPE = "AWS::DynamoDB::GlobalTable"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[DynamoDBGlobalTableProperties],
    ) -> ProgressEvent[DynamoDBGlobalTableProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/TableName

        Required properties:
          - KeySchema
          - AttributeDefinitions
          - Replicas

        Create-only properties:
          - /properties/LocalSecondaryIndexes
          - /properties/TableName
          - /properties/KeySchema

        Read-only properties:
          - /properties/Arn
          - /properties/StreamArn
          - /properties/TableId

        IAM permissions required:
          - dynamodb:CreateTable
          - dynamodb:CreateTableReplica
          - dynamodb:Describe*
          - dynamodb:UpdateTimeToLive
          - dynamodb:UpdateContributorInsights
          - dynamodb:UpdateContinuousBackups
          - dynamodb:ListTagsOfResource
          - dynamodb:Query
          - dynamodb:Scan
          - dynamodb:UpdateItem
          - dynamodb:PutItem
          - dynamodb:GetItem
          - dynamodb:DeleteItem
          - dynamodb:BatchWriteItem
          - dynamodb:TagResource
          - dynamodb:EnableKinesisStreamingDestination
          - dynamodb:DisableKinesisStreamingDestination
          - dynamodb:DescribeKinesisStreamingDestination
          - dynamodb:DescribeTableReplicaAutoScaling
          - dynamodb:UpdateTableReplicaAutoScaling
          - dynamodb:TagResource
          - application-autoscaling:DeleteScalingPolicy
          - application-autoscaling:DeleteScheduledAction
          - application-autoscaling:DeregisterScalableTarget
          - application-autoscaling:Describe*
          - application-autoscaling:PutScalingPolicy
          - application-autoscaling:PutScheduledAction
          - application-autoscaling:RegisterScalableTarget
          - kinesis:ListStreams
          - kinesis:DescribeStream
          - kinesis:PutRecords
          - kms:CreateGrant
          - kms:Describe*
          - kms:Get*
          - kms:List*
          - kms:RevokeGrant
          - cloudwatch:PutMetricData

        """
        model = request.desired_state

        if not request.custom_context.get(REPEATED_INVOCATION):
            request.custom_context[REPEATED_INVOCATION] = True

            if not model.get("TableName"):
                model["TableName"] = util.generate_default_name(
                    stack_name=request.stack_name, logical_resource_id=request.logical_resource_id
                )

            create_params = util.select_attributes(
                model,
                [
                    "AttributeDefinitions",
                    "BillingMode",
                    "GlobalSecondaryIndexes",
                    "KeySchema",
                    "LocalSecondaryIndexes",
                    "Replicas",
                    "SSESpecification",
                    "StreamSpecification",
                    "TableName",
                    "TimeToLiveSpecification",
                    "WriteProvisionedThroughputSettings",
                ],
            )

            replicas = create_params.pop("Replicas", [])

            creation_response = request.aws_client_factory.dynamodb.create_table(**create_params)
            model["Arn"] = creation_response["TableDescription"]["TableArn"]
            model["TableId"] = creation_response["TableDescription"]["TableId"]

            if creation_response["TableDescription"].get("LatestStreamArn"):
                model["StreamArn"] = creation_response["TableDescription"]["LatestStreamArn"]

            replicas_to_create = []
            for replica in replicas:
                create = {
                    "RegionName": replica.get("Region"),
                    "KMSMasterKeyId": replica.get("KMSMasterKeyId"),
                    "ProvisionedThroughputOverride": replica.get("ProvisionedThroughputOverride"),
                    "GlobalSecondaryIndexes": replica.get("GlobalSecondaryIndexes"),
                    "TableClassOverride": replica.get("TableClassOverride"),
                }

                create = {k: v for k, v in create.items() if v is not None}

                replicas_to_create.append({"Create": create})

                request.aws_client_factory.dynamodb.update_table(
                    ReplicaUpdates=replicas_to_create, TableName=model["TableName"]
                )

            return ProgressEvent(
                status=OperationStatus.IN_PROGRESS,
                resource_model=model,
                custom_context=request.custom_context,
            )

        status = request.aws_client_factory.dynamodb.describe_table(TableName=model["TableName"])[
            "Table"
        ]["TableStatus"]
        if status == "ACTIVE":
            return ProgressEvent(
                status=OperationStatus.SUCCESS,
                resource_model=model,
                custom_context=request.custom_context,
            )

        elif status == "CREATING":
            return ProgressEvent(
                status=OperationStatus.IN_PROGRESS,
                resource_model=model,
                custom_context=request.custom_context,
            )
        else:
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resource_model=model,
                custom_context=request.custom_context,
                message=f"Table creation failed with status {status}",
            )

    def read(
        self,
        request: ResourceRequest[DynamoDBGlobalTableProperties],
    ) -> ProgressEvent[DynamoDBGlobalTableProperties]:
        """
        Fetch resource information

        IAM permissions required:
          - dynamodb:Describe*
          - application-autoscaling:Describe*
          - cloudwatch:PutMetricData
        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[DynamoDBGlobalTableProperties],
    ) -> ProgressEvent[DynamoDBGlobalTableProperties]:
        """
        Delete a resource

        IAM permissions required:
          - dynamodb:Describe*
          - application-autoscaling:DeleteScalingPolicy
          - application-autoscaling:DeleteScheduledAction
          - application-autoscaling:DeregisterScalableTarget
          - application-autoscaling:Describe*
          - application-autoscaling:PutScalingPolicy
          - application-autoscaling:PutScheduledAction
          - application-autoscaling:RegisterScalableTarget
        """

        model = request.desired_state
        if not request.custom_context.get(REPEATED_INVOCATION):
            request.custom_context[REPEATED_INVOCATION] = True
            request.aws_client_factory.dynamodb.delete_table(TableName=model["TableName"])

            return ProgressEvent(
                status=OperationStatus.IN_PROGRESS,
                resource_model=model,
                custom_context=request.custom_context,
            )

        try:
            request.aws_client_factory.dynamodb.describe_table(TableName=model["TableName"])
            return ProgressEvent(
                status=OperationStatus.IN_PROGRESS,
                resource_model=model,
                custom_context=request.custom_context,
            )
        except Exception as ex:
            if "ResourceNotFoundException" in str(ex):
                return ProgressEvent(
                    status=OperationStatus.SUCCESS,
                    resource_model=model,
                    custom_context=request.custom_context,
                )

            return ProgressEvent(
                status=OperationStatus.FAILED,
                resource_model=model,
                custom_context=request.custom_context,
                message=str(ex),
            )

    def update(
        self,
        request: ResourceRequest[DynamoDBGlobalTableProperties],
    ) -> ProgressEvent[DynamoDBGlobalTableProperties]:
        """
        Update a resource

        IAM permissions required:
          - dynamodb:Describe*
          - dynamodb:CreateTableReplica
          - dynamodb:UpdateTable
          - dynamodb:UpdateTimeToLive
          - dynamodb:UpdateContinuousBackups
          - dynamodb:UpdateContributorInsights
          - dynamodb:ListTagsOfResource
          - dynamodb:Query
          - dynamodb:Scan
          - dynamodb:UpdateItem
          - dynamodb:PutItem
          - dynamodb:GetItem
          - dynamodb:DeleteItem
          - dynamodb:BatchWriteItem
          - dynamodb:DeleteTable
          - dynamodb:DeleteTableReplica
          - dynamodb:UpdateItem
          - dynamodb:TagResource
          - dynamodb:UntagResource
          - dynamodb:EnableKinesisStreamingDestination
          - dynamodb:DisableKinesisStreamingDestination
          - dynamodb:DescribeKinesisStreamingDestination
          - dynamodb:DescribeTableReplicaAutoScaling
          - dynamodb:UpdateTableReplicaAutoScaling
          - application-autoscaling:DeleteScalingPolicy
          - application-autoscaling:DeleteScheduledAction
          - application-autoscaling:DeregisterScalableTarget
          - application-autoscaling:Describe*
          - application-autoscaling:PutScalingPolicy
          - application-autoscaling:PutScheduledAction
          - application-autoscaling:RegisterScalableTarget
          - kinesis:ListStreams
          - kinesis:DescribeStream
          - kinesis:PutRecords
          - kms:CreateGrant
          - kms:Describe*
          - kms:Get*
          - kms:List*
          - kms:RevokeGrant
          - cloudwatch:PutMetricData
        """
        raise NotImplementedError

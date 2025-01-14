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


class LogsLogGroupProperties(TypedDict):
    Arn: Optional[str]
    DataProtectionPolicy: Optional[dict]
    KmsKeyId: Optional[str]
    LogGroupName: Optional[str]
    RetentionInDays: Optional[int]
    Tags: Optional[list[Tag]]


class Tag(TypedDict):
    Key: Optional[str]
    Value: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class LogsLogGroupProvider(ResourceProvider[LogsLogGroupProperties]):
    TYPE = "AWS::Logs::LogGroup"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[LogsLogGroupProperties],
    ) -> ProgressEvent[LogsLogGroupProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/LogGroupName

        Create-only properties:
          - /properties/LogGroupName

        Read-only properties:
          - /properties/Arn

        IAM permissions required:
          - logs:DescribeLogGroups
          - logs:CreateLogGroup
          - logs:PutRetentionPolicy
          - logs:TagLogGroup
          - logs:GetDataProtectionPolicy
          - logs:PutDataProtectionPolicy
          - logs:CreateLogDelivery
          - s3:REST.PUT.OBJECT
          - firehose:TagDeliveryStream
          - logs:PutResourcePolicy
          - logs:DescribeResourcePolicies

        """
        model = request.desired_state
        logs = request.aws_client_factory.logs

        if not model.get("LogGroupName"):
            model["LogGroupName"] = util.generate_default_name(
                stack_name=request.stack_name, logical_resource_id=request.logical_resource_id
            )

        logs.create_log_group(logGroupName=model["LogGroupName"])

        describe_result = logs.describe_log_groups(logGroupNamePrefix=model["LogGroupName"])
        model["Arn"] = describe_result["logGroups"][0]["arn"]

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[LogsLogGroupProperties],
    ) -> ProgressEvent[LogsLogGroupProperties]:
        """
        Fetch resource information

        IAM permissions required:
          - logs:DescribeLogGroups
          - logs:ListTagsLogGroup
          - logs:GetDataProtectionPolicy
        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[LogsLogGroupProperties],
    ) -> ProgressEvent[LogsLogGroupProperties]:
        """
        Delete a resource

        IAM permissions required:
          - logs:DescribeLogGroups
          - logs:DeleteLogGroup
          - logs:DeleteDataProtectionPolicy
        """
        model = request.desired_state
        logs = request.aws_client_factory.logs

        logs.delete_log_group(logGroupName=model["LogGroupName"])

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def update(
        self,
        request: ResourceRequest[LogsLogGroupProperties],
    ) -> ProgressEvent[LogsLogGroupProperties]:
        """
        Update a resource

        IAM permissions required:
          - logs:DescribeLogGroups
          - logs:AssociateKmsKey
          - logs:DisassociateKmsKey
          - logs:PutRetentionPolicy
          - logs:DeleteRetentionPolicy
          - logs:TagLogGroup
          - logs:UntagLogGroup
          - logs:GetDataProtectionPolicy
          - logs:PutDataProtectionPolicy
          - logs:CreateLogDelivery
          - s3:REST.PUT.OBJECT
          - firehose:TagDeliveryStream
        """
        raise NotImplementedError

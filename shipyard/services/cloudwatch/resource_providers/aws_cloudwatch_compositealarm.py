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
from shipyard.utils.strings import str_to_bool


class CloudWatchCompositeAlarmProperties(TypedDict):
    AlarmRule: Optional[str]
    ActionsEnabled: Optional[bool]
    ActionsSuppressor: Optional[str]
    ActionsSuppressorExtensionPeriod: Optional[int]
    ActionsSuppressorWaitPeriod: Optional[int]
    AlarmActions: Optional[list[str]]
    AlarmDescription: Optional[str]
    AlarmName: Optional[str]
    Arn: Optional[str]
    InsufficientDataActions: Optional[list[str]]
    OKActions: Optional[list[str]]


REPEATED_INVOCATION = "repeated_invocation"


class CloudWatchCompositeAlarmProvider(ResourceProvider[CloudWatchCompositeAlarmProperties]):
    TYPE = "AWS::CloudWatch::CompositeAlarm"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[CloudWatchCompositeAlarmProperties],
    ) -> ProgressEvent[CloudWatchCompositeAlarmProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/AlarmName

        Required properties:
          - AlarmRule

        Create-only properties:
          - /properties/AlarmName

        Read-only properties:
          - /properties/Arn

        IAM permissions required:
          - cloudwatch:DescribeAlarms
          - cloudwatch:PutCompositeAlarm

        """
        model = request.desired_state
        cloud_watch = request.aws_client_factory.cloudwatch

        params = util.select_attributes(
            model,
            [
                "AlarmName",
                "AlarmRule",
                "ActionsEnabled",
                "ActionsSuppressor",
                "ActionsSuppressorWaitPeriod",
                "ActionsSuppressorExtensionPeriod",
                "AlarmActions",
                "AlarmDescription",
                "InsufficientDataActions",
                "OKActions",
            ],
        )
        if not params.get("AlarmName"):
            model["AlarmName"] = util.generate_default_name(
                stack_name=request.stack_name, logical_resource_id=request.logical_resource_id
            )
            params["AlarmName"] = model["AlarmName"]

        if "ActionsEnabled" in params:
            params["ActionsEnabled"] = str_to_bool(params["ActionsEnabled"])

        create_params = util.select_attributes(
            model,
            [
                "AlarmName",
                "AlarmRule",
                "ActionsEnabled",
                "ActionsSuppressor",
                "ActionsSuppressorExtensionPeriod",
                "ActionsSuppressorWaitPeriod",
                "AlarmActions",
                "AlarmDescription",
                "InsufficientDataActions",
                "OKActions",
            ],
        )

        cloud_watch.put_composite_alarm(**create_params)
        alarms = cloud_watch.describe_alarms(
            AlarmNames=[model["AlarmName"]], AlarmTypes=["CompositeAlarm"]
        )["CompositeAlarms"]

        if not alarms:
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resource_model=model,
                message="Composite Alarm not found",
            )
        model["Arn"] = alarms[0]["AlarmArn"]

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[CloudWatchCompositeAlarmProperties],
    ) -> ProgressEvent[CloudWatchCompositeAlarmProperties]:
        """
        Fetch resource information

        IAM permissions required:
          - cloudwatch:DescribeAlarms
        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[CloudWatchCompositeAlarmProperties],
    ) -> ProgressEvent[CloudWatchCompositeAlarmProperties]:
        """
        Delete a resource

        IAM permissions required:
          - cloudwatch:DescribeAlarms
          - cloudwatch:DeleteAlarms
        """
        model = request.desired_state
        cloud_watch = request.aws_client_factory.cloudwatch
        cloud_watch.delete_alarms(AlarmNames=[model["AlarmName"]])

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def update(
        self,
        request: ResourceRequest[CloudWatchCompositeAlarmProperties],
    ) -> ProgressEvent[CloudWatchCompositeAlarmProperties]:
        """
        Update a resource

        IAM permissions required:
          - cloudwatch:DescribeAlarms
          - cloudwatch:PutCompositeAlarm
        """
        raise NotImplementedError

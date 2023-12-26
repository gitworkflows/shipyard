# Shipyard Resource Provider Scaffolding v2
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, TypedDict

import shipyard.services.cloudformation.provider_utils as util
from shipyard.services.cloudformation.resource_provider import (
    OperationStatus,
    ProgressEvent,
    ResourceProvider,
    ResourceRequest,
)


class KMSKeyProperties(TypedDict):
    KeyPolicy: Optional[dict | str]
    Arn: Optional[str]
    Description: Optional[str]
    EnableKeyRotation: Optional[bool]
    Enabled: Optional[bool]
    KeyId: Optional[str]
    KeySpec: Optional[str]
    KeyUsage: Optional[str]
    MultiRegion: Optional[bool]
    PendingWindowInDays: Optional[int]
    Tags: Optional[list[Tag]]


class Tag(TypedDict):
    Key: Optional[str]
    Value: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class KMSKeyProvider(ResourceProvider[KMSKeyProperties]):
    TYPE = "AWS::KMS::Key"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[KMSKeyProperties],
    ) -> ProgressEvent[KMSKeyProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/KeyId

        Required properties:
          - KeyPolicy



        Read-only properties:
          - /properties/Arn
          - /properties/KeyId

        IAM permissions required:
          - kms:CreateKey
          - kms:EnableKeyRotation
          - kms:DisableKey
          - kms:TagResource

        """
        model = request.desired_state
        kms = request.aws_client_factory.kms

        params = util.select_attributes(model, ["Description", "KeySpec", "KeyUsage"])

        if model.get("KeyPolicy"):
            params["Policy"] = json.dumps(model["KeyPolicy"])

        if model.get("Tags"):
            params["Tags"] = [
                {"TagKey": tag["Key"], "TagValue": tag["Value"]} for tag in model.get("Tags", [])
            ]
        response = kms.create_key(**params)
        model["KeyId"] = response["KeyMetadata"]["KeyId"]
        model["Arn"] = response["KeyMetadata"]["Arn"]

        # key is created but some fields map to separate api calls
        if model.get("EnableKeyRotation", False):
            kms.enable_key_rotation(KeyId=model["KeyId"])
        else:
            kms.disable_key_rotation(KeyId=model["KeyId"])

        if model.get("Enabled", True):
            kms.enable_key(KeyId=model["KeyId"])
        else:
            kms.disable_key(KeyId=model["KeyId"])

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[KMSKeyProperties],
    ) -> ProgressEvent[KMSKeyProperties]:
        """
        Fetch resource information

        IAM permissions required:
          - kms:DescribeKey
          - kms:GetKeyPolicy
          - kms:GetKeyRotationStatus
          - kms:ListResourceTags
        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[KMSKeyProperties],
    ) -> ProgressEvent[KMSKeyProperties]:
        """
        Delete a resource

        IAM permissions required:
          - kms:DescribeKey
          - kms:ScheduleKeyDeletion
        """
        model = request.desired_state
        kms = request.aws_client_factory.kms

        kms.schedule_key_deletion(KeyId=model["KeyId"])

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def update(
        self,
        request: ResourceRequest[KMSKeyProperties],
    ) -> ProgressEvent[KMSKeyProperties]:
        """
        Update a resource

        IAM permissions required:
          - kms:DescribeKey
          - kms:DisableKey
          - kms:DisableKeyRotation
          - kms:EnableKey
          - kms:EnableKeyRotation
          - kms:PutKeyPolicy
          - kms:TagResource
          - kms:UntagResource
          - kms:UpdateKeyDescription
        """
        raise NotImplementedError
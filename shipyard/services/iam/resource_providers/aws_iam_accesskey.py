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


class IAMAccessKeyProperties(TypedDict):
    UserName: Optional[str]
    Id: Optional[str]
    SecretAccessKey: Optional[str]
    Serial: Optional[int]
    Status: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class IAMAccessKeyProvider(ResourceProvider[IAMAccessKeyProperties]):
    TYPE = "AWS::IAM::AccessKey"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[IAMAccessKeyProperties],
    ) -> ProgressEvent[IAMAccessKeyProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/Id

        Required properties:
          - UserName

        Create-only properties:
          - /properties/UserName
          - /properties/Serial

        Read-only properties:
          - /properties/SecretAccessKey
          - /properties/Id

        """
        # TODO: what alues can model['Serial'] take on initial create?
        model = request.desired_state
        iam_client = request.aws_client_factory.iam

        access_key = iam_client.create_access_key(UserName=model["UserName"])
        model["SecretAccessKey"] = access_key["AccessKey"]["SecretAccessKey"]
        model["Id"] = access_key["AccessKey"]["AccessKeyId"]

        if model.get("Status") == "Inactive":
            # can be "Active" or "Inactive"
            # by default the created access key has Status "Active", but if user set Inactive this needs to be adjusted
            iam_client.update_access_key(
                AccessKeyId=model["Id"], UserName=model["UserName"], Status=model["Status"]
            )

        return ProgressEvent(status=OperationStatus.SUCCESS, resource_model=model)

    def read(
        self,
        request: ResourceRequest[IAMAccessKeyProperties],
    ) -> ProgressEvent[IAMAccessKeyProperties]:
        """
        Fetch resource information
        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[IAMAccessKeyProperties],
    ) -> ProgressEvent[IAMAccessKeyProperties]:
        """
        Delete a resource
        """
        iam_client = request.aws_client_factory.iam
        model = request.previous_state
        iam_client.delete_access_key(AccessKeyId=model["Id"], UserName=model["UserName"])
        return ProgressEvent(status=OperationStatus.SUCCESS, resource_model={})

    def update(
        self,
        request: ResourceRequest[IAMAccessKeyProperties],
    ) -> ProgressEvent[IAMAccessKeyProperties]:
        """
        Update a resource
        """
        iam_client = request.aws_client_factory.iam

        # FIXME: replacement should be handled in engine before here
        user_name_changed = request.desired_state["UserName"] != request.previous_state["UserName"]
        serial_changed = request.desired_state["Serial"] != request.previous_state["Serial"]
        if user_name_changed or serial_changed:
            # recreate the key
            self.delete(request)
            create_event = self.create(request)
            return create_event

        iam_client.update_access_key(
            AccessKeyId=request.previous_state["Id"],
            UserName=request.previous_state["UserName"],
            Status=request.desired_state["Status"],
        )
        old_model = request.previous_state
        old_model["Status"] = request.desired_state["Status"]
        return ProgressEvent(status=OperationStatus.SUCCESS, resource_model=old_model)

# Shipyard Resource Provider Scaffolding v1
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


class IAMUserProperties(TypedDict):
    Arn: Optional[str]
    Groups: Optional[list[str]]
    Id: Optional[str]
    LoginProfile: Optional[LoginProfile]
    ManagedPolicyArns: Optional[list[str]]
    Path: Optional[str]
    PermissionsBoundary: Optional[str]
    Policies: Optional[list[Policy]]
    Tags: Optional[list[Tag]]
    UserName: Optional[str]


class Policy(TypedDict):
    PolicyDocument: Optional[dict]
    PolicyName: Optional[str]


class LoginProfile(TypedDict):
    Password: Optional[str]
    PasswordResetRequired: Optional[bool]


class Tag(TypedDict):
    Key: Optional[str]
    Value: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class IAMUserProvider(ResourceProvider[IAMUserProperties]):
    TYPE = "AWS::IAM::User"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[IAMUserProperties],
    ) -> ProgressEvent[IAMUserProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/Id

        Create-only properties:
          - /properties/UserName

        Read-only properties:
          - /properties/Id
          - /properties/Arn
        """
        model = request.desired_state
        iam_client = request.aws_client_factory.iam
        # TODO: validations
        # TODO: idempotency

        if not request.custom_context.get(REPEATED_INVOCATION):
            # this is the first time this callback is invoked

            # Set defaults
            if not model.get("UserName"):
                model["UserName"] = util.generate_default_name(
                    request.stack_name, request.logical_resource_id
                )

            # actually create the resource
            # note: technically we could make this synchronous, but for the sake of this being an example it is intentionally "asynchronous" and returns IN_PROGRESS

            # this example uses a helper utility, check out the module for more helpful utilities and add your own!
            iam_client.create_user(
                **util.select_attributes(model, ["UserName", "Path", "PermissionsBoundary", "Tags"])
            )

            # alternatively you can also just do:
            # iam_client.create_user(
            #     UserName=model["UserName"],
            #     Path=model["Path"],
            #     PermissionsBoundary=model["PermissionsBoundary"],
            #     Tags=model["Tags"],
            # )

            # this kind of logic below was previously done in either a result_handler or a custom "_post_create" function
            for group in model.get("Groups", []):
                iam_client.add_user_to_group(GroupName=group, UserName=model["UserName"])

            for policy_arn in model.get("ManagedPolicyArns", []):
                iam_client.attach_user_policy(UserName=model["UserName"], PolicyArn=policy_arn)

            request.custom_context[REPEATED_INVOCATION] = True
            return ProgressEvent(
                status=OperationStatus.IN_PROGRESS,
                resource_model=model,
                custom_context=request.custom_context,
            )

        get_response = iam_client.get_user(UserName=model["UserName"])
        model["Id"] = get_response["User"]["UserName"]  # this is the ref / physical resource id
        model["Arn"] = get_response["User"]["Arn"]

        return ProgressEvent(status=OperationStatus.SUCCESS, resource_model=model)

    def read(
        self,
        request: ResourceRequest[IAMUserProperties],
    ) -> ProgressEvent[IAMUserProperties]:
        """
        Fetch resource information
        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[IAMUserProperties],
    ) -> ProgressEvent[IAMUserProperties]:
        """
        Delete a resource
        """
        iam_client = request.aws_client_factory.iam
        iam_client.delete_user(UserName=request.desired_state["Id"])
        return ProgressEvent(status=OperationStatus.SUCCESS, resource_model=None)

    def update(
        self,
        request: ResourceRequest[IAMUserProperties],
    ) -> ProgressEvent[IAMUserProperties]:
        """
        Update a resource
        """
        # return ProgressEvent(OperationStatus.SUCCESS, request.desired_state)
        raise NotImplementedError
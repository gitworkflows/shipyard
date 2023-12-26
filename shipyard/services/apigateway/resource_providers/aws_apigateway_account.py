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


class ApiGatewayAccountProperties(TypedDict):
    CloudWatchRoleArn: Optional[str]
    Id: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class ApiGatewayAccountProvider(ResourceProvider[ApiGatewayAccountProperties]):
    TYPE = "AWS::ApiGateway::Account"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[ApiGatewayAccountProperties],
    ) -> ProgressEvent[ApiGatewayAccountProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/Id





        Read-only properties:
          - /properties/Id

        IAM permissions required:
          - apigateway:PATCH
          - iam:GetRole
          - iam:PassRole

        """
        model = request.desired_state
        apigw = request.aws_client_factory.apigateway

        role_arn = model["CloudWatchRoleArn"]
        apigw.update_account(
            patchOperations=[{"op": "replace", "path": "/cloudwatchRoleArn", "value": role_arn}]
        )

        model["Id"] = util.generate_default_name(
            stack_name=request.stack_name, logical_resource_id=request.logical_resource_id
        )
        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[ApiGatewayAccountProperties],
    ) -> ProgressEvent[ApiGatewayAccountProperties]:
        """
        Fetch resource information

        IAM permissions required:
          - apigateway:GET
        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[ApiGatewayAccountProperties],
    ) -> ProgressEvent[ApiGatewayAccountProperties]:
        """
        Delete a resource


        """
        model = request.desired_state

        # note: deletion of accounts is currently a no-op
        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def update(
        self,
        request: ResourceRequest[ApiGatewayAccountProperties],
    ) -> ProgressEvent[ApiGatewayAccountProperties]:
        """
        Update a resource

        IAM permissions required:
          - apigateway:PATCH
          - iam:GetRole
          - iam:PassRole
        """
        raise NotImplementedError

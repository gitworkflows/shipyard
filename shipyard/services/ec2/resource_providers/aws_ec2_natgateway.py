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


class EC2NatGatewayProperties(TypedDict):
    SubnetId: Optional[str]
    AllocationId: Optional[str]
    ConnectivityType: Optional[str]
    MaxDrainDurationSeconds: Optional[int]
    NatGatewayId: Optional[str]
    PrivateIpAddress: Optional[str]
    SecondaryAllocationIds: Optional[list[str]]
    SecondaryPrivateIpAddressCount: Optional[int]
    SecondaryPrivateIpAddresses: Optional[list[str]]
    Tags: Optional[list[Tag]]


class Tag(TypedDict):
    Key: Optional[str]
    Value: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class EC2NatGatewayProvider(ResourceProvider[EC2NatGatewayProperties]):
    TYPE = "AWS::EC2::NatGateway"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[EC2NatGatewayProperties],
    ) -> ProgressEvent[EC2NatGatewayProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/NatGatewayId

        Required properties:
          - SubnetId

        Create-only properties:
          - /properties/SubnetId
          - /properties/ConnectivityType
          - /properties/AllocationId
          - /properties/PrivateIpAddress

        Read-only properties:
          - /properties/NatGatewayId

        IAM permissions required:
          - ec2:CreateNatGateway
          - ec2:DescribeNatGateways
          - ec2:CreateTags

        """
        model = request.desired_state
        ec2 = request.aws_client_factory.ec2

        # TODO: validations
        # TODO add tests for this resource at the moment, it's not covered

        if not request.custom_context.get(REPEATED_INVOCATION):
            # this is the first time this callback is invoked
            # TODO: defaults
            # TODO: idempotency
            params = util.select_attributes(
                model,
                ["SubnetId", "AllocationId"],
            )

            if model.get("Tags"):
                tags = [{"ResourceType": "natgateway", "Tags": model.get("Tags")}]
                params["TagSpecifications"] = tags

            response = ec2.create_nat_gateway(
                SubnetId=model["SubnetId"], AllocationId=model["AllocationId"]
            )
            model["NatGatewayId"] = response["NatGateway"]["NatGatewayId"]
            request.custom_context[REPEATED_INVOCATION] = True
            return ProgressEvent(
                status=OperationStatus.IN_PROGRESS,
                resource_model=model,
                custom_context=request.custom_context,
            )
        response = ec2.describe_nat_gateways(NatGatewayIds=[model["NatGatewayId"]])
        if response["NatGateways"][0]["State"] == "pending":
            return ProgressEvent(
                status=OperationStatus.IN_PROGRESS,
                resource_model=model,
                custom_context=request.custom_context,
            )
        # TODO add handling for failed events
        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[EC2NatGatewayProperties],
    ) -> ProgressEvent[EC2NatGatewayProperties]:
        """
        Fetch resource information

        IAM permissions required:
          - ec2:DescribeNatGateways
        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[EC2NatGatewayProperties],
    ) -> ProgressEvent[EC2NatGatewayProperties]:
        """
        Delete a resource

        IAM permissions required:
          - ec2:DeleteNatGateway
          - ec2:DescribeNatGateways
        """
        model = request.desired_state
        ec2 = request.aws_client_factory.ec2

        if not request.custom_context.get(REPEATED_INVOCATION):
            request.custom_context[REPEATED_INVOCATION] = True
            ec2.delete_nat_gateway(NatGatewayId=model["NatGatewayId"])

            return ProgressEvent(
                status=OperationStatus.IN_PROGRESS,
                resource_model=model,
                custom_context=request.custom_context,
            )

        is_deleting = False
        try:
            response = ec2.describe_nat_gateways(NatGatewayIds=[model["NatGatewayId"]])
            is_deleting = response["NatGateways"][0]["State"] == "deleting"
        except ec2.exceptions.ClientError:
            pass

        if is_deleting:
            return ProgressEvent(
                status=OperationStatus.IN_PROGRESS,
                resource_model=model,
                custom_context=request.custom_context,
            )
        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def update(
        self,
        request: ResourceRequest[EC2NatGatewayProperties],
    ) -> ProgressEvent[EC2NatGatewayProperties]:
        """
        Update a resource

        IAM permissions required:
          - ec2:DescribeNatGateways
          - ec2:CreateTags
          - ec2:DeleteTags
          - ec2:AssociateNatGatewayAddress
          - ec2:DisassociateNatGatewayAddress
          - ec2:AssignPrivateNatGatewayAddress
          - ec2:UnassignPrivateNatGatewayAddress
        """
        raise NotImplementedError
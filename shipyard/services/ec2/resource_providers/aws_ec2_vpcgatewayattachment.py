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


class EC2VPCGatewayAttachmentProperties(TypedDict):
    VpcId: Optional[str]
    Id: Optional[str]
    InternetGatewayId: Optional[str]
    VpnGatewayId: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class EC2VPCGatewayAttachmentProvider(ResourceProvider[EC2VPCGatewayAttachmentProperties]):
    TYPE = "AWS::EC2::VPCGatewayAttachment"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[EC2VPCGatewayAttachmentProperties],
    ) -> ProgressEvent[EC2VPCGatewayAttachmentProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/Id

        Required properties:
          - VpcId



        Read-only properties:
          - /properties/Id



        """
        model = request.desired_state
        ec2 = request.aws_client_factory.ec2
        # TODO: validations
        if model.get("InternetGatewayId"):
            ec2.attach_internet_gateway(
                InternetGatewayId=model["InternetGatewayId"], VpcId=model["VpcId"]
            )
        else:
            ec2.attach_vpn_gateway(VpnGatewayId=model["VpnGatewayId"], VpcId=model["VpcId"])

        # TODO: idempotency
        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[EC2VPCGatewayAttachmentProperties],
    ) -> ProgressEvent[EC2VPCGatewayAttachmentProperties]:
        """
        Fetch resource information


        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[EC2VPCGatewayAttachmentProperties],
    ) -> ProgressEvent[EC2VPCGatewayAttachmentProperties]:
        """
        Delete a resource


        """
        model = request.desired_state
        ec2 = request.aws_client_factory.ec2
        # TODO: validations
        try:
            if model.get("InternetGatewayId"):
                ec2.detach_internet_gateway(
                    InternetGatewayId=model["InternetGatewayId"], VpcId=model["VpcId"]
                )
            else:
                ec2.detach_vpn_gateway(VpnGatewayId=model["VpnGatewayId"], VpcId=model["VpcId"])
        except ec2.exceptions.ClientError:
            pass

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def update(
        self,
        request: ResourceRequest[EC2VPCGatewayAttachmentProperties],
    ) -> ProgressEvent[EC2VPCGatewayAttachmentProperties]:
        """
        Update a resource


        """
        raise NotImplementedError

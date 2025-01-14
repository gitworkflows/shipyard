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


class EC2TransitGatewayAttachmentProperties(TypedDict):
    SubnetIds: Optional[list[str]]
    TransitGatewayId: Optional[str]
    VpcId: Optional[str]
    Id: Optional[str]
    Options: Optional[dict]
    Tags: Optional[list[Tag]]


class Tag(TypedDict):
    Key: Optional[str]
    Value: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class EC2TransitGatewayAttachmentProvider(ResourceProvider[EC2TransitGatewayAttachmentProperties]):
    TYPE = "AWS::EC2::TransitGatewayAttachment"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[EC2TransitGatewayAttachmentProperties],
    ) -> ProgressEvent[EC2TransitGatewayAttachmentProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/Id

        Required properties:
          - VpcId
          - SubnetIds
          - TransitGatewayId

        Create-only properties:
          - /properties/TransitGatewayId
          - /properties/VpcId

        Read-only properties:
          - /properties/Id

        IAM permissions required:
          - ec2:CreateTransitGatewayVpcAttachment
          - ec2:CreateTags

        """
        model = request.desired_state
        create_params = util.select_attributes(
            model, ["SubnetIds", "TransitGatewayId", "VpcId", "Options"]
        )

        if model.get("Tags", []):
            create_params["TagSpecifications"] = [
                {"ResourceType": "transit-gateway-attachment", "Tags": model["Tags"]}
            ]

        result = request.aws_client_factory.ec2.create_transit_gateway_vpc_attachment(
            **create_params
        )
        model["Id"] = result["TransitGatewayVpcAttachment"]["TransitGatewayAttachmentId"]

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
        )

    def read(
        self,
        request: ResourceRequest[EC2TransitGatewayAttachmentProperties],
    ) -> ProgressEvent[EC2TransitGatewayAttachmentProperties]:
        """
        Fetch resource information

        IAM permissions required:
          - ec2:DescribeTransitGatewayAttachments
          - ec2:DescribeTransitGatewayVpcAttachments
          - ec2:DescribeTags
        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[EC2TransitGatewayAttachmentProperties],
    ) -> ProgressEvent[EC2TransitGatewayAttachmentProperties]:
        """
        Delete a resource

        IAM permissions required:
          - ec2:DeleteTransitGatewayVpcAttachment
          - ec2:DeleteTags
        """
        model = request.desired_state
        request.aws_client_factory.ec2.delete_transit_gateway_vpc_attachment(
            TransitGatewayAttachmentId=model["Id"]
        )
        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model={},
        )

    def update(
        self,
        request: ResourceRequest[EC2TransitGatewayAttachmentProperties],
    ) -> ProgressEvent[EC2TransitGatewayAttachmentProperties]:
        """
        Update a resource

        IAM permissions required:
          - ec2:ModifyTransitGatewayVpcAttachment
          - ec2:DescribeTransitGatewayVpcAttachments
          - ec2:DeleteTags
          - ec2:CreateTags
        """
        raise NotImplementedError

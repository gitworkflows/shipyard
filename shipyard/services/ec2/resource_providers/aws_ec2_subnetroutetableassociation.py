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


class EC2SubnetRouteTableAssociationProperties(TypedDict):
    RouteTableId: Optional[str]
    SubnetId: Optional[str]
    Id: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class EC2SubnetRouteTableAssociationProvider(
    ResourceProvider[EC2SubnetRouteTableAssociationProperties]
):
    TYPE = "AWS::EC2::SubnetRouteTableAssociation"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[EC2SubnetRouteTableAssociationProperties],
    ) -> ProgressEvent[EC2SubnetRouteTableAssociationProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/Id

        Required properties:
          - RouteTableId
          - SubnetId

        Create-only properties:
          - /properties/SubnetId
          - /properties/RouteTableId

        Read-only properties:
          - /properties/Id

        IAM permissions required:
          - ec2:AssociateRouteTable
          - ec2:ReplaceRouteTableAssociation
          - ec2:DescribeSubnets
          - ec2:DescribeRouteTables

        """
        model = request.desired_state
        ec2 = request.aws_client_factory.ec2

        # TODO: validations
        if not request.custom_context.get(REPEATED_INVOCATION):
            # this is the first time this callback is invoked
            # TODO: defaults
            # TODO: idempotency
            model["Id"] = ec2.associate_route_table(
                RouteTableId=model["RouteTableId"], SubnetId=model["SubnetId"]
            )["AssociationId"]
            request.custom_context[REPEATED_INVOCATION] = True
            return ProgressEvent(
                status=OperationStatus.IN_PROGRESS,
                resource_model=model,
                custom_context=request.custom_context,
            )

        # we need to check association status
        route_table = ec2.describe_route_tables(RouteTableIds=[model["RouteTableId"]])[
            "RouteTables"
        ][0]
        for association in route_table["Associations"]:
            if association["RouteTableAssociationId"] == model["Id"]:
                # if it is showing up here, it's associated
                return ProgressEvent(
                    status=OperationStatus.SUCCESS,
                    resource_model=model,
                    custom_context=request.custom_context,
                )

        return ProgressEvent(
            status=OperationStatus.IN_PROGRESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[EC2SubnetRouteTableAssociationProperties],
    ) -> ProgressEvent[EC2SubnetRouteTableAssociationProperties]:
        """
        Fetch resource information

        IAM permissions required:
          - ec2:DescribeRouteTables
        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[EC2SubnetRouteTableAssociationProperties],
    ) -> ProgressEvent[EC2SubnetRouteTableAssociationProperties]:
        """
        Delete a resource

        IAM permissions required:
          - ec2:DisassociateRouteTable
          - ec2:DescribeSubnets
          - ec2:DescribeRouteTables
        """
        model = request.desired_state
        ec2 = request.aws_client_factory.ec2
        # TODO add async
        try:
            ec2.disassociate_route_table(AssociationId=model["Id"])
        except ec2.exceptions.ClientError:
            pass
        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def update(
        self,
        request: ResourceRequest[EC2SubnetRouteTableAssociationProperties],
    ) -> ProgressEvent[EC2SubnetRouteTableAssociationProperties]:
        """
        Update a resource


        """
        raise NotImplementedError

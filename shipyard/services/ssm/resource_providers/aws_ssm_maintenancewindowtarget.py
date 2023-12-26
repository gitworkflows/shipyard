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


class SSMMaintenanceWindowTargetProperties(TypedDict):
    ResourceType: Optional[str]
    Targets: Optional[list[Targets]]
    WindowId: Optional[str]
    Description: Optional[str]
    Id: Optional[str]
    Name: Optional[str]
    OwnerInformation: Optional[str]


class Targets(TypedDict):
    Key: Optional[str]
    Values: Optional[list[str]]


REPEATED_INVOCATION = "repeated_invocation"


class SSMMaintenanceWindowTargetProvider(ResourceProvider[SSMMaintenanceWindowTargetProperties]):
    TYPE = "AWS::SSM::MaintenanceWindowTarget"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[SSMMaintenanceWindowTargetProperties],
    ) -> ProgressEvent[SSMMaintenanceWindowTargetProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/Id

        Required properties:
          - WindowId
          - ResourceType
          - Targets

        Create-only properties:
          - /properties/WindowId

        Read-only properties:
          - /properties/Id



        """
        model = request.desired_state
        ssm = request.aws_client_factory.ssm

        params = util.select_attributes(
            model=model,
            params=[
                "Description",
                "Name",
                "OwnerInformation",
                "ResourceType",
                "Targets",
                "WindowId",
            ],
        )

        response = ssm.register_target_with_maintenance_window(**params)
        model["Id"] = response["WindowTargetId"]

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[SSMMaintenanceWindowTargetProperties],
    ) -> ProgressEvent[SSMMaintenanceWindowTargetProperties]:
        """
        Fetch resource information


        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[SSMMaintenanceWindowTargetProperties],
    ) -> ProgressEvent[SSMMaintenanceWindowTargetProperties]:
        """
        Delete a resource


        """
        model = request.desired_state
        ssm = request.aws_client_factory.ssm

        ssm.deregister_target_from_maintenance_window(
            WindowId=model["WindowId"], WindowTargetId=model["Id"]
        )

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def update(
        self,
        request: ResourceRequest[SSMMaintenanceWindowTargetProperties],
    ) -> ProgressEvent[SSMMaintenanceWindowTargetProperties]:
        """
        Update a resource


        """
        raise NotImplementedError

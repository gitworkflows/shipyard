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


class Route53HealthCheckProperties(TypedDict):
    HealthCheckConfig: Optional[dict]
    HealthCheckId: Optional[str]
    HealthCheckTags: Optional[list[HealthCheckTag]]


class HealthCheckTag(TypedDict):
    Key: Optional[str]
    Value: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class Route53HealthCheckProvider(ResourceProvider[Route53HealthCheckProperties]):
    TYPE = "AWS::Route53::HealthCheck"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[Route53HealthCheckProperties],
    ) -> ProgressEvent[Route53HealthCheckProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/HealthCheckId

        Required properties:
          - HealthCheckConfig

        Create-only properties:
          - /properties/HealthCheckConfig/Type
          - /properties/HealthCheckConfig/MeasureLatency
          - /properties/HealthCheckConfig/RequestInterval

        Read-only properties:
          - /properties/HealthCheckId

        IAM permissions required:
          - route53:CreateHealthCheck
          - route53:ChangeTagsForResource
          - cloudwatch:DescribeAlarms
          - route53-recovery-control-config:DescribeRoutingControl

        """
        model = request.desired_state
        create_params = util.select_attributes(model, ["HealthCheckConfig", "CallerReference"])
        if not create_params.get("CallerReference"):
            create_params["CallerReference"] = util.generate_default_name_without_stack(
                request.logical_resource_id
            )
        result = request.aws_client_factory.route53.create_health_check(**create_params)
        model["HealthCheckId"] = result["HealthCheck"]["Id"]
        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
        )

    def read(
        self,
        request: ResourceRequest[Route53HealthCheckProperties],
    ) -> ProgressEvent[Route53HealthCheckProperties]:
        """
        Fetch resource information

        IAM permissions required:
          - route53:GetHealthCheck
          - route53:ListTagsForResource
        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[Route53HealthCheckProperties],
    ) -> ProgressEvent[Route53HealthCheckProperties]:
        """
        Delete a resource

        IAM permissions required:
          - route53:DeleteHealthCheck
        """
        model = request.desired_state
        request.aws_client_factory.route53.delete_health_check(HealthCheckId=model["HealthCheckId"])
        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model={},
        )

    def update(
        self,
        request: ResourceRequest[Route53HealthCheckProperties],
    ) -> ProgressEvent[Route53HealthCheckProperties]:
        """
        Update a resource

        IAM permissions required:
          - route53:UpdateHealthCheck
          - route53:ChangeTagsForResource
          - route53:ListTagsForResource
          - cloudwatch:DescribeAlarms
        """
        raise NotImplementedError

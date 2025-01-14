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


class LambdaCodeSigningConfigProperties(TypedDict):
    AllowedPublishers: Optional[AllowedPublishers]
    CodeSigningConfigArn: Optional[str]
    CodeSigningConfigId: Optional[str]
    CodeSigningPolicies: Optional[CodeSigningPolicies]
    Description: Optional[str]


class AllowedPublishers(TypedDict):
    SigningProfileVersionArns: Optional[list[str]]


class CodeSigningPolicies(TypedDict):
    UntrustedArtifactOnDeployment: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class LambdaCodeSigningConfigProvider(ResourceProvider[LambdaCodeSigningConfigProperties]):
    TYPE = "AWS::Lambda::CodeSigningConfig"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[LambdaCodeSigningConfigProperties],
    ) -> ProgressEvent[LambdaCodeSigningConfigProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/CodeSigningConfigArn

        Required properties:
          - AllowedPublishers



        Read-only properties:
          - /properties/CodeSigningConfigId
          - /properties/CodeSigningConfigArn

        IAM permissions required:
          - lambda:CreateCodeSigningConfig

        """
        model = request.desired_state
        lambda_client = request.aws_client_factory.lambda_

        response = lambda_client.create_code_signing_config(**model)
        model["CodeSigningConfigArn"] = response["CodeSigningConfig"]["CodeSigningConfigArn"]

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[LambdaCodeSigningConfigProperties],
    ) -> ProgressEvent[LambdaCodeSigningConfigProperties]:
        """
        Fetch resource information

        IAM permissions required:
          - lambda:GetCodeSigningConfig
        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[LambdaCodeSigningConfigProperties],
    ) -> ProgressEvent[LambdaCodeSigningConfigProperties]:
        """
        Delete a resource

        IAM permissions required:
          - lambda:DeleteCodeSigningConfig
        """
        model = request.desired_state
        lambda_client = request.aws_client_factory.lambda_

        lambda_client.delete_code_signing_config(CodeSigningConfigArn=model["CodeSigningConfigArn"])

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def update(
        self,
        request: ResourceRequest[LambdaCodeSigningConfigProperties],
    ) -> ProgressEvent[LambdaCodeSigningConfigProperties]:
        """
        Update a resource

        IAM permissions required:
          - lambda:UpdateCodeSigningConfig
        """
        raise NotImplementedError

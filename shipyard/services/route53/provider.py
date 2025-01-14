from datetime import datetime
from typing import Optional

import moto.route53.models as route53_models
from moto.route53.models import route53_backends

from shipyard.aws.api import RequestContext
from shipyard.aws.api.route53 import (
    VPC,
    ChangeInfo,
    ChangeStatus,
    CreateHostedZoneResponse,
    DeleteHealthCheckResponse,
    DNSName,
    GetChangeResponse,
    GetHealthCheckResponse,
    HealthCheck,
    HealthCheckId,
    HostedZoneConfig,
    Nonce,
    NoSuchHealthCheck,
    ResourceId,
    Route53Api,
)
from shipyard.services.moto import call_moto
from shipyard.services.plugins import ServiceLifecycleHook


class Route53Provider(Route53Api, ServiceLifecycleHook):
    def create_hosted_zone(
        self,
        context: RequestContext,
        name: DNSName,
        caller_reference: Nonce,
        vpc: VPC = None,
        hosted_zone_config: HostedZoneConfig = None,
        delegation_set_id: ResourceId = None,
    ) -> CreateHostedZoneResponse:
        response = call_moto(context)

        # moto does not populate the VPC struct of the response if creating a private hosted zone
        if (
            hosted_zone_config
            and hosted_zone_config.get("PrivateZone", False)
            and "VPC" in response
            and vpc
        ):
            response["VPC"]["VPCId"] = response["VPC"]["VPCId"] or vpc.get("VPCId", "")
            response["VPC"]["VPCRegion"] = response["VPC"]["VPCRegion"] or vpc.get("VPCRegion", "")

        return response

    def get_change(self, context: RequestContext, id: ResourceId) -> GetChangeResponse:
        change_info = ChangeInfo(Id=id, Status=ChangeStatus.INSYNC, SubmittedAt=datetime.now())
        return GetChangeResponse(ChangeInfo=change_info)

    def get_health_check(
        self, context: RequestContext, health_check_id: HealthCheckId
    ) -> GetHealthCheckResponse:
        health_check: Optional[route53_models.HealthCheck] = route53_backends[context.account_id][
            "global"
        ].health_checks.get(health_check_id, None)
        if not health_check:
            raise NoSuchHealthCheck(
                f"No health check exists with the specified ID {health_check_id}"
            )
        health_check_config = {
            "Disabled": health_check.disabled,
            "EnableSNI": health_check.enable_sni,
            "FailureThreshold": health_check.failure_threshold,
            "FullyQualifiedDomainName": health_check.fqdn,
            "HealthThreshold": health_check.health_threshold,
            "Inverted": health_check.inverted,
            "IPAddress": health_check.ip_address,
            "MeasureLatency": health_check.measure_latency,
            "Port": health_check.port,
            "RequestInterval": health_check.request_interval,
            "ResourcePath": health_check.resource_path,
            "Type": health_check.type_,
        }
        return GetHealthCheckResponse(
            HealthCheck=HealthCheck(
                Id=health_check.id,
                CallerReference=health_check.caller_reference,
                HealthCheckConfig=health_check_config,
            )
        )

    def delete_health_check(
        self, context: RequestContext, health_check_id: HealthCheckId
    ) -> DeleteHealthCheckResponse:
        if health_check_id not in route53_backends[context.account_id]["global"].health_checks:
            raise NoSuchHealthCheck(
                f"No health check exists with the specified ID {health_check_id}"
            )

        route53_backends[context.account_id]["global"].delete_health_check(health_check_id)
        return {}

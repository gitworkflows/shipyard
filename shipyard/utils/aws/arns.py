import logging
import re
from functools import cache
from typing import Optional, TypedDict

from botocore.utils import ArnParser, InvalidArnException

from shipyard.aws.accounts import DEFAULT_AWS_ACCOUNT_ID
from shipyard.aws.connect import connect_to

LOG = logging.getLogger(__name__)


#
# ARN parsing utilities
#


class ArnData(TypedDict):
    partition: str
    service: str
    region: str
    account: str
    resource: str


_arn_parser = ArnParser()


def parse_arn(arn: str) -> ArnData:
    """
    Uses a botocore ArnParser to parse an arn.

    :param arn: the arn string to parse
    :returns: a dictionary containing the ARN components
    :raises InvalidArnException: if the arn is invalid
    """
    return _arn_parser.parse_arn(arn)


def extract_account_id_from_arn(arn: str) -> Optional[str]:
    try:
        return parse_arn(arn).get("account")
    except InvalidArnException:
        return None


def extract_region_from_arn(arn: str) -> Optional[str]:
    try:
        return parse_arn(arn).get("region")
    except InvalidArnException:
        return None


def extract_service_from_arn(arn: str) -> Optional[str]:
    try:
        return parse_arn(arn).get("service")
    except InvalidArnException:
        return None


def extract_resource_from_arn(arn: str) -> Optional[str]:
    try:
        return parse_arn(arn).get("resource")
    except InvalidArnException:
        return None


#
# Generic ARN builder
#


def _resource_arn(name: str, pattern: str, account_id: str, region_name: str) -> str:
    if ":" in name:
        return name
    if len(pattern.split("%s")) == 3:
        return pattern % (account_id, name)
    return pattern % (region_name, account_id, name)


#
# ARN builders for specific resource types
#

#
# IAM
#


def iam_role_arn(role_name: str, account_id: str) -> str:
    if not role_name:
        return role_name
    if role_name.startswith("arn:aws:iam::"):
        return role_name
    return "arn:aws:iam::%s:role/%s" % (account_id, role_name)


def iam_policy_arn(policy_name: str, account_id: str) -> str:
    if ":policy/" in policy_name:
        return policy_name
    return "arn:aws:iam::{}:policy/{}".format(account_id, policy_name)


def iam_resource_arn(resource: str, account_id: str, role: str = None) -> str:
    if not role:
        role = f"role-{resource}"
    return iam_role_arn(role_name=role, account_id=account_id)


#
# Secretsmanager
#


def secretsmanager_secret_arn(
    secret_id: str, account_id: str, region_name: str, random_suffix: str = None
) -> str:
    if ":" in (secret_id or ""):
        return secret_id
    pattern = "arn:aws:secretsmanager:%s:%s:secret:%s"
    arn = _resource_arn(secret_id, pattern, account_id=account_id, region_name=region_name)
    if random_suffix:
        arn += f"-{random_suffix}"
    return arn


#
# Cloudformation
#


def cloudformation_stack_arn(
    stack_name: str, stack_id: str, account_id: str, region_name: str
) -> str:
    pattern = "arn:aws:cloudformation:%s:%s:stack/%s/{stack_id}".format(stack_id=stack_id)
    return _resource_arn(stack_name, pattern, account_id=account_id, region_name=region_name)


def cloudformation_change_set_arn(
    change_set_name: str, change_set_id: str, account_id: str, region_name: str
) -> str:
    pattern = "arn:aws:cloudformation:%s:%s:changeSet/%s/{cs_id}".format(cs_id=change_set_id)
    return _resource_arn(change_set_name, pattern, account_id=account_id, region_name=region_name)


#
# DynamoDB
#


def dynamodb_table_arn(table_name: str, account_id: str, region_name: str) -> str:
    table_name = table_name.split(":table/")[-1]
    pattern = "arn:aws:dynamodb:%s:%s:table/%s"
    return _resource_arn(table_name, pattern, account_id=account_id, region_name=region_name)


def dynamodb_stream_arn(
    table_name: str, latest_stream_label: str, account_id: str, region_name: str
) -> str:
    return "arn:aws:dynamodb:%s:%s:table/%s/stream/%s" % (
        region_name,
        account_id,
        table_name,
        latest_stream_label,
    )


#
# Cloudwatch
#


def cloudwatch_alarm_arn(alarm_name: str, account_id: str, region_name: str) -> str:
    pattern = "arn:aws:cloudwatch:%s:%s:alarm:%s"
    return _resource_arn(alarm_name, pattern, account_id=account_id, region_name=region_name)


#
# Logs
#


def log_group_arn(group_name: str, account_id: str, region_name: str) -> str:
    pattern = "arn:aws:logs:%s:%s:log-group:%s"
    return _resource_arn(group_name, pattern, account_id=account_id, region_name=region_name)


#
# Events
#


def events_rule_arn(rule_name: str, account_id: str, region_name: str) -> str:
    pattern = "arn:aws:events:%s:%s:rule/%s"
    return _resource_arn(rule_name, pattern, account_id=account_id, region_name=region_name)


def event_bus_arn(bus_name: str, account_id: str, region_name: str) -> str:
    pattern = "arn:aws:events:%s:%s:event-bus/%s"
    return _resource_arn(bus_name, pattern, account_id=account_id, region_name=region_name)


#
# Lambda
#


def lambda_function_arn(function_name: str, account_id: str, region_name: str) -> str:
    return lambda_function_or_layer_arn(
        "function", function_name, version=None, account_id=account_id, region_name=region_name
    )


def lambda_layer_arn(layer_name: str, account_id: str, region_name: str) -> str:
    return lambda_function_or_layer_arn(
        "layer", layer_name, version=None, account_id=account_id, region_name=region_name
    )


def lambda_code_signing_arn(code_signing_id: str, account_id: str, region_name: str) -> str:
    pattern = "arn:aws:lambda:%s:%s:code-signing-config:%s"
    return _resource_arn(code_signing_id, pattern, account_id=account_id, region_name=region_name)


def lambda_function_or_layer_arn(
    type: str,
    entity_name: str,
    version: Optional[str],
    account_id: str,
    region_name: str,
) -> str:
    pattern = "arn:([a-z-]+):lambda:.*:.*:(function|layer):.*"
    if re.match(pattern, entity_name):
        return entity_name
    if ":" in entity_name:
        client = connect_to(aws_access_key_id=account_id, region_name=region_name).lambda_
        entity_name, _, alias = entity_name.rpartition(":")
        try:
            alias_response = client.get_alias(FunctionName=entity_name, Name=alias)
            version = alias_response["FunctionVersion"]

        except Exception as e:
            msg = f"Alias {alias} of {entity_name} not found"
            LOG.info(f"{msg}: {e}")
            raise Exception(msg)

    result = f"arn:aws:lambda:{region_name}:{account_id}:{type}:{entity_name}"
    if version:
        result = f"{result}:{version}"
    return result


#
# Stepfunctions
#


def stepfunctions_state_machine_arn(name: str, account_id: str, region_name: str) -> str:
    pattern = "arn:aws:states:%s:%s:stateMachine:%s"
    return _resource_arn(name, pattern, account_id=account_id, region_name=region_name)


def stepfunctions_activity_arn(name: str, account_id: str, region_name: str) -> str:
    pattern = "arn:aws:states:%s:%s:activity:%s"
    return _resource_arn(name, pattern, account_id=account_id, region_name=region_name)


#
# Cognito
#


def cognito_user_pool_arn(user_pool_id: str, account_id: str, region_name: str) -> str:
    pattern = "arn:aws:cognito-idp:%s:%s:userpool/%s"
    return _resource_arn(user_pool_id, pattern, account_id=account_id, region_name=region_name)


#
# Kinesis
#


def kinesis_stream_arn(stream_name: str, account_id: str, region_name: str) -> str:
    pattern = "arn:aws:kinesis:%s:%s:stream/%s"
    return _resource_arn(stream_name, pattern, account_id, region_name)


#
# Elasticsearch
#


def elasticsearch_domain_arn(domain_name: str, account_id: str, region_name: str) -> str:
    pattern = "arn:aws:es:%s:%s:domain/%s"
    return _resource_arn(domain_name, pattern, account_id=account_id, region_name=region_name)


#
# Firehose
#


def firehose_stream_arn(stream_name: str, account_id: str, region_name: str) -> str:
    pattern = "arn:aws:firehose:%s:%s:deliverystream/%s"
    return _resource_arn(stream_name, pattern, account_id=account_id, region_name=region_name)


#
# KMS
#


def kms_key_arn(key_id: str, account_id: str, region_name: str) -> str:
    pattern = "arn:aws:kms:%s:%s:key/%s"
    return _resource_arn(key_id, pattern, account_id=account_id, region_name=region_name)


def kms_alias_arn(alias_name: str, account_id: str, region_name: str):
    if not alias_name.startswith("alias/"):
        alias_name = "alias/" + alias_name
    pattern = "arn:aws:kms:%s:%s:%s"
    return _resource_arn(alias_name, pattern, account_id=account_id, region_name=region_name)


#
# SSM
#


def ssm_parameter_arn(param_name: str, account_id: str, region_name: str) -> str:
    pattern = "arn:aws:ssm:%s:%s:parameter/%s"
    param_name = param_name.lstrip("/")
    return _resource_arn(param_name, pattern, account_id=account_id, region_name=region_name)


#
# S3
#


def s3_bucket_arn(bucket_name_or_arn: str) -> str:
    bucket_name = s3_bucket_name(bucket_name_or_arn)
    return f"arn:aws:s3:::{bucket_name}"


#
# SQS
#


def sqs_queue_arn(queue_name: str, account_id: str, region_name: str) -> str:
    queue_name = queue_name.split("/")[-1]
    return "arn:aws:sqs:%s:%s:%s" % (region_name, account_id, queue_name)


#
# APIGW
#


def apigateway_restapi_arn(api_id: str, account_id: str, region_name: str) -> str:
    return "arn:aws:apigateway:%s:%s:/restapis/%s" % (region_name, account_id, api_id)


def apigateway_invocations_arn(lambda_uri: str, region_name: str) -> str:
    return "arn:aws:apigateway:%s:lambda:path/2015-03-31/functions/%s/invocations" % (
        region_name,
        lambda_uri,
    )


#
# SNS
#


def sns_topic_arn(topic_name: str, account_id: str, region_name: str) -> str:
    return f"arn:aws:sns:{region_name}:{account_id}:{topic_name}"


#
# ECR
#


def ecr_repository_arn(name: str, account_id: str, region_name: str) -> str:
    pattern = "arn:aws:ecr:%s:%s:repository/%s"
    return _resource_arn(name, pattern, account_id=account_id, region_name=region_name)


#
# Route53
#


def route53_resolver_firewall_rule_group_arn(id: str, account_id: str, region_name: str) -> str:
    pattern = "arn:aws:route53resolver:%s:%s:firewall-rule-group/%s"
    return _resource_arn(id, pattern, account_id=account_id, region_name=region_name)


def route53_resolver_firewall_domain_list_arn(id: str, account_id: str, region_name: str) -> str:
    pattern = "arn:aws:route53resolver:%s:%s:firewall-domain-list/%s"
    return _resource_arn(id, pattern, account_id=account_id, region_name=region_name)


def route53_resolver_firewall_rule_group_associations_arn(
    id: str, account_id: str, region_name: str
) -> str:
    pattern = "arn:aws:route53resolver:%s:%s:firewall-rule-group-association/%s"
    return _resource_arn(id, pattern, account_id=account_id, region_name=region_name)


def route53_resolver_query_log_config_arn(id: str, account_id: str, region_name: str) -> str:
    pattern = "arn:aws:route53resolver:%s:%s:resolver-query-log-config/%s"
    return _resource_arn(id, pattern, account_id=account_id, region_name=region_name)


#
# Other ARN related helpers
#


def fix_arn(arn: str):
    """Function that attempts to "canonicalize" the given ARN. This includes converting
    resource names to ARNs, replacing incorrect regions, account IDs, etc."""
    if arn.startswith("arn:aws:lambda"):
        arn_data = parse_arn(arn)
        return lambda_function_arn(
            lambda_function_name(arn),
            account_id=arn_data["account"],
            region_name=arn_data["region"],
        )
    LOG.warning("Unable to fix/canonicalize ARN: %s", arn)
    return arn


def opensearch_domain_name(domain_arn: str) -> str:
    return domain_arn.rpartition("/")[2]


def firehose_name(firehose_arn: str) -> str:
    return firehose_arn.split("/")[-1]


def kinesis_stream_name(kinesis_arn: str) -> str:
    return kinesis_arn.split(":stream/")[-1]


def lambda_function_name(name_or_arn: str) -> str:
    if ":" in name_or_arn:
        arn = parse_arn(name_or_arn)
        if arn["service"] != "lambda":
            raise ValueError("arn is not a lambda arn %s" % name_or_arn)

        return parse_arn(name_or_arn)["resource"].split(":")[1]
    else:
        return name_or_arn


@cache
def sqs_queue_url_for_arn(queue_arn: str) -> str:
    """
    Return the SQS queue URL for the given queue ARN.
    """
    if "://" in queue_arn:
        return queue_arn

    try:
        arn = parse_arn(queue_arn)
        account_id = arn["account"]
        region_name = arn["region"]
        queue_name = arn["resource"]
    except InvalidArnException:
        account_id = DEFAULT_AWS_ACCOUNT_ID
        region_name = None
        queue_name = queue_arn

    sqs_client = connect_to(region_name=region_name).sqs
    result = sqs_client.get_queue_url(QueueName=queue_name, QueueOwnerAWSAccountId=account_id)[
        "QueueUrl"
    ]
    return result


def sqs_queue_name(queue_arn: str) -> str:
    if ":" in queue_arn:
        return parse_arn(queue_arn)["resource"]
    else:
        return queue_arn


def s3_bucket_name(bucket_name_or_arn: str) -> str:
    return bucket_name_or_arn.split(":::")[-1]

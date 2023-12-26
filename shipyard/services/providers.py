from shipyard.aws.forwarder import HttpFallbackDispatcher
from shipyard.services.plugins import (
    Service,
    aws_provider,
)


@aws_provider()
def acm():
    from shipyard.services.acm.provider import AcmProvider
    from shipyard.services.moto import MotoFallbackDispatcher

    provider = AcmProvider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider(api="apigateway")
def apigateway():
    from shipyard.services.apigateway.provider import ApigatewayProvider
    from shipyard.services.moto import MotoFallbackDispatcher

    provider = ApigatewayProvider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider()
def cloudformation():
    from shipyard.services.cloudformation.provider import CloudformationProvider

    provider = CloudformationProvider()
    return Service.for_provider(provider)


@aws_provider(api="config")
def awsconfig():
    from shipyard.services.configservice.provider import ConfigProvider
    from shipyard.services.moto import MotoFallbackDispatcher

    provider = ConfigProvider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider()
def cloudwatch():
    from shipyard.services.cloudwatch.provider import CloudwatchProvider
    from shipyard.services.moto import MotoFallbackDispatcher

    provider = CloudwatchProvider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider()
def dynamodb():
    from shipyard.services.dynamodb.provider import DynamoDBProvider

    provider = DynamoDBProvider()
    return Service.for_provider(
        provider,
        dispatch_table_factory=lambda _provider: HttpFallbackDispatcher(
            _provider, _provider.get_forward_url
        ),
    )


@aws_provider()
def dynamodbstreams():
    from shipyard.services.dynamodbstreams.provider import DynamoDBStreamsProvider

    provider = DynamoDBStreamsProvider()
    return Service.for_provider(provider)


@aws_provider()
def ec2():
    from shipyard.services.ec2.provider import Ec2Provider
    from shipyard.services.moto import MotoFallbackDispatcher

    provider = Ec2Provider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider()
def es():
    from shipyard.services.es.provider import EsProvider

    provider = EsProvider()
    return Service.for_provider(provider)


@aws_provider()
def firehose():
    from shipyard.services.firehose.provider import FirehoseProvider

    provider = FirehoseProvider()
    return Service.for_provider(provider)


@aws_provider()
def iam():
    from shipyard.services.iam.provider import IamProvider
    from shipyard.services.moto import MotoFallbackDispatcher

    provider = IamProvider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider()
def sts():
    from shipyard.services.moto import MotoFallbackDispatcher
    from shipyard.services.sts.provider import StsProvider

    provider = StsProvider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider()
def kinesis():
    from shipyard.services.kinesis.provider import KinesisProvider

    provider = KinesisProvider()
    return Service.for_provider(
        provider,
        dispatch_table_factory=lambda _provider: HttpFallbackDispatcher(
            _provider, _provider.get_forward_url
        ),
    )


@aws_provider()
def kms():
    from shipyard.services.kms.provider import KmsProvider

    provider = KmsProvider()
    return Service.for_provider(provider)


@aws_provider(api="lambda")
def lambda_():
    from shipyard.services.lambda_.provider import LambdaProvider

    provider = LambdaProvider()
    return Service.for_provider(provider)


@aws_provider(api="lambda", name="asf")
def lambda_asf():
    from shipyard.services.lambda_.provider import LambdaProvider

    provider = LambdaProvider()
    return Service.for_provider(provider)


@aws_provider(api="lambda", name="v2")
def lambda_v2():
    from shipyard.services.lambda_.provider import LambdaProvider

    provider = LambdaProvider()
    return Service.for_provider(provider)


@aws_provider()
def logs():
    from shipyard.services.logs.provider import LogsProvider
    from shipyard.services.moto import MotoFallbackDispatcher

    provider = LogsProvider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider()
def opensearch():
    from shipyard.services.opensearch.provider import OpensearchProvider

    provider = OpensearchProvider()
    return Service.for_provider(provider)


@aws_provider()
def redshift():
    from shipyard.services.moto import MotoFallbackDispatcher
    from shipyard.services.redshift.provider import RedshiftProvider

    provider = RedshiftProvider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider()
def route53():
    from shipyard.services.moto import MotoFallbackDispatcher
    from shipyard.services.route53.provider import Route53Provider

    provider = Route53Provider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider()
def route53resolver():
    from shipyard.services.moto import MotoFallbackDispatcher
    from shipyard.services.route53resolver.provider import Route53ResolverProvider

    provider = Route53ResolverProvider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider(api="s3", name="asf")
def s3_asf():
    from shipyard.services.moto import MotoFallbackDispatcher
    from shipyard.services.s3.provider import S3Provider

    provider = S3Provider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider(api="s3", name="v2")
def s3_v2():
    from shipyard.services.moto import MotoFallbackDispatcher
    from shipyard.services.s3.provider import S3Provider

    provider = S3Provider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider(api="s3", name="legacy_v2")
def s3_legacy_v2():
    from shipyard.services.moto import MotoFallbackDispatcher
    from shipyard.services.s3.provider import S3Provider

    provider = S3Provider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider(api="s3", name="default")
def s3():
    from shipyard.services.s3.v3.provider import S3Provider

    provider = S3Provider()
    return Service.for_provider(provider)


@aws_provider(api="s3", name="stream")
def s3_stream():
    from shipyard.services.s3.v3.provider import S3Provider

    provider = S3Provider()
    return Service.for_provider(provider)


@aws_provider(api="s3", name="v3")
def s3_v3():
    from shipyard.services.s3.v3.provider import S3Provider

    provider = S3Provider()
    return Service.for_provider(provider)


@aws_provider()
def s3control():
    from shipyard.services.moto import MotoFallbackDispatcher
    from shipyard.services.s3control.provider import S3ControlProvider

    provider = S3ControlProvider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider()
def scheduler():
    from shipyard.services.moto import MotoFallbackDispatcher
    from shipyard.services.scheduler.provider import SchedulerProvider

    provider = SchedulerProvider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider()
def secretsmanager():
    from shipyard.services.moto import MotoFallbackDispatcher
    from shipyard.services.secretsmanager.provider import SecretsmanagerProvider

    provider = SecretsmanagerProvider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider()
def ses():
    from shipyard.services.moto import MotoFallbackDispatcher
    from shipyard.services.ses.provider import SesProvider

    provider = SesProvider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider()
def sns():
    from shipyard.services.moto import MotoFallbackDispatcher
    from shipyard.services.sns.provider import SnsProvider

    provider = SnsProvider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


sqs_provider = None


def get_sqs_provider():
    """
    Creates the SQS provider instance (and registers the query API routes) in a singleton fashion, such that the
    same instance of the provider can be used by multiple services (i.e. the `sqs` as well as the `sqs-query` service).

    TODO it would be great if we could find a better solution to use a single provider for multiple services
    """
    global sqs_provider

    if not sqs_provider:
        from shipyard.services import edge
        from shipyard.services.sqs import query_api
        from shipyard.services.sqs.provider import SqsProvider

        query_api.register(edge.ROUTER)

        sqs_provider = SqsProvider()
    return sqs_provider


@aws_provider()
def sqs():
    return Service.for_provider(get_sqs_provider())


@aws_provider("sqs-query")
def sqs_query():
    sqs_query_service = Service.for_provider(
        get_sqs_provider(),
        custom_service_name="sqs-query",
    )
    return sqs_query_service


@aws_provider()
def ssm():
    from shipyard.services.moto import MotoFallbackDispatcher
    from shipyard.services.ssm.provider import SsmProvider

    provider = SsmProvider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider()
def events():
    from shipyard.services.events.provider import EventsProvider
    from shipyard.services.moto import MotoFallbackDispatcher

    provider = EventsProvider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider()
def stepfunctions():
    from shipyard.services.stepfunctions.provider import StepFunctionsProvider

    provider = StepFunctionsProvider()
    return Service.for_provider(provider)


@aws_provider(api="stepfunctions", name="v2")
def stepfunctions_v2():
    from shipyard.services.stepfunctions.provider import StepFunctionsProvider

    provider = StepFunctionsProvider()
    return Service.for_provider(provider)


@aws_provider(api="stepfunctions", name="v1")
def stepfunctions_legacy():
    from shipyard.services.stepfunctions.legacy.provider_legacy import StepFunctionsProvider

    provider = StepFunctionsProvider()
    return Service.for_provider(
        provider,
        dispatch_table_factory=lambda _provider: HttpFallbackDispatcher(
            _provider, _provider.get_forward_url
        ),
    )


@aws_provider(api="stepfunctions", name="legacy")
def stepfunctions_v1():
    from shipyard.services.stepfunctions.legacy.provider_legacy import StepFunctionsProvider

    provider = StepFunctionsProvider()
    return Service.for_provider(
        provider,
        dispatch_table_factory=lambda _provider: HttpFallbackDispatcher(
            _provider, _provider.get_forward_url
        ),
    )


@aws_provider()
def swf():
    from shipyard.services.moto import MotoFallbackDispatcher
    from shipyard.services.swf.provider import SWFProvider

    provider = SWFProvider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider()
def resourcegroupstaggingapi():
    from shipyard.services.moto import MotoFallbackDispatcher
    from shipyard.services.resourcegroupstaggingapi.provider import (
        ResourcegroupstaggingapiProvider,
    )

    provider = ResourcegroupstaggingapiProvider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider(api="resource-groups")
def resource_groups():
    from shipyard.services.moto import MotoFallbackDispatcher
    from shipyard.services.resource_groups.provider import ResourceGroupsProvider

    provider = ResourceGroupsProvider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider()
def support():
    from shipyard.services.moto import MotoFallbackDispatcher
    from shipyard.services.support.provider import SupportProvider

    provider = SupportProvider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)


@aws_provider()
def transcribe():
    from shipyard.services.moto import MotoFallbackDispatcher
    from shipyard.services.transcribe.provider import TranscribeProvider

    provider = TranscribeProvider()
    return Service.for_provider(provider, dispatch_table_factory=MotoFallbackDispatcher)

from typing import Dict, List, TypedDict

import pytest
from botocore.parsers import create_parser

from shipyard.aws.api import (
    CommonServiceException,
    HttpRequest,
    RequestContext,
    ServiceException,
    ServiceRequest,
    handler,
)
from shipyard.aws.api.sqs import SendMessageRequest
from shipyard.aws.skeleton import DispatchTable, ServiceRequestDispatcher, Skeleton
from shipyard.aws.spec import load_service

""" Stripped down version of the SQS API generated by the Scaffold. """

String = str
StringList = List[String]

Binary = bytes
BinaryList = List[Binary]
Integer = int


class MessageAttributeValue(TypedDict):
    StringValue: String
    BinaryValue: Binary
    StringListValues: StringList
    BinaryListValues: BinaryList
    DataType: String


class MessageSystemAttributeName(str):
    SenderId = "SenderId"
    SentTimestamp = "SentTimestamp"
    ApproximateReceiveCount = "ApproximateReceiveCount"
    ApproximateFirstReceiveTimestamp = "ApproximateFirstReceiveTimestamp"
    SequenceNumber = "SequenceNumber"
    MessageDeduplicationId = "MessageDeduplicationId"
    MessageGroupId = "MessageGroupId"
    AWSTraceHeader = "AWSTraceHeader"


class MessageSystemAttributeNameForSends(str):
    AWSTraceHeader = "AWSTraceHeader"


class SendMessageResult(TypedDict):
    MD5OfMessageBody: String
    MD5OfMessageAttributes: String
    MD5OfMessageSystemAttributes: String
    MessageId: String
    SequenceNumber: String


class MessageSystemAttributeValue(TypedDict):
    StringValue: String
    BinaryValue: Binary
    StringListValues: StringList
    BinaryListValues: BinaryList
    DataType: String


MessageBodyAttributeMap = Dict[String, MessageAttributeValue]
MessageSystemAttributeMap = Dict[MessageSystemAttributeName, String]
MessageBodySystemAttributeMap = Dict[
    MessageSystemAttributeNameForSends, MessageSystemAttributeValue
]


class InvalidMessageContents(ServiceException):
    pass


class UnsupportedOperation(ServiceException):
    pass


class TestSqsApi:
    service = "sqs"
    version = "2012-11-05"

    @handler("SendMessage")
    def send_message(
        self,
        context: RequestContext,
        queue_url: String,
        message_body: String,
        delay_seconds: Integer = None,
        message_attributes: MessageBodyAttributeMap = None,
        message_system_attributes: MessageBodySystemAttributeMap = None,
        message_deduplication_id: String = None,
        message_group_id: String = None,
    ) -> SendMessageResult:
        return {
            "MD5OfMessageBody": "String",
            "MD5OfMessageAttributes": "String",
            "MD5OfMessageSystemAttributes": "String",
            "MessageId": "String",
            "SequenceNumber": "String",
        }


class TestSqsApiNotImplemented:
    service = "sqs"
    version = "2012-11-05"

    @handler("SendMessage")
    def send_message(
        self,
        context: RequestContext,
        queue_url: String,
        message_body: String,
        delay_seconds: Integer = None,
        message_attributes: MessageBodyAttributeMap = None,
        message_system_attributes: MessageBodySystemAttributeMap = None,
        message_deduplication_id: String = None,
        message_group_id: String = None,
    ) -> SendMessageResult:
        raise NotImplementedError


class TestSqsApiNotImplementedWithMessage:
    service = "sqs"
    version = "2012-11-05"

    @handler("SendMessage", expand=False)
    def send_message(
        self,
        context: RequestContext,
        request: SendMessageRequest,
    ) -> SendMessageResult:
        raise NotImplementedError("We will implement it soon, that's a promise!")


""" Test implementations """


def _get_sqs_request_headers():
    return {
        "Remote-Addr": "127.0.0.1",
        "Host": "localhost:4566",
        "Accept-Encoding": "identity",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "User-Agent": "aws-cli/1.20.47 Python/3.8.10 Linux/5.4.0-88-generic botocore/1.21.47",
        "X-Amz-Date": "20211009T185815Z",
        "Authorization": "AWS4-HMAC-SHA256 Credential=test/20211009/us-east-1/sqs/aws4_request, SignedHeaders=content-type;host;x-amz-date, Signature=d9f93b13a07dda8cba650fba583fab92e0c72465e5e02fb56a3bb4994aefc339",
        "Content-Length": "169",
        "x-shipyard-request-url": "http://localhost:4566/",
        "X-Forwarded-For": "127.0.0.1, localhost:4566",
    }


def test_skeleton_e2e_sqs_send_message():
    sqs_service = load_service("sqs-query")
    skeleton = Skeleton(sqs_service, TestSqsApi())
    context = RequestContext()
    context.account = "test"
    context.region = "us-west-1"
    context.service = sqs_service
    context.request = HttpRequest(
        **{
            "method": "POST",
            "path": "/",
            "body": "Action=SendMessage&Version=2012-11-05&QueueUrl=http%3A%2F%2Flocalhost%3A4566%2F000000000000%2Ftf-acc-test-queue&MessageBody=%7B%22foo%22%3A+%22bared%22%7D&DelaySeconds=2",
            "headers": _get_sqs_request_headers(),
        }
    )
    result = skeleton.invoke(context)

    # Use the parser from botocore to parse the serialized response
    response_parser = create_parser("query")
    parsed_response = response_parser.parse(
        result.to_readonly_response_dict(), sqs_service.operation_model("SendMessage").output_shape
    )

    # Test the ResponseMetadata and delete it afterwards
    assert "ResponseMetadata" in parsed_response
    assert "RequestId" in parsed_response["ResponseMetadata"]
    assert len(parsed_response["ResponseMetadata"]["RequestId"]) == 36
    assert "HTTPStatusCode" in parsed_response["ResponseMetadata"]
    assert parsed_response["ResponseMetadata"]["HTTPStatusCode"] == 200
    del parsed_response["ResponseMetadata"]

    # Compare the (remaining) actual payload
    assert parsed_response == {
        "MD5OfMessageBody": "String",
        "MD5OfMessageAttributes": "String",
        "MD5OfMessageSystemAttributes": "String",
        "MessageId": "String",
        "SequenceNumber": "String",
    }


@pytest.mark.parametrize(
    "api_class, oracle_message",
    [
        (
            TestSqsApiNotImplemented(),
            "API action 'SendMessage' for service 'sqs' not yet implemented or pro feature"
            " - please check https://docs.shipyard.khulnasoft.com/references/coverage/coverage_sqs/ for further information",
        ),
        (
            TestSqsApiNotImplementedWithMessage(),
            "We will implement it soon, that's a promise!",
        ),
    ],
)
def test_skeleton_e2e_sqs_send_message_not_implemented(api_class, oracle_message):
    sqs_service = load_service("sqs-query")
    skeleton = Skeleton(sqs_service, api_class)
    context = RequestContext()
    context.account = "test"
    context.region = "us-west-1"
    context.service = sqs_service
    context.request = HttpRequest(
        **{
            "method": "POST",
            "path": "/",
            "body": "Action=SendMessage&Version=2012-11-05&QueueUrl=http%3A%2F%2Flocalhost%3A4566%2F000000000000%2Ftf-acc-test-queue&MessageBody=%7B%22foo%22%3A+%22bared%22%7D&DelaySeconds=2",
            "headers": _get_sqs_request_headers(),
        }
    )
    result = skeleton.invoke(context)

    # Use the parser from botocore to parse the serialized response
    response_parser = create_parser(sqs_service.protocol)
    parsed_response = response_parser.parse(
        result.to_readonly_response_dict(), sqs_service.operation_model("SendMessage").output_shape
    )

    # Test the ResponseMetadata
    assert "ResponseMetadata" in parsed_response
    assert "RequestId" in parsed_response["ResponseMetadata"]
    assert len(parsed_response["ResponseMetadata"]["RequestId"]) == 36
    assert "HTTPStatusCode" in parsed_response["ResponseMetadata"]
    assert parsed_response["ResponseMetadata"]["HTTPStatusCode"] == 501

    # Compare the (remaining) actual error payload
    assert "Error" in parsed_response
    assert parsed_response["Error"] == {
        "Code": "InternalFailure",
        "Message": oracle_message,
    }


def test_dispatch_common_service_exception():
    def delete_queue(_context: RequestContext, _request: ServiceRequest):
        raise CommonServiceException("NonExistentQueue", "No such queue")

    table: DispatchTable = {}
    table["DeleteQueue"] = delete_queue

    sqs_service = load_service("sqs-query")
    skeleton = Skeleton(sqs_service, table)

    context = RequestContext()
    context.account = "test"
    context.region = "us-west-1"
    context.service = sqs_service
    context.request = HttpRequest(
        **{
            "method": "POST",
            "path": "/",
            "body": "Action=DeleteQueue&Version=2012-11-05&QueueUrl=http%3A%2F%2Flocalhost%3A4566%2F000000000000%2Ftf-acc-test-queue",
            "headers": _get_sqs_request_headers(),
        }
    )
    result = skeleton.invoke(context)

    # Use the parser from botocore to parse the serialized response
    response_parser = create_parser(sqs_service.protocol)
    parsed_response = response_parser.parse(
        result.to_readonly_response_dict(), sqs_service.operation_model("SendMessage").output_shape
    )

    assert "Error" in parsed_response
    assert parsed_response["Error"] == {
        "Code": "NonExistentQueue",
        "Message": "No such queue",
    }


def test_dispatch_missing_method_returns_internal_failure():
    table: DispatchTable = {}

    sqs_service = load_service("sqs-query")
    skeleton = Skeleton(sqs_service, table)

    context = RequestContext()
    context.account = "test"
    context.region = "us-west-1"
    context.service = sqs_service
    context.request = HttpRequest(
        **{
            "method": "POST",
            "path": "/",
            "body": "Action=DeleteQueue&Version=2012-11-05&QueueUrl=http%3A%2F%2Flocalhost%3A4566%2F000000000000%2Ftf-acc-test-queue",
            "headers": _get_sqs_request_headers(),
        }
    )

    result = skeleton.invoke(context)
    # Use the parser from botocore to parse the serialized response
    response_parser = create_parser(sqs_service.protocol)
    parsed_response = response_parser.parse(
        result.to_readonly_response_dict(), sqs_service.operation_model("SendMessage").output_shape
    )
    assert "Error" in parsed_response
    assert parsed_response["Error"] == {
        "Code": "InternalFailure",
        "Message": "API action 'DeleteQueue' for service 'sqs' not yet implemented or pro feature - please check "
        "https://docs.shipyard.khulnasoft.com/references/coverage/coverage_sqs/ for further information",
    }


class TestServiceRequestDispatcher:
    def test_default_dispatcher(self):
        class SomeAction(ServiceRequest):
            ArgOne: str
            ArgTwo: int

        def fn(context, arg_one, arg_two):
            assert type(context) == RequestContext
            assert arg_one == "foo"
            assert arg_two == 69

        dispatcher = ServiceRequestDispatcher(fn, "SomeAction")
        dispatcher(RequestContext(), SomeAction(ArgOne="foo", ArgTwo=69))

    def test_without_context_without_expand(self):
        def fn(*args):
            assert len(args) == 1
            assert type(args[0]) == dict

        dispatcher = ServiceRequestDispatcher(
            fn, "SomeAction", pass_context=False, expand_parameters=False
        )
        dispatcher(RequestContext(), ServiceRequest())

    def test_without_expand(self):
        def fn(*args):
            assert len(args) == 2
            assert type(args[0]) == RequestContext
            assert type(args[1]) == dict

        dispatcher = ServiceRequestDispatcher(
            fn, "SomeAction", pass_context=True, expand_parameters=False
        )
        dispatcher(RequestContext(), ServiceRequest())

    def test_dispatch_without_args(self):
        def fn(context):
            assert type(context) == RequestContext

        dispatcher = ServiceRequestDispatcher(fn, "SomeAction")
        dispatcher(RequestContext(), ServiceRequest())

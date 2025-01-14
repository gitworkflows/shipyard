import json
import os

from shipyard.testing.pytest import markers
from shipyard.utils.strings import short_uid


@markers.aws.validated
def test_alarm_creation(deploy_cfn_template, snapshot):
    snapshot.add_transformer(snapshot.transform.resource_name())
    alarm_name = f"alarm-{short_uid()}"

    template = json.dumps(
        {
            "Resources": {
                "Alarm": {
                    "Type": "AWS::CloudWatch::Alarm",
                    "Properties": {
                        "AlarmName": alarm_name,
                        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
                        "EvaluationPeriods": 1,
                        "MetricName": "Errors",
                        "Namespace": "AWS/Lambda",
                        "Period": 300,
                        "Statistic": "Average",
                        "Threshold": 1,
                    },
                }
            },
            "Outputs": {
                "AlarmName": {"Value": {"Ref": "Alarm"}},
                "AlarmArnFromAtt": {"Value": {"Fn::GetAtt": "Alarm.Arn"}},
            },
        }
    )

    outputs = deploy_cfn_template(template=template).outputs
    snapshot.match("alarm_outputs", outputs)


@markers.aws.validated
@markers.snapshot.skip_snapshot_verify(
    paths=[
        "$..StateReason",
        "$..StateReasonData",
        "$..StateTransitionedTimestamp",
        "$..StateValue",
        "$..AlarmActions",
        "$..AlarmRule",
        "$..StateReason",
        "$..StateReasonData",
        "$..StateTransitionedTimestamp",
        "$..StateValue",
    ]
)
def test_composite_alarm_creation(aws_client, deploy_cfn_template, snapshot):
    snapshot.add_transformer(snapshot.transform.cloudwatch_api())
    stack = deploy_cfn_template(
        template_path=os.path.join(
            os.path.dirname(__file__), "../../../templates/cfn_cw_composite_alarm.yml"
        ),
    )
    composite_alarm_name = stack.outputs["CompositeAlarmName"]
    response = aws_client.cloudwatch.describe_alarms(
        AlarmNames=[composite_alarm_name], AlarmTypes=["CompositeAlarm"]
    )
    snapshot.match("composite_alarm", response["CompositeAlarms"])

    metric_alarm_name = stack.outputs["MetricAlarmName"]
    response = aws_client.cloudwatch.describe_alarms(AlarmNames=[metric_alarm_name])
    snapshot.match("metric_alarm", response["MetricAlarms"])

    stack.destroy()
    response = aws_client.cloudwatch.describe_alarms(
        AlarmNames=[composite_alarm_name], AlarmTypes=["CompositeAlarm"]
    )
    assert not response["CompositeAlarms"]
    response = aws_client.cloudwatch.describe_alarms(AlarmNames=[metric_alarm_name])
    assert not response["MetricAlarms"]


@markers.aws.validated
@markers.snapshot.skip_snapshot_verify(paths=["$..StateTransitionedTimestamp"])
def test_alarm_ext_statistic(aws_client, deploy_cfn_template, snapshot):
    snapshot.add_transformer(snapshot.transform.cloudwatch_api())
    stack = deploy_cfn_template(
        template_path=os.path.join(
            os.path.dirname(__file__), "../../../templates/cfn_cw_simple_alarm.yml"
        ),
    )
    alarm_name = stack.outputs["MetricAlarmName"]
    response = aws_client.cloudwatch.describe_alarms(AlarmNames=[alarm_name])
    snapshot.match("simple_alarm", response["MetricAlarms"])

    stack.destroy()
    response = aws_client.cloudwatch.describe_alarms(AlarmNames=[alarm_name])
    assert not response["MetricAlarms"]

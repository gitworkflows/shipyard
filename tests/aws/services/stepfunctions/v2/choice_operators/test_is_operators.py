import pytest

from shipyard.testing.aws.util import is_aws_cloud
from shipyard.testing.pytest import markers
from tests.aws.services.stepfunctions.v2.choice_operators.utils import (
    TYPE_COMPARISONS,
    create_and_test_comparison_function,
)

# TODO: test for validation errors, and boundary testing.


@markers.snapshot.skip_snapshot_verify(paths=["$..loggingConfiguration", "$..tracingConfiguration"])
class TestIsOperators:
    @markers.aws.validated
    def test_is_boolean(
        self, create_iam_role_for_sfn, create_state_machine, sfn_snapshot, aws_client
    ):
        create_and_test_comparison_function(
            aws_client.stepfunctions,
            create_iam_role_for_sfn,
            create_state_machine,
            sfn_snapshot,
            "IsBoolean",
            comparisons=TYPE_COMPARISONS,
        )

    @markers.aws.validated
    def test_is_null(self, create_iam_role_for_sfn, create_state_machine, sfn_snapshot, aws_client):
        create_and_test_comparison_function(
            aws_client.stepfunctions,
            create_iam_role_for_sfn,
            create_state_machine,
            sfn_snapshot,
            "IsNull",
            comparisons=TYPE_COMPARISONS,
        )

    @markers.aws.validated
    def test_is_numeric(
        self, create_iam_role_for_sfn, create_state_machine, sfn_snapshot, aws_client
    ):
        create_and_test_comparison_function(
            aws_client.stepfunctions,
            create_iam_role_for_sfn,
            create_state_machine,
            sfn_snapshot,
            "IsNumeric",
            comparisons=TYPE_COMPARISONS,
        )

    @markers.aws.validated
    def test_is_present(
        self, create_iam_role_for_sfn, create_state_machine, sfn_snapshot, aws_client
    ):
        create_and_test_comparison_function(
            aws_client.stepfunctions,
            create_iam_role_for_sfn,
            create_state_machine,
            sfn_snapshot,
            "IsPresent",
            comparisons=TYPE_COMPARISONS,
        )

    @markers.aws.validated
    def test_is_string(
        self, create_iam_role_for_sfn, create_state_machine, sfn_snapshot, aws_client
    ):
        create_and_test_comparison_function(
            aws_client.stepfunctions,
            create_iam_role_for_sfn,
            create_state_machine,
            sfn_snapshot,
            "IsString",
            comparisons=TYPE_COMPARISONS,
        )

    @pytest.mark.skipif(
        condition=not is_aws_cloud(), reason="TODO: investigate IsTimestamp behaviour."
    )
    @markers.aws.needs_fixing
    def test_is_timestamp(
        self, create_iam_role_for_sfn, create_state_machine, sfn_snapshot, aws_client
    ):
        create_and_test_comparison_function(
            aws_client.stepfunctions,
            create_iam_role_for_sfn,
            create_state_machine,
            sfn_snapshot,
            "IsTimestamp",
            comparisons=TYPE_COMPARISONS,
        )

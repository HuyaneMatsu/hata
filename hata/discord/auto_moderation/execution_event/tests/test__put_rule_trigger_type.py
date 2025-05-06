import vampytest

from ...rule import AutoModerationRuleTriggerType

from ..fields import put_rule_trigger_type


def test__put_rule_trigger_type():
    """
    Tests whether ``put_rule_trigger_type`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (
            AutoModerationRuleTriggerType.keyword,
            False,
            {'rule_trigger_type': AutoModerationRuleTriggerType.keyword.value},
        ),
    ):
        data = put_rule_trigger_type(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)

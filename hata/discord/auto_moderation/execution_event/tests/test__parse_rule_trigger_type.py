import vampytest

from ...rule import AutoModerationRuleTriggerType

from ..fields import parse_rule_trigger_type


def test__parse_rule_trigger_type():
    """
    Tests whether ``parse_rule_trigger_type`` works as intended.
    """
    for input_data, expected_output in (
        ({}, AutoModerationRuleTriggerType.none),
        ({'rule_trigger_type': AutoModerationRuleTriggerType.keyword.value}, AutoModerationRuleTriggerType.keyword),
    ):
        output = parse_rule_trigger_type(input_data)
        vampytest.assert_eq(output, expected_output)

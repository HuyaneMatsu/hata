import vampytest

from ...rule import AutoModerationRuleTriggerType

from ..fields import put_rule_trigger_type_into


def test__put_rule_trigger_type_into():
    """
    Tests whether ``put_rule_trigger_type_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (
            AutoModerationRuleTriggerType.keyword,
            False,
            {'rule_trigger_type': AutoModerationRuleTriggerType.keyword.value},
        ),
    ):
        data = put_rule_trigger_type_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)

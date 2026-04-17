import vampytest

from ...rule import AutoModerationRuleTriggerType

from ..fields import validate_rule_trigger_type


def test__validate_rule_trigger_type__0():
    """
    Tests whether `validate_rule_trigger_type` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (AutoModerationRuleTriggerType.keyword, AutoModerationRuleTriggerType.keyword),
        (AutoModerationRuleTriggerType.keyword.value, AutoModerationRuleTriggerType.keyword)
    ):
        output = validate_rule_trigger_type(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_rule_trigger_type__1():
    """
    Tests whether `validate_rule_trigger_type` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_rule_trigger_type(input_value)

import vampytest

from ..fields import validate_trigger_type
from ..preinstanced import AutoModerationRuleTriggerType


def test__validate_trigger_type():
    """
    Tests whether ``validate_trigger_type`` is working as intended.
    """
    for input_value, expected_output in (
        (AutoModerationRuleTriggerType.mention_spam,  AutoModerationRuleTriggerType.mention_spam),
        (AutoModerationRuleTriggerType.mention_spam.value,  AutoModerationRuleTriggerType.mention_spam),
    ):
        output = validate_trigger_type(input_value)
        vampytest.assert_eq(output, expected_output)


def test__parse_trigger_type__1():
    """
    Tests whether `parse_trigger_type` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_trigger_type(input_value)

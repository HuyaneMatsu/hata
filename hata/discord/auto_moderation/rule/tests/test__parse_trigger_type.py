import vampytest

from ..fields import parse_trigger_type
from ..preinstanced import AutoModerationRuleTriggerType


def test__parse_trigger_type__0():
    """
    Tests whether `parse_trigger_type` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        ({}, AutoModerationRuleTriggerType.none),
        ({'trigger_type': AutoModerationRuleTriggerType.mention_spam.value}, AutoModerationRuleTriggerType.mention_spam),
    ):
        output = parse_trigger_type(input_value)
        vampytest.assert_is(output, expected_output)

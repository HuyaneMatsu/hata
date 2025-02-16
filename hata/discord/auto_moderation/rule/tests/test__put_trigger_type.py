import vampytest

from ..fields import put_trigger_type
from ..preinstanced import AutoModerationRuleTriggerType


def test__put_trigger_type():
    """
    Tests whether ``put_trigger_type`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (AutoModerationRuleTriggerType.mention_spam, True, {'trigger_type': AutoModerationRuleTriggerType.mention_spam.value}),
    ):
        data = put_trigger_type(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)

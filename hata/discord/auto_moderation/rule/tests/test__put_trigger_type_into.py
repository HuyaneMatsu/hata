import vampytest

from ..fields import put_trigger_type_into
from ..preinstanced import AutoModerationRuleTriggerType


def test__put_trigger_type_into():
    """
    Tests whether ``put_trigger_type_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (AutoModerationRuleTriggerType.mention_spam, True, {'trigger_type': AutoModerationRuleTriggerType.mention_spam.value}),
    ):
        data = put_trigger_type_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)

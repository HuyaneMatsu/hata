import vampytest

from .. import AutoModerationActionExecutionEvent, AutoModerationActionType, AutoModerationRuleTriggerType


def get_base_payload():
    return {
        'action': {
            'type': AutoModerationActionType.block_message.value,
            'metadata': {},
        },
        'content': 'owo',
        'rule_id': '0',
        'rule_trigger_type': AutoModerationRuleTriggerType.keyword.value,
        'user_id': '0',
    }


def test__AutoModerationActionExecutionEvent__repr():
    """
    Tests whether ``AutoModerationActionExecutionEvent``'s `__repr__` method works as intended.
    """
    data = get_base_payload()
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_instance(repr(event), str)


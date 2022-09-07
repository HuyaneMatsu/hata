import vampytest

from .. import (
    AutoModerationActionExecutionEvent, AutoModerationActionType, AutoModerationRuleTriggerType, AutoModerationAction
)


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


class test__AutoModerationActionExecutionEvent__new():
    """
    Asserts whether `AutoModerationActionExecutionEvent` returns an instance of the correct type. 
    """
    data = get_base_payload()
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_instance(event, AutoModerationActionExecutionEvent)


class test__AutoModerationActionExecutionEvent__new__action():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct `.action` attribute.
    """
    data = get_base_payload()
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.action, AutoModerationAction(AutoModerationActionType.block_message.value))
    
    
class test__AutoModerationActionExecutionEvent__new__alert_system_message_id__0():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.alert_system_message_id` attribute.
    Case: '0'.
    """
    data = get_base_payload()
    data['alert_system_message_id'] = '0'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.alert_system_message_id, 0)


class test__AutoModerationActionExecutionEvent__new__alert_system_message_id__1():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.alert_system_message_id` attribute.
    Case: '69'
    """
    data = get_base_payload()
    data['alert_system_message_id'] = '69'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.alert_system_message_id, 69)


class test__AutoModerationActionExecutionEvent__new__alert_system_message_id__2():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.alert_system_message_id` attribute.
    Case: None
    """
    data = get_base_payload()
    data['alert_system_message_id'] = None
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.alert_system_message_id, 0)


class test__AutoModerationActionExecutionEvent__new__alert_system_message_id__3():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.alert_system_message_id` attribute.
    Case: *missing*
    """
    data = get_base_payload()
    data.pop('alert_system_message_id', None)
    
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.alert_system_message_id, 0)

    
class test__AutoModerationActionExecutionEvent__new__channel_id__0():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.channel_id` attribute.
    Case: '0'.
    """
    data = get_base_payload()
    data['channel_id'] = '0'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.channel_id, 0)


class test__AutoModerationActionExecutionEvent__new__channel_id__1():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.channel_id` attribute.
    Case: '69'
    """
    data = get_base_payload()
    data['channel_id'] = '69'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.channel_id, 69)


class test__AutoModerationActionExecutionEvent__new__channel_id__2():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.channel_id` attribute.
    Case: None
    """
    data = get_base_payload()
    data['channel_id'] = None
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.channel_id, 0)


class test__AutoModerationActionExecutionEvent__new__channel_id__3():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.channel_id` attribute.
    Case: *missing*
    """
    data = get_base_payload()
    data.pop('channel_id', None)
    
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.channel_id, 0)


class test__AutoModerationActionExecutionEvent__new__guild_id__0():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.guild_id` attribute.
    Case: '0'.
    """
    data = get_base_payload()
    data['guild_id'] = '0'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.guild_id, 0)


class test__AutoModerationActionExecutionEvent__new__guild_id__1():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.guild_id` attribute.
    Case: '69'
    """
    data = get_base_payload()
    data['guild_id'] = '69'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.guild_id, 69)


class test__AutoModerationActionExecutionEvent__new__guild_id__2():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.guild_id` attribute.
    Case: None
    """
    data = get_base_payload()
    data['guild_id'] = None
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.guild_id, 0)


class test__AutoModerationActionExecutionEvent__new__guild_id__3():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.guild_id` attribute.
    Case: *missing*
    """
    data = get_base_payload()
    data.pop('guild_id', None)
    
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.guild_id, 0)


class test__AutoModerationActionExecutionEvent__new__matched_content__0():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.matched_content` attribute.
    Case: None
    """
    data = get_base_payload()
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.matched_content, None)


class test__AutoModerationActionExecutionEvent__new__matched_content__1():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.matched_content` attribute.
    Case: ''
    """
    data = get_base_payload()
    data['matched_content'] = ''
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_is(event.matched_content, None)


class test__AutoModerationActionExecutionEvent__new__matched_content__2():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.matched_content` attribute.
    Case: 'owo'
    """
    data = get_base_payload()
    data['matched_content'] = 'owo'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.matched_content, 'owo')


class test__AutoModerationActionExecutionEvent__new__matched_content__3():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.matched_content` attribute.
    Case: *missing*
    """
    data = get_base_payload()
    
    data.pop('matched_content', None)
    
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_is(event.matched_content, None)


class test__AutoModerationActionExecutionEvent__new__matched_keyword__0():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.matched_keyword` attribute.
    Case: None
    """
    data = get_base_payload()
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.matched_keyword, None)


class test__AutoModerationActionExecutionEvent__new__matched_keyword__1():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.matched_keyword` attribute.
    Case: ''
    """
    data = get_base_payload()
    data['matched_keyword'] = ''
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_is(event.matched_keyword, None)


class test__AutoModerationActionExecutionEvent__new__matched_keyword__2():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.matched_keyword` attribute.
    Case: 'owo'
    """
    data = get_base_payload()
    data['matched_keyword'] = 'owo'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.matched_keyword, 'owo')


class test__AutoModerationActionExecutionEvent__new__matched_keyword__3():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.matched_keyword` attribute.
    Case: *missing*
    """
    data = get_base_payload()
    data.pop('matched_keyword', None)
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_is(event.matched_keyword, None)



class test__AutoModerationActionExecutionEvent__new__rule_id__0():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.rule_id` attribute.
    Case: '0'.
    """
    data = get_base_payload()
    data['rule_id'] = '0'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.rule_id, 0)


class test__AutoModerationActionExecutionEvent__new__rule_id__1():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.rule_id` attribute.
    Case: '69'
    """
    data = get_base_payload()
    data['rule_id'] = '69'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.rule_id, 69)


class test__AutoModerationActionExecutionEvent__new__rule_trigger_type():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.rule_trigger_type` attribute.
    """
    data = get_base_payload()
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_is(event.rule_trigger_type, AutoModerationRuleTriggerType.keyword)


class test__AutoModerationActionExecutionEvent__new__user_id__0():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.user_id` attribute.
    Case: '0'.
    """
    data = get_base_payload()
    data['user_id'] = '0'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.user_id, 0)


class test__AutoModerationActionExecutionEvent__new__user_id__1():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.user_id` attribute.
    Case: '69'
    """
    data = get_base_payload()
    data['user_id'] = '69'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.user_id, 69)

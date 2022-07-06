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


class test__AutoModerationActionExecutionEvent__constructor():
    """
    Asserts whether `AutoModerationActionExecutionEvent` returns an instance of the correct type. 
    """
    data = get_base_payload()
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_instance(event, AutoModerationActionExecutionEvent)


class test__AutoModerationActionExecutionEvent__constructor__action():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct `.action` attribute.
    """
    data = get_base_payload()
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.action, AutoModerationAction(AutoModerationActionType.block_message.value))
    
    
class test__AutoModerationActionExecutionEvent__constructor__alert_system_message_id_0():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.alert_system_message_id` attribute.
    Case: '0'.
    """
    data = get_base_payload()
    data['alert_system_message_id'] = '0'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.alert_system_message_id, 0)


class test__AutoModerationActionExecutionEvent__constructor__alert_system_message_id_1():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.alert_system_message_id` attribute.
    Case: '69'
    """
    data = get_base_payload()
    data['alert_system_message_id'] = '69'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.alert_system_message_id, 69)


class test__AutoModerationActionExecutionEvent__constructor__alert_system_message_id_2():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.alert_system_message_id` attribute.
    Case: None
    """
    data = get_base_payload()
    data['alert_system_message_id'] = None
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.alert_system_message_id, 0)


class test__AutoModerationActionExecutionEvent__constructor__alert_system_message_id_3():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.alert_system_message_id` attribute.
    Case: *missing*
    """
    data = get_base_payload()
    data.pop('alert_system_message_id', None)
    
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.alert_system_message_id, 0)

    
class test__AutoModerationActionExecutionEvent__constructor__channel_id_0():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.channel_id` attribute.
    Case: '0'.
    """
    data = get_base_payload()
    data['channel_id'] = '0'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.channel_id, 0)


class test__AutoModerationActionExecutionEvent__constructor__channel_id_1():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.channel_id` attribute.
    Case: '69'
    """
    data = get_base_payload()
    data['channel_id'] = '69'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.channel_id, 69)


class test__AutoModerationActionExecutionEvent__constructor__channel_id_2():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.channel_id` attribute.
    Case: None
    """
    data = get_base_payload()
    data['channel_id'] = None
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.channel_id, 0)


class test__AutoModerationActionExecutionEvent__constructor__channel_id_3():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.channel_id` attribute.
    Case: *missing*
    """
    data = get_base_payload()
    data.pop('channel_id', None)
    
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.channel_id, 0)


class test__AutoModerationActionExecutionEvent__constructor__guild_id_0():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.guild_id` attribute.
    Case: '0'.
    """
    data = get_base_payload()
    data['guild_id'] = '0'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.guild_id, 0)


class test__AutoModerationActionExecutionEvent__constructor__guild_id_1():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.guild_id` attribute.
    Case: '69'
    """
    data = get_base_payload()
    data['guild_id'] = '69'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.guild_id, 69)


class test__AutoModerationActionExecutionEvent__constructor__guild_id_2():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.guild_id` attribute.
    Case: None
    """
    data = get_base_payload()
    data['guild_id'] = None
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.guild_id, 0)


class test__AutoModerationActionExecutionEvent__constructor__guild_id_3():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.guild_id` attribute.
    Case: *missing*
    """
    data = get_base_payload()
    data.pop('guild_id', None)
    
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.guild_id, 0)


class test__AutoModerationActionExecutionEvent__constructor__matched_content_0():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.matched_content` attribute.
    Case: None
    """
    data = get_base_payload()
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.matched_content, None)


class test__AutoModerationActionExecutionEvent__constructor__matched_content_1():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.matched_content` attribute.
    Case: ''
    """
    data = get_base_payload()
    data['matched_content'] = ''
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_is(event.matched_content, None)


class test__AutoModerationActionExecutionEvent__constructor__matched_content_2():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.matched_content` attribute.
    Case: 'owo'
    """
    data = get_base_payload()
    data['matched_content'] = 'owo'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.matched_content, 'owo')


class test__AutoModerationActionExecutionEvent__constructor__matched_content_3():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.matched_content` attribute.
    Case: *missing*
    """
    data = get_base_payload()
    
    data.pop('matched_content', None)
    
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_is(event.matched_content, None)


class test__AutoModerationActionExecutionEvent__constructor__matched_keyword_0():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.matched_keyword` attribute.
    Case: None
    """
    data = get_base_payload()
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.matched_keyword, None)


class test__AutoModerationActionExecutionEvent__constructor__matched_keyword_1():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.matched_keyword` attribute.
    Case: ''
    """
    data = get_base_payload()
    data['matched_keyword'] = ''
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_is(event.matched_keyword, None)


class test__AutoModerationActionExecutionEvent__constructor__matched_keyword_2():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.matched_keyword` attribute.
    Case: 'owo'
    """
    data = get_base_payload()
    data['matched_keyword'] = 'owo'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.matched_keyword, 'owo')


class test__AutoModerationActionExecutionEvent__constructor__matched_keyword_3():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.matched_keyword` attribute.
    Case: *missing*
    """
    data = get_base_payload()
    data.pop('matched_keyword', None)
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_is(event.matched_keyword, None)



class test__AutoModerationActionExecutionEvent__constructor__rule_id_0():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.rule_id` attribute.
    Case: '0'.
    """
    data = get_base_payload()
    data['rule_id'] = '0'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.rule_id, 0)


class test__AutoModerationActionExecutionEvent__constructor__rule_id_1():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.rule_id` attribute.
    Case: '69'
    """
    data = get_base_payload()
    data['rule_id'] = '69'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.rule_id, 69)


class test__AutoModerationActionExecutionEvent__constructor__rule_trigger_type():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.rule_trigger_type` attribute.
    """
    data = get_base_payload()
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_is(event.rule_trigger_type, AutoModerationRuleTriggerType.keyword)


class test__AutoModerationActionExecutionEvent__constructor__user_id_0():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.user_id` attribute.
    Case: '0'.
    """
    data = get_base_payload()
    data['user_id'] = '0'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.user_id, 0)


class test__AutoModerationActionExecutionEvent__constructor__user_id_1():
    """
    Asserts whether `AutoModerationActionExecutionEvent` creates an instance with correct
    `.user_id` attribute.
    Case: '69'
    """
    data = get_base_payload()
    data['user_id'] = '69'
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_eq(event.user_id, 69)

import vampytest

from ...action import AutoModerationAction
from ...rule import AutoModerationRuleTriggerType

from ..execution_event import AutoModerationActionExecutionEvent


def test__AutoModerationActionExecutionEvent__repr():
    """
    Tests whether ``AutoModerationActionExecutionEvent.__repr__`` works as intended.
    """
    action = AutoModerationAction(duration = 69)
    alert_system_message_id = 202211160015
    channel_id = 202211160016
    content = 'Teary'
    guild_id = 202211160017
    matched_content = 'Blood'
    matched_keyword = 'OTOMEKAN'
    rule_id = 202211160018
    rule_trigger_type = AutoModerationRuleTriggerType.keyword
    user_id = 202211160019
    
    event = AutoModerationActionExecutionEvent(
        action = action,
        alert_system_message_id = alert_system_message_id,
        channel_id = channel_id,
        content = content,
        guild_id = guild_id,
        matched_content = matched_content,
        matched_keyword = matched_keyword,
        rule_id = rule_id,
        rule_trigger_type = rule_trigger_type,
        user_id = user_id,
    )
    
    vampytest.assert_instance(repr(event), str)


def test__AutoModerationActionExecutionEvent__hash():
    """
    Tests whether ``AutoModerationActionExecutionEvent.__hash__`` works as intended.
    """
    action = AutoModerationAction(duration = 69)
    alert_system_message_id = 202211160020
    channel_id = 202211160021
    content = 'Teary'
    guild_id = 202211160022
    matched_content = 'Blood'
    matched_keyword = 'OTOMEKAN'
    rule_id = 202211160023
    rule_trigger_type = AutoModerationRuleTriggerType.keyword
    user_id = 202211160024
    
    event = AutoModerationActionExecutionEvent(
        action = action,
        alert_system_message_id = alert_system_message_id,
        channel_id = channel_id,
        content = content,
        guild_id = guild_id,
        matched_content = matched_content,
        matched_keyword = matched_keyword,
        rule_id = rule_id,
        rule_trigger_type = rule_trigger_type,
        user_id = user_id,
    )
    
    vampytest.assert_instance(hash(event), int)


def test__AutoModerationActionExecutionEvent__eq():
    """
    Tests whether ``AutoModerationActionExecutionEvent.__hash__`` works as intended.
    """
    action = AutoModerationAction(duration = 69)
    alert_system_message_id = 202211160020
    channel_id = 202211160021
    content = 'Teary'
    guild_id = 202211160022
    matched_content = 'Blood'
    matched_keyword = 'OTOMEKAN'
    rule_id = 202211160023
    rule_trigger_type = AutoModerationRuleTriggerType.keyword
    user_id = 202211160024
    
    keyword_parameters = {
        'action': action,
        'alert_system_message_id': alert_system_message_id,
        'channel_id': channel_id,
        'content': content,
        'guild_id': guild_id,
        'matched_content': matched_content,
        'matched_keyword': matched_keyword,
        'rule_id': rule_id,
        'rule_trigger_type': rule_trigger_type,
        'user_id': user_id,
    }
    
    event = AutoModerationActionExecutionEvent(**keyword_parameters)
    
    vampytest.assert_eq(event, event)
    vampytest.assert_ne(event, object())
    
    for field_name, field_value in (
        ('action', AutoModerationAction(channel_id = 202211160030)),
        ('alert_system_message_id', 202211160025),
        ('channel_id', 202211160026),
        ('content', 'a'),
        ('guild_id', 202211160027),
        ('matched_content', 'b'),
        ('matched_keyword', 'd'), # the missing "c" causes massive emotion damage
        ('rule_id', 202211160028),
        ('rule_trigger_type', AutoModerationRuleTriggerType.spam),
        ('user_id', 202211160029),
    ):
        test_event = AutoModerationActionExecutionEvent(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(event, test_event)


def test__AutoModerationActionExecutionEvent__unpack():
    """
    Tests whether ``AutoModerationActionExecutionEvent`` unpacking works as intended.
    """
    action = AutoModerationAction(duration = 69)
    alert_system_message_id = 202211160030
    channel_id = 202211160031
    content = 'Teary'
    guild_id = 202211160032
    matched_content = 'Blood'
    matched_keyword = 'OTOMEKAN'
    rule_id = 202211160033
    rule_trigger_type = AutoModerationRuleTriggerType.keyword
    user_id = 202211160034
    
    event = AutoModerationActionExecutionEvent(
        action = action,
        alert_system_message_id = alert_system_message_id,
        channel_id = channel_id,
        content = content,
        guild_id = guild_id,
        matched_content = matched_content,
        matched_keyword = matched_keyword,
        rule_id = rule_id,
        rule_trigger_type = rule_trigger_type,
        user_id = user_id,
    )
    
    vampytest.assert_eq(len([*event]), len(event))

import vampytest

from ...action import AutoModerationAction
from ...rule import AutoModerationRuleTriggerType

from ..execution_event import AutoModerationActionExecutionEvent

from .test__AutoModerationActionExecutionEvent__constructor import _assert_fields_set


def test__AutoModerationActionExecutionEvent__from_data():
    """
    Tests whether ``AutoModerationActionExecutionEvent.from_data`` works as intended.
    """
    action = AutoModerationAction(duration = 69)
    alert_system_message_id = 202211160047
    channel_id = 202211160048
    content = 'Teary'
    guild_id = 202211160049
    matched_content = 'Blood'
    matched_keyword = 'OTOMEKAN'
    rule_id = 202211160050
    rule_trigger_type = AutoModerationRuleTriggerType.keyword
    user_id = 202211160051
    
    data = {
        'action': action.to_data(defaults = True),
        'alert_system_message_id': str(alert_system_message_id),
        'channel_id': str(channel_id),
        'content': content,
        'guild_id': str(guild_id),
        'matched_content': matched_content,
        'matched_keyword': matched_keyword,
        'rule_id': str(rule_id),
        'rule_trigger_type': rule_trigger_type.value,
        'user_id': str(user_id),
    }
    
    event = AutoModerationActionExecutionEvent.from_data(data)
    _assert_fields_set(event)

    vampytest.assert_eq(event.action, action)
    vampytest.assert_eq(event.alert_system_message_id, alert_system_message_id)
    vampytest.assert_eq(event.channel_id, channel_id)
    vampytest.assert_eq(event.guild_id, guild_id)
    vampytest.assert_eq(event.matched_content, matched_content)
    vampytest.assert_eq(event.matched_keyword, matched_keyword)
    vampytest.assert_eq(event.rule_id, rule_id)
    vampytest.assert_is(event.rule_trigger_type, rule_trigger_type)
    vampytest.assert_eq(event.user_id, user_id)



def test__AutoModerationActionExecutionEvent__to_data():
    """
    Tests whether ``AutoModerationActionExecutionEvent.to_data`` works as intended.
    
    Case: include defaults.
    """
    action = AutoModerationAction(duration = 69)
    alert_system_message_id = 202211160052
    channel_id = 202211160053
    content = 'Teary'
    guild_id = 202211160054
    matched_content = 'Blood'
    matched_keyword = 'OTOMEKAN'
    rule_id = 202211160055
    rule_trigger_type = AutoModerationRuleTriggerType.keyword
    user_id = 202211160056
    
    
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
    
    expected_data = {
        'action': action.to_data(defaults = True),
        'alert_system_message_id': str(alert_system_message_id),
        'channel_id': str(channel_id),
        'content': content,
        'guild_id': str(guild_id),
        'matched_content': matched_content,
        'matched_keyword': matched_keyword,
        'rule_id': str(rule_id),
        'rule_trigger_type': rule_trigger_type.value,
        'user_id': str(user_id),
    }
    
    vampytest.assert_eq(
        event.to_data(
            defaults = True,
        ),
        expected_data,
    )

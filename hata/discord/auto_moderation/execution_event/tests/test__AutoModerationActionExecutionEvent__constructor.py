import vampytest

from ...action import AutoModerationAction
from ...rule import AutoModerationRuleTriggerType

from ..execution_event import AutoModerationActionExecutionEvent


def _assert_is_every_attribute_set(event):
    """
    Asserts whether every attributes are set of the given event.
    
    Parameters
    ----------
    event : ``AutoModerationActionExecutionEvent``
        the event to check.
    """
    vampytest.assert_instance(event, AutoModerationActionExecutionEvent)
    vampytest.assert_instance(event.alert_system_message_id, int)
    vampytest.assert_instance(event.channel_id, int)
    vampytest.assert_instance(event.content, str, nullable = True)
    vampytest.assert_instance(event.guild_id, int)
    vampytest.assert_instance(event.matched_content, str, nullable = True)
    vampytest.assert_instance(event.matched_keyword, str, nullable = True)
    vampytest.assert_instance(event.rule_id, int)
    vampytest.assert_instance(event.rule_trigger_type, AutoModerationRuleTriggerType)
    vampytest.assert_instance(event.user_id, int)


def test__AutoModerationActionExecutionEvent__new__0():
    """
    Tests whether ``AutoModerationActionExecutionEvent.__new__`` works as intended.
    
    Case: No parameters.
    """
    event = AutoModerationActionExecutionEvent()
    _assert_is_every_attribute_set(event)


def test__AutoModerationActionExecutionEvent__new__1():
    """
    Tests whether ``AutoModerationActionExecutionEvent.__new__`` works as intended.
    
    Case: ALL parameters.
    """
    action = AutoModerationAction(duration = 69)
    alert_system_message_id = 202211160042
    channel_id = 202211160043
    content = 'Teary'
    guild_id = 202211160044
    matched_content = 'Blood'
    matched_keyword = 'OTOMEKAN'
    rule_id = 202211160045
    rule_trigger_type = AutoModerationRuleTriggerType.keyword
    user_id = 202211160046
    
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
    
    _assert_is_every_attribute_set(event)
    
    vampytest.assert_eq(event.action, action)
    vampytest.assert_eq(event.alert_system_message_id, alert_system_message_id)
    vampytest.assert_eq(event.channel_id, channel_id)
    vampytest.assert_eq(event.guild_id, guild_id)
    vampytest.assert_eq(event.matched_content, matched_content)
    vampytest.assert_eq(event.matched_keyword, matched_keyword)
    vampytest.assert_eq(event.rule_id, rule_id)
    vampytest.assert_is(event.rule_trigger_type, rule_trigger_type)
    vampytest.assert_eq(event.user_id, user_id)

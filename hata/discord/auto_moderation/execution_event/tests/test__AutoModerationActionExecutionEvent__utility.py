import vampytest

from ....channel import Channel
from ....guild import Guild
from ....message import Message
from ....user import User

from ...action import AutoModerationAction
from ...rule import AutoModerationRule
from ...rule import AutoModerationRuleTriggerType

from ..execution_event import AutoModerationActionExecutionEvent

from .test__AutoModerationActionExecutionEvent__constructor import _assert_fields_set


def test__AutoModerationActionExecutionEvent__channel():
    """
    Tests whether ``AutoModerationActionExecutionEvent.channel`` works as intended.
    """
    channel_id = 202211160035
    
    for field_value, expected_output in (
        (0, None),
        (channel_id, Channel.precreate(channel_id)),
    ):
        event = AutoModerationActionExecutionEvent(channel_id = field_value)
        vampytest.assert_is(event.channel, expected_output)


def test__AutoModerationActionExecutionEvent__guild():
    """
    Tests whether ``AutoModerationActionExecutionEvent.guild`` works as intended.
    Case: None
    """
    guild_id = 202211160036
    
    for field_value, expected_output in (
        (0, None),
        (guild_id, Guild.precreate(guild_id)),
        (202211160037, None),
    ):
        event = AutoModerationActionExecutionEvent(guild_id = field_value)
        vampytest.assert_is(event.guild, expected_output)


def test__AutoModerationActionExecutionEvent__user():
    """
    Tests whether ``AutoModerationActionExecutionEvent.user`` works as intended.
    """
    user_id = 202211160038
    
    for field_value, expected_output in (
        (user_id, User.precreate(user_id)),
    ):
        event = AutoModerationActionExecutionEvent(user_id = field_value)
        vampytest.assert_is(event.user, expected_output)


def test__AutoModerationActionExecutionEvent__alert_system_message():
    """
    Tests whether ``AutoModerationActionExecutionEvent.alert_system_message`` unpacking works as intended.
    """
    alert_system_message_id = 202211160039
    
    for field_value, expected_output in (
        (0, None),
        (alert_system_message_id, Message.precreate(alert_system_message_id)),
    ):
        event = AutoModerationActionExecutionEvent(alert_system_message_id = field_value)
        vampytest.assert_is(event.alert_system_message, expected_output)


def test__AutoModerationActionExecutionEvent__rule():
    """
    Tests whether ``AutoModerationActionExecutionEvent.rule`` unpacking works as intended.
    """
    rule_id = 202211160040
    
    for field_value, expected_output in (
        (0, None),
        (202211160041, None),
        (rule_id, AutoModerationRule.precreate(rule_id)),
    ):
        event = AutoModerationActionExecutionEvent(rule_id = field_value)
        vampytest.assert_is(event.rule, expected_output)


def test__AutoModerationActionExecutionEvent__copy():
    """
    Tests whether ``AutoModerationActionExecutionEvent.copy`` works as intended.
    """
    action = AutoModerationAction(duration = 69)
    alert_system_message_id = 202211170000
    channel_id = 202211170001
    content = 'Teary'
    guild_id = 202211170002
    matched_content = 'Blood'
    matched_keyword = 'OTOMEKAN'
    rule_id = 202211170003
    rule_trigger_type = AutoModerationRuleTriggerType.keyword
    user_id = 202211170004
    
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
    
    copy = event.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, event)
    vampytest.assert_is_not(copy, event)


def test__AutoModerationActionExecutionEvent__copy_with__0():
    """
    Tests whether ``AutoModerationActionExecutionEvent.copy_with`` works as intended.
    
    Case: No fields given.
    """
    action = AutoModerationAction(duration = 69)
    alert_system_message_id = 202211170005
    channel_id = 202211170006
    content = 'Teary'
    guild_id = 202211170007
    matched_content = 'Blood'
    matched_keyword = 'OTOMEKAN'
    rule_id = 202211170008
    rule_trigger_type = AutoModerationRuleTriggerType.keyword
    user_id = 202211170009
    
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
    
    copy = event.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, event)
    vampytest.assert_is_not(copy, event)


def test__AutoModerationActionExecutionEvent__copy_with__1():
    """
    Tests whether ``AutoModerationActionExecutionEvent.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_action = AutoModerationAction(duration = 69)
    new_action = AutoModerationAction(channel_id = 202211170010)
    old_alert_system_message_id = 202211170011
    new_alert_system_message_id = 202211170012
    old_channel_id = 202211170013
    new_channel_id = 202211170014
    old_content = 'Teary'
    new_content = 'hanatan'
    old_guild_id = 202211170015
    new_guild_id = 202211170016
    old_matched_content = 'Blood'
    new_matched_content = 'maji'
    old_matched_keyword = 'OTOMEKAN'
    new_matched_keyword = 'tenshi'
    old_rule_id = 202211170017
    new_rule_id = 202211170018
    old_rule_trigger_type = AutoModerationRuleTriggerType.keyword
    new_rule_trigger_type = AutoModerationRuleTriggerType.mention_spam
    old_user_id = 202211170019
    new_user_id = 202211170020
    
    event = AutoModerationActionExecutionEvent(
        action = old_action,
        alert_system_message_id = old_alert_system_message_id,
        channel_id = old_channel_id,
        content = old_content,
        guild_id = old_guild_id,
        matched_content = old_matched_content,
        matched_keyword = old_matched_keyword,
        rule_id = old_rule_id,
        rule_trigger_type = old_rule_trigger_type,
        user_id = old_user_id,
    )
    
    copy = event.copy_with(
        action = new_action,
        alert_system_message_id = new_alert_system_message_id,
        channel_id = new_channel_id,
        content = new_content,
        guild_id = new_guild_id,
        matched_content = new_matched_content,
        matched_keyword = new_matched_keyword,
        rule_id = new_rule_id,
        rule_trigger_type = new_rule_trigger_type,
        user_id = new_user_id,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, event)

    vampytest.assert_eq(copy.action, new_action)
    vampytest.assert_eq(copy.alert_system_message_id, new_alert_system_message_id)
    vampytest.assert_eq(copy.channel_id, new_channel_id)
    vampytest.assert_eq(copy.guild_id, new_guild_id)
    vampytest.assert_eq(copy.matched_content, new_matched_content)
    vampytest.assert_eq(copy.matched_keyword, new_matched_keyword)
    vampytest.assert_eq(copy.rule_id, new_rule_id)
    vampytest.assert_is(copy.rule_trigger_type, new_rule_trigger_type)
    vampytest.assert_eq(copy.user_id, new_user_id)

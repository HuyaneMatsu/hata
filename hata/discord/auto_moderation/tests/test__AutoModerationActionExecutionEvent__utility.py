import vampytest

from ...channel import Channel
from ...guild import Guild
from ...user import ClientUserBase, User

from .. import (
    AutoModerationActionExecutionEvent, AutoModerationActionType, AutoModerationRuleTriggerType
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


def test__AutoModerationActionExecutionEvent__channel__0():
    """
    Tests whether ``AutoModerationActionExecutionEvent``'s `channel` property works as intended.
    Case: None
    """
    data = get_base_payload()
    data['channel_id'] = None
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_is(event.channel, None)



def test__AutoModerationActionExecutionEvent__channel__1():
    """
    Tests whether ``AutoModerationActionExecutionEvent``'s `channel` property works as intended.
    Case: Channel.precreate(69)
    """
    data = get_base_payload()
    data['channel_id'] = '69'
    event = AutoModerationActionExecutionEvent(data)
    channel = Channel.precreate(69)
    
    vampytest.assert_instance(event.channel, Channel)
    vampytest.assert_is(event.channel, channel)


def test__AutoModerationActionExecutionEvent__guild__0():
    """
    Tests whether ``AutoModerationActionExecutionEvent``'s `guild` property works as intended.
    Case: None
    """
    data = get_base_payload()
    data['guild_id'] = None
    event = AutoModerationActionExecutionEvent(data)
    
    vampytest.assert_is(event.guild, None)


def test__AutoModerationActionExecutionEvent__guild__1():
    """
    Tests whether ``AutoModerationActionExecutionEvent``'s `guild` property works as intended.
    Case: Guild.precreate(69)
    """
    data = get_base_payload()
    data['guild_id'] = '69'
    event = AutoModerationActionExecutionEvent(data)
    guild = Guild.precreate(69)
    
    vampytest.assert_instance(event.guild, Guild)
    vampytest.assert_is(event.guild, guild)



def test__AutoModerationActionExecutionEvent__user():
    """
    Tests whether ``AutoModerationActionExecutionEvent``'s `user` property works as intended.
    Case: User.precreate(69)
    """
    data = get_base_payload()
    data['user_id'] = '69'
    event = AutoModerationActionExecutionEvent(data)
    user = User.precreate(69)
    
    vampytest.assert_instance(event.user, ClientUserBase)
    vampytest.assert_is(event.user, user)

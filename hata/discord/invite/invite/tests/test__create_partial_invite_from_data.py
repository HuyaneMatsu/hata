import vampytest

from ..invite import Invite
from ..utils import create_partial_invite_from_data


def test__create_partial_invite_from_data__new():
    """
    Tests whether ``create_partial_invite_from_data`` works as intended.
    
    Case: new.
    """
    code = '202308060000'
    channel_id = 202308060001
    guild_id = 202308060002
    
    data = {
        'code': code,
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
    }
    
    invite = create_partial_invite_from_data(data)
    
    vampytest.assert_instance(invite, Invite)
    vampytest.assert_eq(invite.code, code)
    vampytest.assert_eq(invite.channel_id, channel_id)
    vampytest.assert_eq(invite.guild_id, guild_id)


def test__create_partial_invite_from_data__cache():
    """
    Tests whether ``create_partial_invite_from_data`` works as intended.
    
    Case: Caching.
    """
    code = '202308060003'
    
    data = {
        'code': code,
    }
    
    invite = create_partial_invite_from_data(data)
    test_invite = create_partial_invite_from_data(data)
    
    vampytest.assert_is(invite, test_invite)

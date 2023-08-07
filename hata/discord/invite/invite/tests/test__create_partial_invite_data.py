import vampytest

from ....channel import Channel
from ....guild import Guild

from ..invite import Invite
from ..utils import create_partial_invite_data


def test__create_partial_invite_data():
    """
    Tests whether ``create_partial_invite_data`` works as intended.
    """
    code = '202308060004'
    channel_id = 202308060005
    guild_id = 202308060006
    
    invite = Invite.precreate(
        code,
        channel = Channel.precreate(channel_id),
        guild = Guild.precreate(guild_id),
    )
    
    expected_output = {
        'code': code,
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
    }
    
    vampytest.assert_eq(
        create_partial_invite_data(invite),
        expected_output,
    )

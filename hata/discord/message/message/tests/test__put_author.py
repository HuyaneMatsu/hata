import vampytest

from ....user import GuildProfile, User
from ....webhook import Webhook

from ..fields import put_author


def test__put_author__user():
    """
    Tests whether ``put_author`` works as intended.
    
    Case: user.
    """
    user_id = 202304280043
    name = 'Keine'
    
    user = User.precreate(user_id, name = name)
    
    expected_output = {
        'author': user.to_data(defaults = True, include_internals = True),
        'webhook_id': None,
    }
    
    output = put_author(user, {}, True)
    vampytest.assert_eq(output, expected_output)


def test__put_author__user__guild_profile():
    """
    Tests whether ``put_author`` works as intended.
    
    Case: user.
    """
    user_id = 202304280044
    guild_id = 202304280045
    name = 'Keine'
    nick = 'oni'
    
    user = User.precreate(user_id, name = name)
    guild_profile = GuildProfile(nick = nick)
    user.guild_profiles[guild_id] = guild_profile
    
    expected_output = {
        'author': user.to_data(defaults = True, include_internals = True),
        'member': guild_profile.to_data(defaults = True, include_internals = True),
        'webhook_id': None,
    }
    
    output = put_author(user, {}, True, guild_id = guild_id)
    vampytest.assert_eq(output, expected_output)


def test__put_author__webhook():
    """
    Tests whether ``put_author`` works as intended.
    
    Case: user.
    """
    user_id = 202304280046
    name = 'Keine'
    
    user = Webhook.precreate(user_id, name = name)
    
    expected_output = {
        'author': user.to_data(defaults = True, include_internals = True),
        'webhook_id': str(user_id),
    }
    
    output = put_author(user, {}, True)
    vampytest.assert_eq(output, expected_output)

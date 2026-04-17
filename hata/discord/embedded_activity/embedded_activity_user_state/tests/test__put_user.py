import vampytest

from ....user import GuildProfile, User

from ..fields import put_user


def test__put_user__user():
    """
    Tests whether ``put_user`` works as intended.
    
    Case: user.
    """
    user_id = 202409010006
    user = User.precreate(user_id)
    
    
    expected_output = {
        'user_id': str(user_id),
    }
    
    vampytest.assert_eq(
        put_user(user, {}, True),
        expected_output,
    )


def test__put_user__user_and_guild():
    """
    Tests whether ``put_user`` works as intended.
    
    Case: user & guild_id.
    """
    user_id = 202409010007
    guild_id = 202409010008
    
    user = User.precreate(user_id)
    
    
    expected_output = {
        'user_id': str(user_id),
    }
    
    vampytest.assert_eq(
        put_user(user, {}, True, guild_id = guild_id),
        expected_output,
    )


def test__put_user__user_and_guild_id_and_guild_profile():
    """
    Tests whether ``put_user`` works as intended.
    
    Case: user & guild_id & guild_profile.
    """
    user_id = 202409010009
    guild_id = 202409010010
    
    user = User.precreate(user_id)
    guild_profile = GuildProfile(nick = 'sinker')
    user.guild_profiles[guild_id] = guild_profile
    
    expected_output = {
        'user_id': str(user_id),
        'member': {
            **guild_profile.to_data(
                defaults = True,
                include_internals = True,
            ),
            'user': user.to_data(
                defaults = True,
                include_internals = True,
            )
        }
    }
    
    vampytest.assert_eq(
        put_user(user, {}, True, guild_id = guild_id),
        expected_output,
    )

def test__put_user__user_and_guild_profile():
    """
    Tests whether ``put_user`` works as intended.
    
    Case: user & guild_profile.
    """
    user_id = 202409010011
    
    user = User.precreate(user_id)
    
    expected_output = {
        'user_id': str(user_id),
    }
    
    vampytest.assert_eq(
        put_user(user, {}, True),
        expected_output,
    )

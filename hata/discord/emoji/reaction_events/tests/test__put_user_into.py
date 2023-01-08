import vampytest

from ....user import GuildProfile, User

from ..fields import put_user_into


def test__put_user_into__0():
    """
    Tests whether ``put_user-into`` works as intended.
    
    Case: user.
    """
    user_id = 202301020006
    user = User.precreate(user_id)
    
    
    expected_output = {
        'user_id': str(user_id),
    }
    
    vampytest.assert_eq(
        put_user_into(user, {}, True),
        expected_output,
    )


def test__put_user_into__1():
    """
    Tests whether ``put_user-into`` works as intended.
    
    Case: user & guild_id.
    """
    user_id = 202301020007
    guild_id = 202301020008
    
    user = User.precreate(user_id)
    
    
    expected_output = {
        'user_id': str(user_id),
    }
    
    vampytest.assert_eq(
        put_user_into(user, {}, True, guild_id = guild_id),
        expected_output,
    )


def test__put_user_into__2():
    """
    Tests whether ``put_user-into`` works as intended.
    
    Case: user & guild_id & guild_profile.
    """
    user_id = 202301020009
    guild_id = 202301020010
    
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
        put_user_into(user, {}, True, guild_id = guild_id),
        expected_output,
    )

def test__put_user_into__3():
    """
    Tests whether ``put_user-into`` works as intended.
    
    Case: user & guild_profile.
    """
    user_id = 202301020011
    
    user = User.precreate(user_id)
    
    expected_output = {
        'user_id': str(user_id),
    }
    
    vampytest.assert_eq(
        put_user_into(user, {}, True),
        expected_output,
    )

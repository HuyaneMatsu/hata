import vampytest

from ....user import ClientUserBase, GuildProfile, User

from ..fields import parse_user


def test__parse_user__user_id():
    """
    Tests whether ``parse_user`` works as intended.
    
    Case: user_id.
    """
    user_id = 202301020000
    
    data = {
        'user_id': str(user_id),
    }
    
    user = parse_user(data)
    
    vampytest.assert_instance(user, ClientUserBase)
    vampytest.assert_eq(user.id, user_id)
    vampytest.assert_eq(user.guild_profiles, {})


def test__parse_user__user_id_and_guild_id():
    """
    Tests whether ``parse_user`` works as intended.
    
    Case: user_id & guild_id.
    """
    user_id = 202301020001
    guild_id = 202301020002
    
    data = {
        'user_id': str(user_id),
    }
    
    user = parse_user(data, guild_id)
    
    vampytest.assert_instance(user, ClientUserBase)
    vampytest.assert_eq(user.id, user_id)
    vampytest.assert_eq(user.guild_profiles, {})


def test__parse_user__user_id_and_guild_id_and_member():
    """
    Tests whether ``parse_user`` works as intended.
    
    Case: user_id & guild_id & member.
    """
    user_id = 202301020003
    guild_id = 202301020004
    
    user = User.precreate(user_id)
    guild_profile = GuildProfile(nick = 'sinker')
    
    data = {
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
    
    user = parse_user(data, guild_id)
    
    vampytest.assert_instance(user, ClientUserBase)
    vampytest.assert_eq(user.id, user_id)
    vampytest.assert_eq(user.guild_profiles, {guild_id: guild_profile})


def test__parse_user__user_id_and_member():
    """
    Tests whether ``parse_user`` works as intended.
    
    Case: user_id & member.
    """
    user_id = 202301020005
    
    user = User.precreate(user_id)
    guild_profile = GuildProfile(nick = 'sinker')
    
    data = {
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
    
    user = parse_user(data)
    
    vampytest.assert_instance(user, ClientUserBase)
    vampytest.assert_eq(user.id, user_id)
    vampytest.assert_eq(user.guild_profiles, {})

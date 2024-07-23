import vampytest

from ...bases import Icon, IconType
from ...user import GuildProfile, User
from ...utils import is_url

from ..urls import CDN_ENDPOINT, user_avatar_url_at_as


def _iter_options():
    guild_id = 202407160062
    
    user_id = 202407160063
    user = User.precreate(user_id)
    
    yield (
        user,
        guild_id,
        {},
        f'{CDN_ENDPOINT}/embed/avatars/5.png',
    )
    
    user_id = 202407160064
    user = User.precreate(user_id, avatar = Icon(IconType.static, 2))
    
    yield (
        user,
        guild_id,
        {},
        f'{CDN_ENDPOINT}/avatars/{user_id}/00000000000000000000000000000002.png',
    )
    
    user_id = 202407160065
    user = User.precreate(user_id, avatar = Icon(IconType.static, 2))
    
    yield (
        user,
        guild_id,
        {'size': 1024, 'ext': 'jpg'},
        f'{CDN_ENDPOINT}/avatars/{user_id}/00000000000000000000000000000002.jpg?size=1024',
    )
    
    user_id = 202407160066
    user = User.precreate(user_id)
    
    yield (
        user,
        guild_id,
        {'size': 1024, 'ext': 'jpg'},
        f'{CDN_ENDPOINT}/embed/avatars/5.png',
    )
    
    user_id = 202407160067
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile(avatar = None)
    
    yield (
        user,
        guild_id,
        {},
        f'{CDN_ENDPOINT}/embed/avatars/5.png',
    )
    
    user_id = 202407160068
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile(avatar = Icon(IconType.static, 2))
    
    yield (
        user,
        guild_id,
        {},
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/avatars/00000000000000000000000000000002.png',
    )
    
    user_id = 202407160069
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile(avatar = Icon(IconType.animated, 3))
    
    yield (
        user,
        guild_id,
        {},
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/avatars/a_00000000000000000000000000000003.gif',
    )
    
    user_id = 202407160070
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile(avatar = Icon(IconType.static, 2))
    
    yield (
        user,
        guild_id,
        {'size': 1024},
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/avatars/00000000000000000000000000000002.png?size=1024',
    )
    
    user_id = 202407160071
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile(avatar = Icon(IconType.static, 2))
    
    yield (
        user,
        guild_id,
        {'size': 1024, 'ext': 'jpg'},
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/avatars/00000000000000000000000000000002.jpg?size=1024',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__user_avatar_url_at_as(user, guild_id, keyword_parameters):
    """
    Tests whether ``user_avatar_url_at_as`` works as intended.
    
    Parameters
    ----------
    user : ``User``
        User to get its avatar url of.
    guild_id : `int`
        The respective guild's identifier.
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    output : `None | str`
    """
    output = user_avatar_url_at_as(user, guild_id, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output

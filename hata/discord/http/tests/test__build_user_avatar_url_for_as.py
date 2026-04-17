import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_user_avatar_url_for_as


def _iter_options():
    guild_id = 202407160029
    
    user_id = 202407160030
    yield (
        user_id,
        guild_id,
        IconType.none,
        0,
        None,
        None,
        None,
    )
    
    user_id = 202407160033
    yield (
        user_id,
        guild_id,
        IconType.static,
        2,
        None,
        None,
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/avatars/00000000000000000000000000000002.png',
    )
    
    user_id = 202407160034
    yield (
        user_id,
        guild_id,
        IconType.animated,
        3,
        None,
        None,
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/avatars/a_00000000000000000000000000000003.gif',
    )
    
    user_id = 202407160035
    yield (
        user_id,
        guild_id,
        IconType.static,
        2,
        None,
        1024,
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/avatars/00000000000000000000000000000002.png?size=1024',
    )
    
    user_id = 202407160036
    yield (
        user_id,
        guild_id,
        IconType.static,
        2,
        'jpg',
        1024,
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/avatars/00000000000000000000000000000002.jpg?size=1024',
    )
    
    user_id = 202506210024
    yield (
        user_id,
        guild_id,
        IconType.static,
        4,
        'webp',
        None,
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/avatars/00000000000000000000000000000004.webp',
    )
    
    user_id = 202506210025
    yield (
        user_id,
        guild_id,
        IconType.animated,
        4,
        'webp',
        None,
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/avatars/a_00000000000000000000000000000004.webp?animated=true',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_user_avatar_url_for_as(user_id, guild_id, icon_type, icon_hash, ext, size):
    """
    Tests whether ``build_user_avatar_url_for_as`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    guild_id : `int`
        The guild's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_user_avatar_url_for_as(user_id, guild_id, icon_type, icon_hash, ext, size)
    vampytest.assert_instance(output, str, nullable = True)
    return output

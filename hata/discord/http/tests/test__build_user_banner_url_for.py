import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_user_banner_url_for


def _iter_options():
    guild_id = 202407160024
    
    user_id = 202407160025
    yield (
        user_id,
        guild_id,
        IconType.none,
        0,
        None,
    )
    
    user_id = 202407160026
    yield (
        user_id,
        guild_id,
        IconType.static,
        2,
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/banners/00000000000000000000000000000002.png',
    )
    
    user_id = 202407160027
    yield (
        user_id,
        guild_id,
        IconType.animated,
        3,
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/banners/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_user_banner_url_for(user_id, guild_id, icon_type, icon_hash):
    """
    Tests whether ``build_user_banner_url_for`` works as intended.
    
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
    
    Returns
    -------
    output : `None | str`
    """
    output = build_user_banner_url_for(user_id, guild_id, icon_type, icon_hash)
    vampytest.assert_instance(output, str, nullable = True)
    return output

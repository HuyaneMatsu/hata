import vampytest

from ...bases import Icon, IconType
from ...user import AvatarDecoration, User

from ..urls import CDN_ENDPOINT, user_avatar_decoration_url


def _iter_options():
    user_id = 202504180030
    yield (
        user_id,
        False,
        None,
        None,
    )
    
    user_id = 202504180033
    yield (
        user_id,
        True,
        None,
        None,
    )
    
    user_id = 202504180031
    yield (
        user_id,
        True,
        Icon(IconType.static, 2),
        f'{CDN_ENDPOINT}/avatar-decoration-presets/00000000000000000000000000000002.png',
    )
    
    user_id = 202504180032
    yield (
        user_id,
        True,
        Icon(IconType.animated, 3),
        f'{CDN_ENDPOINT}/avatar-decoration-presets/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__user_avatar_decoration_url(user_id, create_avatar_decoration, icon):
    """ 
    Tests whether ``user_avatar_decoration_url`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        User identifier to create user for.
    
    create_avatar_decoration : `bool`
        Whether to create avatar decoration and attack it to the user.
    
    icon : `None | Icon`
        Icon to use as the user's avatar decoration image.
    
    Returns
    -------
    output : `None | str`
    """
    if create_avatar_decoration:
        avatar_decoration = AvatarDecoration(asset = icon)
    else:
        avatar_decoration = None
    
    user = User.precreate(user_id, avatar_decoration = avatar_decoration)
    output = user_avatar_decoration_url(user)
    vampytest.assert_instance(output, str, nullable = True)
    return output

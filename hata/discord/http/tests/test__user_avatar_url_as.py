import vampytest

from ...bases import Icon, IconType
from ...user import User
from ...utils import is_url

from ..urls import CDN_ENDPOINT, user_avatar_url_as


def _iter_options():
    user_id = 202407160006
    yield (
        user_id,
        None,
        {},
        f'{CDN_ENDPOINT}/embed/avatars/5.png',
    )
    
    user_id = 202407160007
    yield (
        user_id,
        Icon(IconType.static, 2),
        {},
        f'{CDN_ENDPOINT}/avatars/{user_id}/00000000000000000000000000000002.png',
    )
    
    user_id = 202407160008
    yield (
        user_id,
        Icon(IconType.static, 2),
        {'size': 1024},
        f'{CDN_ENDPOINT}/avatars/{user_id}/00000000000000000000000000000002.png?size=1024',
    )
    
    user_id = 202407160009
    yield (
        user_id,
        Icon(IconType.static, 2),
        {'size': 1024, 'ext': 'jpg'},
        f'{CDN_ENDPOINT}/avatars/{user_id}/00000000000000000000000000000002.jpg?size=1024',
    )
    
    user_id = 2024060100010
    yield (
        user_id,
        Icon(IconType.animated, 3),
        {},
        f'{CDN_ENDPOINT}/avatars/{user_id}/a_00000000000000000000000000000003.gif',
    )

    user_id = 202407160013
    yield (
        user_id,
        None,
        {'size': 1024, 'ext': 'jpg'},
        'https://cdn.discordapp.com/embed/avatars/5.png',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__user_avatar_url_as(user_id, icon, keyword_parameters):
    """
    Tests whether ``user_avatar_url_as`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        User identifier.
    
    icon : `None | Icon`
        Icon to use as the user's avatar.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    output : `None | str`
    """
    user = User.precreate(user_id, avatar = icon)
    output = user_avatar_url_as(user, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output

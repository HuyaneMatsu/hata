import vampytest

from ...bases import Icon, IconType
from ...user import User
from ...utils import is_url

from ..urls import CDN_ENDPOINT, user_banner_url


def _iter_options():
    user_id = 202407160005
    yield (
        user_id,
        None,
        None,
    )
    
    user_id = 202407160004
    yield (
        user_id,
        Icon(IconType.static, 2),
        f'{CDN_ENDPOINT}/banners/{user_id}/00000000000000000000000000000002.png',
    )
    
    user_id = 202406010003
    yield (
        user_id,
        Icon(IconType.animated, 3),
        f'{CDN_ENDPOINT}/banners/{user_id}/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__user_banner_url(user_id, icon):
    """
    Tests whether ``user_banner_url`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        User identifier.
    
    icon : `None | Icon`
        Icon to use as the user's banner.
    
    Returns
    -------
    output : `None | str`
    """
    user = User.precreate(user_id, banner = icon)
    
    output = user_banner_url(user)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output

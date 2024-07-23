import vampytest

from ...bases import Icon, IconType
from ...user import User
from ...utils import is_url

from ..urls import CDN_ENDPOINT, user_avatar_url


def _iter_options():
    user_id = 202407160002
    yield (
        User.precreate(user_id, avatar = None),
        'https://cdn.discordapp.com/embed/avatars/5.png',
    )
    
    user_id = 202407160000
    yield (
        User.precreate(user_id, avatar = Icon(IconType.static, 2)),
        f'{CDN_ENDPOINT}/avatars/{user_id}/00000000000000000000000000000002.png',
    )
    
    user_id = 202406010001
    yield (
        User.precreate(user_id, avatar = Icon(IconType.animated, 3)),
        f'{CDN_ENDPOINT}/avatars/{user_id}/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__user_avatar_url(user):
    """
    Tests whether ``user_avatar_url`` works as intended.
    
    Parameters
    ----------
    user : ``User``
        User to get its avatar url of.
    
    Returns
    -------
    output : `None | str`
    """
    output = user_avatar_url(user)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output

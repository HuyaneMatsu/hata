import vampytest

from ...user import DefaultAvatar
from ...utils import is_url

from ..urls import CDN_ENDPOINT, default_avatar_url


def _iter_options():
    default_avatar = DefaultAvatar.green
    yield (
        default_avatar,
        f'{CDN_ENDPOINT}/embed/avatars/{default_avatar.value}.png',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__default_avatar_url(default_avatar):
    """
    Tests whether ``default_avatar_url`` works as intended.
    
    Parameters
    ----------
    default_avatar : ``DefaultAvatar``
        Default avatar to use.
    
    Returns
    -------
    output : `None | str`
    """
    output = default_avatar_url(default_avatar)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output

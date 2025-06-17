import vampytest

from ...user import DefaultAvatar

from ..urls import CDN_ENDPOINT, build_default_avatar_url


def _iter_options():
    default_avatar_value = DefaultAvatar.green.value
    
    yield (
        default_avatar_value,
        f'{CDN_ENDPOINT}/embed/avatars/{default_avatar_value}.png',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_default_avatar_url(default_avatar):
    """
    Tests whether ``build_default_avatar_url`` works as intended.
    
    Parameters
    ----------
    default_avatar : ``DefaultAvatar``
        Default avatar to use.
    
    Returns
    -------
    output : `str`
    """
    output = build_default_avatar_url(default_avatar)
    vampytest.assert_instance(output, str)
    return output

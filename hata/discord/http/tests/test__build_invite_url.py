import vampytest

from ..urls import INVITE_ENDPOINT, build_invite_url


def _iter_options():
    invite_code = 'tewi'
    yield (
        invite_code,
        f'{INVITE_ENDPOINT}/{invite_code}',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_invite_url(invite_code):
    """
    Tests whether ``build_invite_url`` works as intended.
    
    Parameters
    ----------
    invite_code : `str`
        Invite code to use.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_invite_url(invite_code)
    vampytest.assert_instance(output, str, nullable = True)
    
    return output

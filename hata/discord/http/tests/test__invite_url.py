import vampytest

from ...invite import Invite
from ...utils import is_url

from ..urls import INVITE_ENDPOINT, invite_url


def _iter_options():
    invite_code = 'tewi'
    yield (
        invite_code,
        f'{INVITE_ENDPOINT}/{invite_code}',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__invite_url(invite_code):
    """
    Tests whether ``invite_url`` works as intended.
    
    Parameters
    ----------
    invite_code : `str`
        Code to create the invite with.
    
    Returns
    -------
    output : `None | str`
    """
    invite = Invite.precreate(invite_code)
    
    output = invite_url(invite)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output

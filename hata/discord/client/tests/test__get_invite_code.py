import vampytest

from ...invite import Invite

from ..request_helpers import get_invite_code


def _iter_options__passing():
    invite_code = 'satori'
    invite = Invite.precreate(invite_code) 
    
    yield (
        invite,
        invite_code,
    )
    
    invite_code = 'okuu'
    
    yield (
        invite_code,
        invite_code,
    )


def _iter_options__type_error():
    yield None
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__get_invite_code(input_value):
    """
    Tests whether ``get_invite_code`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    
    Returns
    -------
    output : `str`
    
    Raises
    ------
    TypeError
    """
    output = get_invite_code(input_value)
    
    vampytest.assert_instance(output, str)
    
    return output

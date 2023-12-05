import vampytest

from ..fields import validate_verification_state
from ..preinstanced import ApplicationVerificationState


def _iter_options__passing():
    yield None, ApplicationVerificationState.none
    yield ApplicationVerificationState.approved, ApplicationVerificationState.approved
    yield ApplicationVerificationState.approved.value, ApplicationVerificationState.approved


def _iter_options__type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_verification_state(input_value):
    """
    Tests whether ``validate_verification_state`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``ApplicationVerificationState``
        
    Raises
    ------
    TypeError
    """
    output = validate_verification_state(input_value)
    vampytest.assert_instance(output, ApplicationVerificationState)
    return output

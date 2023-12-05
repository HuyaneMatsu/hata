import vampytest

from ..fields import parse_verification_state
from ..preinstanced import ApplicationVerificationState


def _iter_options():
    yield {}, ApplicationVerificationState.none
    yield {'verification_state': ApplicationVerificationState.submitted.value}, ApplicationVerificationState.submitted


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_verification_state(input_data):
    """
    Tests whether ``parse_verification_state`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``ApplicationVerificationState``
    """
    output = parse_verification_state(input_data)
    vampytest.assert_instance(output, ApplicationVerificationState)
    return output

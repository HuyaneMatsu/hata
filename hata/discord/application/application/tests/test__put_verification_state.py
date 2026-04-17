import vampytest

from ..fields import put_verification_state
from ..preinstanced import ApplicationVerificationState


def _iter_options():
    yield (
        ApplicationVerificationState.approved,
        False,
        {'verification_state': ApplicationVerificationState.approved.value},
    )
    yield (
        ApplicationVerificationState.approved,
        True,
        {'verification_state': ApplicationVerificationState.approved.value},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_verification_state(input_value, defaults):
    """
    Tests whether ``put_verification_state`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ApplicationVerificationState``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_verification_state(input_value, {}, defaults)

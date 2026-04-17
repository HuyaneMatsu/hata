import vampytest

from ..fields import validate_status
from ..preinstanced import InviteAllowedUserIdsStatusStatus


def _iter_options__passing():
    yield (
        None,
        InviteAllowedUserIdsStatusStatus.none,
    )
    
    yield (
        InviteAllowedUserIdsStatusStatus.failed,
        InviteAllowedUserIdsStatusStatus.failed
    )
    
    yield (
        InviteAllowedUserIdsStatusStatus.failed.value,
        InviteAllowedUserIdsStatusStatus.failed,
    )


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_status(input_value):
    """
    Validates whether ``validate_status`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``InviteAllowedUserIdsStatusStatus``
    
    Raises
    ------
    TypeError
    """
    output = validate_status(input_value)
    vampytest.assert_instance(output, InviteAllowedUserIdsStatusStatus)
    return output

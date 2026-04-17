import vampytest

from ...status_by_platform import Status

from ..fields import validate_web


def _iter_options():
    yield None, Status.offline
    yield Status.online.value, Status.online
    yield Status.online, Status.online


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_web(input_value):
    """
    Validates whether ``validate_web`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``Status``
    
    Raises
    ------
    TypeError
    """
    output = validate_web(input_value)
    vampytest.assert_instance(output, Status)
    return output

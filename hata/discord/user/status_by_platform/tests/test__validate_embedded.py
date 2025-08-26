import vampytest

from ...status_by_platform import Status

from ..fields import validate_embedded


def _iter_options():
    yield None, Status.offline
    yield Status.online.value, Status.online
    yield Status.online, Status.online


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_embedded(input_value):
    """
    Validates whether ``validate_embedded`` works as intended.
    
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
    output = validate_embedded(input_value)
    vampytest.assert_instance(output, Status)
    return output

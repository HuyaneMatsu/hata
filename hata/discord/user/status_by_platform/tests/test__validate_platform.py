import vampytest

from ...status_by_platform import SessionPlatformType

from ..fields import validate_platform


def _iter_options():
    yield None, SessionPlatformType.none
    yield SessionPlatformType.embedded.value, SessionPlatformType.embedded
    yield SessionPlatformType.embedded, SessionPlatformType.embedded


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_platform(input_value):
    """
    Validates whether ``validate_platform`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``SessionPlatformType``
    
    Raises
    ------
    TypeError
    """
    output = validate_platform(input_value)
    vampytest.assert_instance(output, SessionPlatformType)
    return output

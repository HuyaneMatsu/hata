import vampytest

from ..fields import validate_explicit_content_filter_level
from ..preinstanced import ApplicationExplicitContentFilterLevel


def _iter_options__passing():
    yield None, ApplicationExplicitContentFilterLevel.none
    yield ApplicationExplicitContentFilterLevel.filtered, ApplicationExplicitContentFilterLevel.filtered
    yield ApplicationExplicitContentFilterLevel.filtered.value, ApplicationExplicitContentFilterLevel.filtered


def _iter_options__type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_explicit_content_filter_level(input_value):
    """
    Tests whether ``validate_explicit_content_filter_level`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``ApplicationExplicitContentFilterLevel``
        
    Raises
    ------
    TypeError
    """
    output = validate_explicit_content_filter_level(input_value)
    vampytest.assert_instance(output, ApplicationExplicitContentFilterLevel)
    return output

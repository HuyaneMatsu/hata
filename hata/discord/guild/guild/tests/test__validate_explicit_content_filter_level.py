import vampytest

from ..fields import validate_explicit_content_filter_level
from ..preinstanced import ExplicitContentFilterLevel


def _iter_options__passing():
    yield None, ExplicitContentFilterLevel.disabled
    yield ExplicitContentFilterLevel.no_role, ExplicitContentFilterLevel.no_role
    yield ExplicitContentFilterLevel.no_role.value, ExplicitContentFilterLevel.no_role



def _iter_options__type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_explicit_content_filter_level(input_value):
    """
    Tests whether `validate_explicit_content_filter_level` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``ExplicitContentFilterLevel``
    
    Raises
    ------
    TypeError
    """
    output = validate_explicit_content_filter_level(input_value)
    vampytest.assert_instance(output, ExplicitContentFilterLevel)
    return output

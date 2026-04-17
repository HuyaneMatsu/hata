import vampytest

from ..fields import validate_source_type
from ..preinstanced import EntitlementSourceType


def _iter_options__passing():
    yield None, EntitlementSourceType.none
    yield EntitlementSourceType.user_gift, EntitlementSourceType.user_gift
    yield EntitlementSourceType.user_gift.value, EntitlementSourceType.user_gift


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_source_type(input_value):
    """
    Validates whether ``validate_source_type`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``EntitlementSourceType``
    
    Raises
    ------
    TypeError
    """
    output = validate_source_type(input_value)
    vampytest.assert_instance(output, EntitlementSourceType)
    return output

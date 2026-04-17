import vampytest

from ..fields import validate_default_sort_order
from ..preinstanced import SortOrder


def _iter_options__passing():
    yield None, SortOrder.latest_activity
    yield SortOrder.creation_date, SortOrder.creation_date
    yield SortOrder.creation_date.value, SortOrder.creation_date


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_default_sort_order(input_value):
    """
    Validates whether ``validate_default_sort_order`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``SortOrder``
    
    Raises
    ------
    TypeError
    """
    output = validate_default_sort_order(input_value)
    vampytest.assert_instance(output, SortOrder)
    return output

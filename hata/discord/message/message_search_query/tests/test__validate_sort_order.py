import vampytest

from ..fields import validate_sort_order
from ..preinstanced import MessageSearchSortOrderType


def _iter_options__passing():
    yield (
        None,
        MessageSearchSortOrderType.descending,
    )
    
    yield (
        MessageSearchSortOrderType.ascending,
        MessageSearchSortOrderType.ascending,
    )
    
    yield (
        MessageSearchSortOrderType.ascending.value,
        MessageSearchSortOrderType.ascending,
    )


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_sort_order(input_value):
    """
    Tests whether `validate_sort_order` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``MessageSearchSortOrderType``
    
    Raises
    ------
    TypeError
    """
    output = validate_sort_order(input_value)
    vampytest.assert_instance(output, MessageSearchSortOrderType)
    return output

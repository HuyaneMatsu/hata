import vampytest

from ..fields import validate_sort_by
from ..preinstanced import MessageSearchSortByType


def _iter_options__passing():
    yield (
        None,
        MessageSearchSortByType.creation,
    )
    
    yield (
        MessageSearchSortByType.relevance,
        MessageSearchSortByType.relevance,
    )
    
    yield (
        MessageSearchSortByType.relevance.value,
        MessageSearchSortByType.relevance,
    )


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_sort_by(input_value):
    """
    Tests whether `validate_sort_by` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``MessageSearchSortByType``
    
    Raises
    ------
    TypeError
    """
    output = validate_sort_by(input_value)
    vampytest.assert_instance(output, MessageSearchSortByType)
    return output

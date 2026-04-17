import vampytest

from ..fields import parse_sort_order
from ..preinstanced import MessageSearchSortOrderType


def _iter_options():
    yield (
        {},
        MessageSearchSortOrderType.descending,
    )
    
    yield (
        {
            'sort_order': None,
        },
        MessageSearchSortOrderType.descending,
    )
    
    yield (
        {
            'sort_order': MessageSearchSortOrderType.ascending.value,
        },
        MessageSearchSortOrderType.ascending,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_sort_order(input_data):
    """
    Tests whether ``parse_sort_order`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``MessageSearchSortOrderType``
    """
    output = parse_sort_order(input_data)
    vampytest.assert_instance(output, MessageSearchSortOrderType)
    return output

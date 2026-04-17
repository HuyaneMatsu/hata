import vampytest

from ..fields import put_sort_order
from ..preinstanced import MessageSearchSortOrderType


def _iter_options():
    yield (
        MessageSearchSortOrderType.descending,
        False,
        {},
    )
    
    yield (
        MessageSearchSortOrderType.descending,
        True,
        {
            'sort_order': MessageSearchSortOrderType.descending.value,
        },
    )
    
    yield (
        MessageSearchSortOrderType.ascending,
        False,
        {
            'sort_order': MessageSearchSortOrderType.ascending.value,
        },
    )
    
    yield (
        MessageSearchSortOrderType.ascending,
        True,
        {
            'sort_order': MessageSearchSortOrderType.ascending.value,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_sort_order(input_value, defaults):
    """
    Tests whether ``put_sort_order`` works as intended.
    
    Parameters
    ----------
    input_value : ``MessageSearchSortOrderType``
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_sort_order(input_value, {}, defaults)

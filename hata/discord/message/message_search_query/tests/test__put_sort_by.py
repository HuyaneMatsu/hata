import vampytest

from ..fields import put_sort_by
from ..preinstanced import MessageSearchSortByType


def _iter_options():
    yield (
        MessageSearchSortByType.creation,
        False,
        {},
    )
    
    yield (
        MessageSearchSortByType.creation,
        True,
        {
            'sort_by': MessageSearchSortByType.creation.value,
        },
    )
    
    yield (
        MessageSearchSortByType.relevance,
        False,
        {
            'sort_by': MessageSearchSortByType.relevance.value,
        },
    )
    
    yield (
        MessageSearchSortByType.relevance,
        True,
        {
            'sort_by': MessageSearchSortByType.relevance.value,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_sort_by(input_value, defaults):
    """
    Tests whether ``put_sort_by`` works as intended.
    
    Parameters
    ----------
    input_value : ``MessageSearchSortByType``
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_sort_by(input_value, {}, defaults)

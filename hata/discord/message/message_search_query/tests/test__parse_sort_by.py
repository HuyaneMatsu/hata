import vampytest

from ..fields import parse_sort_by
from ..preinstanced import MessageSearchSortByType


def _iter_options():
    yield (
        {},
        MessageSearchSortByType.creation,
    )
    
    yield (
        {
            'sort_by': None,
        },
        MessageSearchSortByType.creation,
    )
    
    yield (
        {
            'sort_by': MessageSearchSortByType.relevance.value,
        },
        MessageSearchSortByType.relevance,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_sort_by(input_data):
    """
    Tests whether ``parse_sort_by`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``MessageSearchSortByType``
    """
    output = parse_sort_by(input_data)
    vampytest.assert_instance(output, MessageSearchSortByType)
    return output

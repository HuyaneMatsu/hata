import vampytest

from ..preinstanced import SortOrder

from ..fields import parse_default_sort_order


def _iter_options():
    yield {}, SortOrder.latest_activity
    yield {'default_sort_order': None}, SortOrder.latest_activity
    yield {'default_sort_order': SortOrder.creation_date.value}, SortOrder.creation_date
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_default_sort_order(input_data):
    """
    Tests whether ``parse_default_sort_order`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``SortOrder``
    """
    output = parse_default_sort_order(input_data)
    vampytest.assert_instance(output, SortOrder)
    return output

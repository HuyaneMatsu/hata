import vampytest

from ..fields import put_default_sort_order
from ..preinstanced import SortOrder


def _iter_options():
    yield SortOrder.latest_activity, False, {}
    yield SortOrder.latest_activity, True, {'default_sort_order': SortOrder.latest_activity.value}
    yield SortOrder.creation_date, False, {'default_sort_order': SortOrder.creation_date.value}
    yield SortOrder.creation_date, True, {'default_sort_order': SortOrder.creation_date.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_default_sort_order(input_value, defaults):
    """
    Tests whether ``put_default_sort_order`` is working as intended.
    
    Parameters
    ----------
    input_value : ``SortOrder``
        Value to serialize.
    defaults : `bool`
        Whether fields with their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_default_sort_order(input_value, {}, defaults)

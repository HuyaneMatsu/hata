import vampytest

from ..value_mergers import value_merger_sorted_array, value_merger_replace


def _iter_options__value_merger_sorted_array():
    yield None, None, None
    yield (1,), None, (1,)
    yield None, (2,), (2,)
    yield (1,), (2,), (1, 2)


@vampytest._(vampytest.call_from(_iter_options__value_merger_sorted_array()).returning_last())
def test__value_merger_sorted_array(value_0, value_1):
    """
    Tests whether ``value_merger_sorted_array`` works as intended.
    
    Parameters
    ----------
    value_0 : `None | tuple<sortable>`
        Self instance's value.
    value_1 : `None | tuple<sortable>`
        Other instance's value.
    
    Returns
    -------
    new : `None | tuple<sortable>`
    """
    return value_merger_sorted_array(value_0, value_1)


def _iter_options__value_merger_replace():
    yield None, None, None
    yield 1, None, 1
    yield None, 2, 2
    yield 1, 2, 2


@vampytest._(vampytest.call_from(_iter_options__value_merger_replace()).returning_last())
def test__value_merger_replace(value_0, value_1):
    """
    Tests whether ``value_merger_replace`` works as intended.
    
    Parameters
    ----------
    value_0 : `None | object`
        Self instance's value.
    value_1 : `None | object`
        Other instance's value.
    
    Returns
    -------
    new : `None | object`
    """
    return value_merger_replace(value_0, value_1)

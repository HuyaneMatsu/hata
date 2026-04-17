import vampytest

from ..fields import put_deep_historical_indexing_in_progress


def _iter_options():
    yield (
        False,
        False,
        {},
    )
    
    yield (
        False,
        True,
        {
            'doing_deep_historical_index': False,
        },
    )
    
    yield (
        True,
        False,
        {
            'doing_deep_historical_index': True,
        },
    )
    
    yield (
        True,
        True,
        {
            'doing_deep_historical_index': True
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_deep_historical_indexing_in_progress(input_value, defaults):
    """
    Tests whether ``put_deep_historical_indexing_in_progress`` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_deep_historical_indexing_in_progress(input_value, {}, defaults)

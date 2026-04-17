import vampytest

from ..fields import parse_deep_historical_indexing_in_progress


def _iter_options():
    yield (
        {},
        False,
    )
    
    yield (
        {
            'doing_deep_historical_index': None,
        },
        False,
    )
    
    yield (
        {
            'doing_deep_historical_index': False,
        },
        False,
    )
    
    yield (
        {
            'doing_deep_historical_index': True,
        },
        True,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_deep_historical_indexing_in_progress(input_data):
    """
    Tests whether ``parse_deep_historical_indexing_in_progress`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    output = parse_deep_historical_indexing_in_progress(input_data)
    vampytest.assert_instance(output, bool)
    return output

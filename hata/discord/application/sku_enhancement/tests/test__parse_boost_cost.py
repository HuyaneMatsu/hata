import vampytest

from ..fields import parse_boost_cost


def _iter_options():
    yield (
        {},
        0,
    )
    
    yield (
        {
            'boost_price': None,
        },
        0,
    )
    
    yield (
        {
            'boost_price': 1,
        },
        1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_boost_cost(input_data):
    """
    Tests whether ``parse_boost_cost`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_boost_cost(input_data)
    vampytest.assert_instance(output, int)
    return output

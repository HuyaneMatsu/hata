import vampytest

from ..fields import parse_purchase_limit


def _iter_options():
    yield (
        {},
        0,
    )
    
    yield (
        {
            'purchase_limit': None,
        },
        0,
    )
    
    yield (
        {
            'purchase_limit': 1,
        },
        1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_purchase_limit(input_data):
    """
    Tests whether ``parse_purchase_limit`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_purchase_limit(input_data)
    vampytest.assert_instance(output, int)
    return output

import vampytest

from ..fields import parse_total


def _iter_options():
    yield (
        {},
        0,
    )
    
    yield (
        {
            'total_users': None,
        },
        0,
    )
    
    yield (
        {
            'total_users': 1,
        },
        1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_total(input_data):
    """
    Tests whether ``parse_total`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to try to parse the total from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_total(input_data)
    vampytest.assert_instance(output, int)
    return output

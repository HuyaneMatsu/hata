import vampytest

from ..fields import parse_value


def _iter_options():
    yield (
        {},
        0,
    )
    
    yield (
        {
            'id': None,
        },
        0,
    )
    
    yield (
        {
            'id': 1,
        },
        1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_value(input_data):
    """
    Tests whether ``parse_value`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_value(input_data)
    vampytest.assert_instance(output, int)
    return output

import vampytest

from ..fields import parse_count


def _iter_options():
    yield (
        {},
        0,
    )
    
    yield (
        {
            'count': None,
        },
        0,
    )
    
    yield (
        {
            'count': 1,
        },
        1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_count(input_data):
    """
    Tests whether ``parse_count`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_count(input_data)
    vampytest.assert_instance(output, int)
    return output

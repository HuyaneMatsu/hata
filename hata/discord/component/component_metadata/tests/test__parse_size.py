import vampytest

from ..fields import parse_size


def _iter_options():
    yield (
        {},
        0,
    )
    
    yield (
        {
            'size': None,
        },
        0,
    )
    
    yield (
        {
            'size': 1,
        },
        1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_size(input_data):
    """
    Tests whether ``parse_size`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_size(input_data)
    vampytest.assert_instance(output, int)
    return output

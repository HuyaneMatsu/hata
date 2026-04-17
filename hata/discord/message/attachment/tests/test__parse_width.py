import vampytest

from ..fields import parse_width


def _iter_options():
    yield {}, 0
    yield {'width': None}, 0
    yield {'width': 1}, 1


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_width(input_data):
    """
    Tests whether ``parse_width`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_width(input_data)
    vampytest.assert_instance(output, int)
    return output

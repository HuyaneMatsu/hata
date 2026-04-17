import vampytest

from ..fields import parse_duration


def _iter_options():
    yield {}, 0
    yield {'duration_seconds': None}, 0
    yield {'duration_seconds': 1}, 1


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_duration(input_data):
    """
    Tests whether ``parse_duration`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_duration(input_data)
    vampytest.assert_instance(output, int)
    return output

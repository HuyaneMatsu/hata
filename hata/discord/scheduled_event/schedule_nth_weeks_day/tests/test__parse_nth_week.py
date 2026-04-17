import vampytest

from ..fields import parse_nth_week


def _iter_options():
    yield {}, 1
    yield {'n': 1}, 1
    yield {'n': 2}, 2


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_nth_week(input_data):
    """
    Tests whether ``parse_nth_week`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_nth_week(input_data)
    vampytest.assert_instance(output, int)
    return output

import vampytest

from ..fields import parse_slowmode


def _iter_options():
    yield {}, 0
    yield {'rate_limit_per_user': None}, 0
    yield {'rate_limit_per_user': 1}, 1


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_slowmode(input_data):
    """
    Tests whether ``parse_slowmode`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_slowmode(input_data)
    vampytest.assert_instance(output, int)
    return output

import vampytest

from ..fields import parse_score


def _iter_options():
    yield {}, 0
    yield {'activity_score': None}, 0
    yield {'activity_score': 1}, 1


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_score(input_data):
    """
    Tests whether ``parse_score`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_score(input_data)
    vampytest.assert_instance(output, int)
    return output

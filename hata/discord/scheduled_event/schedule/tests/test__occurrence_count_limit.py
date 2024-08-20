import vampytest

from ..fields import parse_occurrence_count_limit


def _iter_options():
    yield {}, 0
    yield {'count': 1}, 1


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_occurrence_count_limit(input_data):
    """
    Tests whether ``parse_occurrence_count_limit`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    return parse_occurrence_count_limit(input_data)

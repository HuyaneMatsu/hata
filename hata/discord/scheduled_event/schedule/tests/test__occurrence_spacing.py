import vampytest

from ..fields import parse_occurrence_spacing


def _iter_options():
    yield {}, 1
    yield {'interval': 2}, 2


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_occurrence_spacing(input_data):
    """
    Tests whether ``parse_occurrence_spacing`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    return parse_occurrence_spacing(input_data)

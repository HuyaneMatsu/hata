import vampytest

from ..fields import parse_reason


def _iter_options():
    yield {}, None
    yield {'reason': None}, None
    yield {'reason': ''}, None
    yield {'reason': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_reason(input_data):
    """
    Tests whether ``parse_reason`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    return parse_reason(input_data)

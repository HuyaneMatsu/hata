import vampytest

from ..fields import parse_name


def _iter_options():
    yield {}, ''
    yield {'title': None}, ''
    yield {'title': ''}, ''
    yield {'title': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_name(input_data):
    """
    Tests whether ``parse_name`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse the name from.
    
    Returns
    -------
    name : `str`
    """
    return parse_name(input_data)

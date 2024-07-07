import vampytest

from ..fields import parse_title


def _iter_options():
    yield {}, ''
    yield {'label': None}, ''
    yield {'label': ''}, ''
    yield {'label': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_title(input_data):
    """
    Tests whether ``parse_title`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse the title from.
    
    Returns
    -------
    title : `str`
    """
    return parse_title(input_data)

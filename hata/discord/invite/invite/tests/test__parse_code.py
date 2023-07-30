import vampytest

from ..fields import parse_code


def _iter_options():
    yield {}, ''
    yield {'code': None}, ''
    yield {'code': ''}, ''
    yield {'code': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_code(input_data):
    """
    Tests whether ``parse_code`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse the code from.
    
    Returns
    -------
    code : `str`
    """
    return parse_code(input_data)

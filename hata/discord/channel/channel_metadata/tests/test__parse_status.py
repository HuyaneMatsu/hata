import vampytest

from ..fields import parse_status


def _iter_options():
    yield {}, None
    yield {'status': None}, None
    yield {'status': ''}, None
    yield {'status': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_status(input_data):
    """
    Tests whether ``parse_status`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Output to parse from.
    
    Returns
    -------
    output : `None`, `str`
    """
    return parse_status(input_data)

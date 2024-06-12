import vampytest

from ..fields import parse_description


def _iter_options():
    yield {}, None
    yield {'description': None}, None
    yield {'description': ''}, None
    yield {'description': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_description(input_data):
    """
    Tests whether ``parse_description`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    return parse_description(input_data)

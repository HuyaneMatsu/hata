import vampytest

from ..fields import parse_topic


def _iter_options():
    yield {}, None
    yield {'topic': None}, None
    yield {'topic': ''}, None
    yield {'topic': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_topic(input_data):
    """
    Tests whether ``parse_topic`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Output to parse from.
    
    Returns
    -------
    output : `None`, `str`
    """
    return parse_topic(input_data)

import vampytest

from ..fields import parse_keywords


def _iter_options():
    yield {}, None
    yield {'keywords': None}, None
    yield {'keywords': []}, None
    yield {'keywords': ['apple']}, ('apple', )
    yield {'keywords': ['apple', 'bad']}, ('apple', 'bad')
    yield {'keywords': ['bad', 'apple']}, ('apple', 'bad')


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_keywords(input_data):
    """
    Tests whether ``parse_keywords`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<str>`
    """
    return parse_keywords(input_data)

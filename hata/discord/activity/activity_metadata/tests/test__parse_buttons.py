import vampytest

from ..fields import parse_buttons


def _iter_options():
    yield {}, None
    yield {'buttons': None}, None
    yield {'buttons': []}, None
    yield {'buttons': ['apple']}, ('apple', )
    yield {'buttons': ['apple', 'bad']}, ('apple', 'bad')
    yield {'buttons': ['bad', 'apple']}, ('bad', 'apple')


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_buttons(input_data):
    """
    Tests whether ``parse_buttons`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<str>`
    """
    return parse_buttons(input_data)

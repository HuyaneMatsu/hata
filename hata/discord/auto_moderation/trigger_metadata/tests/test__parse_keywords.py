import vampytest

from ..fields import parse_keywords


def _iter_options():
    yield {}, None
    yield {'keyword_filter': None}, None
    yield {'keyword_filter': []}, None
    yield {'keyword_filter': ['apple']}, ('apple', )
    yield {'keyword_filter': ['apple', 'bad']}, ('apple', 'bad')
    yield {'keyword_filter': ['bad', 'apple']}, ('apple', 'bad')


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
    output = parse_keywords(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output

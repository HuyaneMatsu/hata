import vampytest

from ..fields import parse_regex_patterns


def _iter_options():
    yield {}, None
    yield {'regex_patterns': None}, None
    yield {'regex_patterns': []}, None
    yield {'regex_patterns': ['apple']}, ('apple', )
    yield {'regex_patterns': ['apple', 'bad']}, ('apple', 'bad')
    yield {'regex_patterns': ['bad', 'apple']}, ('apple', 'bad')


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_regex_patterns(input_data):
    """
    Tests whether ``parse_regex_patterns`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<str>`
    """
    output = parse_regex_patterns(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output

import vampytest

from ..fields import parse_excluded_keywords


def _iter_options():
    yield {}, None
    yield {'allow_list': None}, None
    yield {'allow_list': []}, None
    yield {'allow_list': ['apple']}, ('apple', )
    yield {'allow_list': ['apple', 'bad']}, ('apple', 'bad')
    yield {'allow_list': ['bad', 'apple']}, ('apple', 'bad')


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_excluded_keywords(input_data):
    """
    Tests whether ``parse_excluded_keywords`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<str>`
    """
    output = parse_excluded_keywords(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output

import vampytest

from ..fields import parse_text_small


def _iter_options():
    yield {}, None
    yield {'small_text': None}, None
    yield {'small_text': ''}, None
    yield {'small_text': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_text_small(input_data):
    """
    Tests whether ``parse_text_small`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_text_small(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output

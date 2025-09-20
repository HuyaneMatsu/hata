import vampytest

from ..fields import parse_text_large


def _iter_options():
    yield {}, None
    yield {'large_text': None}, None
    yield {'large_text': ''}, None
    yield {'large_text': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_text_large(input_data):
    """
    Tests whether ``parse_text_large`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_text_large(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output

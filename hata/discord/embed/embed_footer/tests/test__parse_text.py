import vampytest

from ..fields import parse_text


def _iter_options():
    yield {'text': None}, None
    yield {'text': ''}, None
    yield {'text': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_text(input_data):
    """
    Tests whether ``parse_text`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_text(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output

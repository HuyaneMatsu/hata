import vampytest

from ..fields import parse_placeholder


def _iter_options():
    yield {}, None
    yield {'placeholder': None}, None
    yield {'placeholder': ''}, None
    yield {'placeholder': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_placeholder(input_data):
    """
    Tests whether ``parse_placeholder`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_placeholder(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output

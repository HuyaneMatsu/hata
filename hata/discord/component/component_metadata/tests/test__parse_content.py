import vampytest

from ..fields import parse_content


def _iter_options():
    yield {}, None
    yield {'content': None}, None
    yield {'content': ''}, None
    yield {'content': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_content(input_data):
    """
    Tests whether ``parse_content`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse the content from.
    
    Returns
    -------
    content : `None | str`
    """
    output = parse_content(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output

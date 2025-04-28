import vampytest

from ..fields import parse_tag


def _iter_options():
    yield {}, ''
    yield {'tag': None}, ''
    yield {'tag': ''}, ''
    yield {'tag': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_tag(input_data):
    """
    Tests whether ``parse_tag`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse the tag from.
    
    Returns
    -------
    tag : `str`
    """
    output = parse_tag(input_data)
    vampytest.assert_instance(output, str)
    return output

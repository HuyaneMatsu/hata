import vampytest

from ..fields import parse_name


def _iter_options():
    yield {}, ''
    yield {'label': None}, ''
    yield {'label': ''}, ''
    yield {'label': 'COLLECTIBLES_NAMEPLATES_CITYSCAPE_A11Y'}, 'COLLECTIBLES_NAMEPLATES_CITYSCAPE_A11Y'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_name(input_data):
    """
    Tests whether ``parse_name`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse the name from.
    
    Returns
    -------
    name : `str`
    """
    output = parse_name(input_data)
    vampytest.assert_instance(output, str)
    return output

import vampytest

from ..fields import parse_location


def _iter_options():
    yield {}, None
    yield {'location': None}, None
    yield {'location': ''}, None
    yield {'location': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_location(input_data):
    """
    Tests whether ``parse_location`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_location(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output

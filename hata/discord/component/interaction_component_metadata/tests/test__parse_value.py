import vampytest

from ..fields import parse_value


def _iter_options():
    yield {}, None
    yield {'value': None}, None
    yield {'value': ''}, None
    yield {'value': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_value(input_data):
    """
    Tests whether ``parse_value`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_value(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output

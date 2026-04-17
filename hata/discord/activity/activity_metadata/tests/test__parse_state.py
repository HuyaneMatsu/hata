import vampytest

from ..fields import parse_state


def _iter_options():
    yield {}, None
    yield {'state': None}, None
    yield {'state': ''}, None
    yield {'state': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_state(input_data):
    """
    Tests whether ``parse_state`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_state(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output

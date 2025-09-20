import vampytest

from ..fields import parse_state_url


def _iter_options():
    yield {}, None
    yield {'state_url': None}, None
    yield {'state_url': ''}, None
    yield {'state_url': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_state_url(input_data):
    """
    Tests whether ``parse_state_url`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_state_url(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output

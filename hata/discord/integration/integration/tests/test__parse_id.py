import vampytest

from ..fields import parse_id


def _iter_options():
    integration_id = 202307310012
    
    yield {}, 0
    yield {'id': None}, 0
    yield {'id': str(integration_id)}, integration_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_id(input_data):
    """
    Tests whether ``parse_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    return parse_id(input_data)

import vampytest

from ..fields import parse_target_id


def _iter_options():
    target_id = 202310200000
    
    yield {}, 0
    yield {'target_id': None}, 0
    yield {'target_id': str(target_id)}, target_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_target_id(input_data):
    """
    Tests whether ``parse_target_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to try to parse the target identifier from.
    
    Returns
    -------
    output : `int`
    """
    return parse_target_id(input_data)

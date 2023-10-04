import vampytest

from ..fields import parse_subscription_id


def _iter_options():
    subscription_id = 202310030011
    
    yield {}, 0
    yield {'subscription_id': None}, 0
    yield {'subscription_id': str(subscription_id)}, subscription_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_subscription_id(input_data):
    """
    Tests whether ``parse_subscription_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to try to parse the subscription identifier from.
    
    Returns
    -------
    output : `int`
    """
    return parse_subscription_id(input_data)

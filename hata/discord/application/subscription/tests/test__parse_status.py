import vampytest

from ..fields import parse_status
from ..preinstanced import SubscriptionStatus


def _iter_options():
    yield {}, SubscriptionStatus.active
    yield {'status': SubscriptionStatus.ending.value}, SubscriptionStatus.ending


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_status(input_data):
    """
    Tests whether ``parse_status`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``SubscriptionStatus``
    """
    output = parse_status(input_data)
    vampytest.assert_instance(output, SubscriptionStatus)
    return output

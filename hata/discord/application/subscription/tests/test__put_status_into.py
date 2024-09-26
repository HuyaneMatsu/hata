import vampytest

from ..fields import put_status_into
from ..preinstanced import SubscriptionStatus


def _iter_options():
    yield SubscriptionStatus.active, False, {'status': SubscriptionStatus.active.value}
    yield SubscriptionStatus.active, True, {'status': SubscriptionStatus.active.value}
    yield SubscriptionStatus.ending, False, {'status': SubscriptionStatus.ending.value}
    yield SubscriptionStatus.ending, True, {'status': SubscriptionStatus.ending.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_status_into(input_value, defaults):
    """
    Tests whether ``put_status_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``SubscriptionStatus``
        Value to serialize.
    defaults : `bool`
        Whether values as their defaults should be included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_status_into(input_value, {}, defaults)

import vampytest

from ..fields import put_subscription_id


def _iter_options():
    subscription_id = 202310030010
    
    yield 0, False, {}
    yield 0, True, {'subscription_id': None}
    yield subscription_id, False, {'subscription_id': str(subscription_id)}
    yield subscription_id, True, {'subscription_id': str(subscription_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_subscription_id(subscription_id, defaults):
    """
    Tests whether ``put_subscription_id`` works as intended.
    
    Parameters
    ----------
    subscription_id : `int`
        The subscription's identifier to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_subscription_id(subscription_id, {}, defaults)

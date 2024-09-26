import vampytest

from ...application import Subscription

from ..request_helpers import get_subscription_and_sku_id_and_id


def _iter_options__passing():
    subscription_id = 202409230003
    sku_id = 202409230004
    
    yield (
        (sku_id, subscription_id),
        [],
        (None, sku_id, subscription_id),
    )
    
    subscription_id = 202409230005
    sku_id = 202409230006
    
    yield (
        (str(sku_id), str(subscription_id)),
        [],
        (None, sku_id, subscription_id),
    )
    
    subscription_id = 202409230007
    sku_id = 202409230008
    subscription = Subscription.precreate(subscription_id, sku_ids = [sku_id])
    
    yield (
        subscription,
        [subscription],
        (subscription, sku_id, subscription_id),
    )
    
    
    subscription_id = 202409230009
    sku_id = 0
    subscription = Subscription.precreate(subscription_id, sku_ids = [sku_id])
    
    yield (
        subscription,
        [subscription],
        (subscription, sku_id, subscription_id),
    )


    subscription_id = 202409230010
    sku_id = 202409230011
    subscription = Subscription.precreate(subscription_id, sku_ids = [sku_id])
    
    yield (
        (sku_id, subscription_id),
        [subscription],
        (subscription, sku_id, subscription_id),
    )


def _iter_options__type_error():
    yield None, []
    yield 12.6, []
    yield (202409230012, 'hey'), []
    yield ('hey', 202409230013), []


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__get_subscription_and_sku_id_and_id(input_value, extra):
    """
    Tests whether ``get_subscription_and_sku_id_and_id`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    extra : `list<object>`
        Additional objects to keep in the cache.
    
    Returns
    -------
    output : `(None | Subscription, int, int)`
    
    Raises
    ------
    TypeError
    """
    return get_subscription_and_sku_id_and_id(input_value)

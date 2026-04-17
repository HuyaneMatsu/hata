import vampytest

from ...subscription import Subscription

from ..fields import validate_subscription_id


def _iter_options__passing():
    subscription_id = 202310020015
    
    yield 0, 0
    yield subscription_id, subscription_id
    yield str(subscription_id), subscription_id
    yield None, 0
    yield Subscription.precreate(subscription_id), subscription_id


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield '-1'
    yield '1111111111111111111111'
    yield -1
    yield 1111111111111111111111


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_subscription_id(input_value):
    """
    Tests whether `validate_subscription_id` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_subscription_id(input_value)
    vampytest.assert_instance(output, int)
    return output

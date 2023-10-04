import vampytest

from ..fields import validate_subscription_id


def _iter_options__passing():
    subscription_id = 202310020015
    
    yield 0, 0
    yield subscription_id, subscription_id
    yield str(subscription_id), subscription_id


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
def test__validate_subscription_id__passing(input_value):
    """
    Tests whether `validate_subscription_id` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to get `subscription_id` of.
    
    Returns
    -------
    output : `int`
    """
    return validate_subscription_id(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
@vampytest.call_with(None)
def test__validate_subscription_id__type_error(input_value):
    """
    Tests whether `validate_subscription_id` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value to get `subscription_id` of.
    
    Raises
    ------
    TypeError
        The occurred exception.
    """
    validate_subscription_id(input_value)


@vampytest.raising(ValueError)
@vampytest.call_with('-1')
@vampytest.call_with('1111111111111111111111')
@vampytest.call_with(-1)
@vampytest.call_with(1111111111111111111111)
def test__validate_subscription_id__value_error(input_value):
    """
    Tests whether `validate_subscription_id` works as intended.
    
    Case: `ValueError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value to get `subscription_id` of.
    
    Raises
    ------
    ValueError
        The occurred exception.
    """
    validate_subscription_id(input_value)

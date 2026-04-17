import vampytest

from ..fields import validate_subscription_listing_id


def test__validate_subscription_listing_id__0():
    """
    Tests whether `validate_subscription_listing_id` works as intended.
    
    Case: passing.
    """
    subscription_listing_id = 202301190002
    
    for input_value, expected_output in (
        (subscription_listing_id, subscription_listing_id),
        (str(subscription_listing_id), subscription_listing_id),
    ):
        output = validate_subscription_listing_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_subscription_listing_id__1():
    """
    Tests whether `validate_subscription_listing_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '-1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_subscription_listing_id(input_value)


def test__validate_subscription_listing_id__2():
    """
    Tests whether `validate_subscription_listing_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_subscription_listing_id(input_value)

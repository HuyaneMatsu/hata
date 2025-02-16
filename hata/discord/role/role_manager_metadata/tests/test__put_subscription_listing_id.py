import vampytest

from ..fields import put_subscription_listing_id


def test__put_subscription_listing_id():
    """
    Tests whether ``put_subscription_listing_id`` works as intended.
    """
    subscription_listing_id = 202212160001
    
    for input_value, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'subscription_listing_id': None}),
        (subscription_listing_id, False, {'subscription_listing_id': str(subscription_listing_id)}),
    ):
        data = put_subscription_listing_id(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)

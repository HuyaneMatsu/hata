import vampytest

from ..fields import parse_subscription_listing_id


def test__parse_subscription_listing_id():
    """
    Tests whether ``parse_subscription_listing_id`` works as intended.
    """
    subscription_listing_id = 202212160000
    
    for input_data, expected_output in (
        ({}, 0),
        ({'subscription_listing_id': None}, 0),
        ({'subscription_listing_id': str(subscription_listing_id)}, subscription_listing_id),
    ):
        output = parse_subscription_listing_id(input_data)
        vampytest.assert_eq(output, expected_output)

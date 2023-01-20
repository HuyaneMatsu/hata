import vampytest

from ..fields import put_subscription_listing_id_into


def test__put_subscription_listing_id_into():
    """
    Tests whether ``put_subscription_listing_id_into`` is working as intended.
    """
    subscription_listing_id = 202301190001
    
    for input_value, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'role_subscription_listing_id': None}),
        (subscription_listing_id, False, {'role_subscription_listing_id': str(subscription_listing_id)}),
    ):
        data = put_subscription_listing_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)

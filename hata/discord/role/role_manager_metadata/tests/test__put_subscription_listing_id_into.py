import vampytest

from ..fields import put_subscription_listing_id_into


def test__put_subscription_listing_id_into():
    """
    Tests whether ``put_subscription_listing_id_into`` works as intended.
    """
    subscription_listing_id = 202212160001
    
    for input_, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'subscription_listing_id': None}),
        (subscription_listing_id, False, {'subscription_listing_id': str(subscription_listing_id)}),
    ):
        data = put_subscription_listing_id_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)

import vampytest

from ..fields import put_purchasable_into


def test__put_purchasable_into():
    """
    Tests whether ``put_purchasable_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (True, False, {'available_for_purchase': None}),
        (False, True, {}),
        (True, True, {'available_for_purchase': None}),
    ):
        data = put_purchasable_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)

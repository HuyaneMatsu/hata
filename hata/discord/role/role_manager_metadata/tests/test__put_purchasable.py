import vampytest

from ..fields import put_purchasable


def test__put_purchasable():
    """
    Tests whether ``put_purchasable`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (True, False, {'available_for_purchase': None}),
        (False, True, {}),
        (True, True, {'available_for_purchase': None}),
    ):
        data = put_purchasable(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)

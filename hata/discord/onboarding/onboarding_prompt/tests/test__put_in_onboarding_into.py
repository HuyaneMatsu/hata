import vampytest

from ..fields import put_in_onboarding_into


def test__put_in_onboarding_into():
    """
    Tests whether ``put_in_onboarding_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {'in_onboarding': False}),
        (False, True, {'in_onboarding': False}),
        (True, False, {'in_onboarding': True}),
    ):
        data = put_in_onboarding_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)

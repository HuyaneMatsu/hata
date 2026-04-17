import vampytest

from ..fields import put_in_onboarding


def test__put_in_onboarding():
    """
    Tests whether ``put_in_onboarding`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {'in_onboarding': False}),
        (False, True, {'in_onboarding': False}),
        (True, False, {'in_onboarding': True}),
    ):
        data = put_in_onboarding(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)

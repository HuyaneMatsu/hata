import vampytest

from ..fields import parse_in_onboarding


def test__parse_in_onboarding():
    """
    Tests whether ``parse_in_onboarding`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'in_onboarding': False}, False),
        ({'in_onboarding': True}, True),
    ):
        output = parse_in_onboarding(input_data)
        vampytest.assert_eq(output, expected_output)

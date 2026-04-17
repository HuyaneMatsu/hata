import vampytest

from ...onboarding_prompt_option import OnboardingPromptOption

from ..fields import parse_options


def test__parse_options():
    """
    Tests whether ``parse_options`` works as intended.
    """
    option = OnboardingPromptOption(name = 'ibuki')
    
    for input_value, expected_output in (
        ({}, None),
        ({'options': None}, None),
        ({'options': [option.to_data()]}, (option, )),
    ):
        output = parse_options(input_value)
        vampytest.assert_eq(output, expected_output)

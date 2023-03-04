import vampytest

from ...onboarding_prompt import OnboardingPrompt

from ..fields import parse_prompts


def test__parse_prompts():
    """
    Tests whether ``parse_prompts`` works as intended.
    """
    prompt = OnboardingPrompt(name = 'ibuki')
    
    for input_value, expected_output in (
        ({}, None),
        ({'prompts': None}, None),
        ({'prompts': [prompt.to_data()]}, (prompt, )),
    ):
        output = parse_prompts(input_value)
        vampytest.assert_eq(output, expected_output)

import vampytest

from ...onboarding_prompt import OnboardingPrompt
from ..fields import put_prompts_into


def test__put_prompts_into():
    """
    Tests whether ``put_prompts_into`` works as intended.
    """
    prompt = OnboardingPrompt.precreate(202303040028, name = 'ibuki')
    
    for input_value, expected_output in (
        (None, {'prompts': []}),
        ((prompt, ), {'prompts': [prompt.to_data(defaults = True, include_internals = True)]}),
    ):
        output = put_prompts_into(input_value, {}, True, include_internals = True)
        vampytest.assert_eq(output, expected_output)

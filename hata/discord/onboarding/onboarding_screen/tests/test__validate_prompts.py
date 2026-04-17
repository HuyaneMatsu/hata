import vampytest

from ...onboarding_prompt import OnboardingPrompt

from ..fields import validate_prompts


def test__validate_prompts__0():
    """
    Tests whether ``validate_prompts`` works as intended.
    
    Case: passing.
    """
    prompt = OnboardingPrompt(name = 'ibuki')
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([prompt], (prompt, )),
    ):
        output = validate_prompts(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_prompts__1():
    """
    Tests whether ``validate_prompts`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_prompts(input_value)

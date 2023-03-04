import vampytest

from ...onboarding_prompt_option import OnboardingPromptOption

from ..fields import validate_options


def test__validate_options__0():
    """
    Tests whether ``validate_options`` works as intended.
    
    Case: passing.
    """
    option = OnboardingPromptOption(name = 'ibuki')
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([option], (option, )),
    ):
        output = validate_options(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_options__1():
    """
    Tests whether ``validate_options`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_options(input_value)

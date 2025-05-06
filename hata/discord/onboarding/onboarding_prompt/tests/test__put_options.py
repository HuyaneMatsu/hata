import vampytest

from ...onboarding_prompt_option import OnboardingPromptOption
from ..fields import put_options


def test__put_options():
    """
    Tests whether ``put_options`` works as intended.
    """
    option = OnboardingPromptOption.precreate(202303040005, name = 'ibuki')
    
    for input_value, expected_output in (
        (None, {'options': []}),
        ((option, ), {'options': [option.to_data(defaults = True, include_internals = True)]}),
    ):
        output = put_options(input_value, {}, True, include_internals = True)
        vampytest.assert_eq(output, expected_output)

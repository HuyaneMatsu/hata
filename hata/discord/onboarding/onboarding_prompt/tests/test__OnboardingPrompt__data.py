import vampytest

from ...onboarding_prompt_option import OnboardingPromptOption

from ..onboarding_prompt import OnboardingPrompt
from ..preinstanced import OnboardingPromptType

from .test__OnboardingPrompt__constructor import _assert_fields_set


def test__OnboardingPrompt__from_data__0():
    """
    Tests whether ``OnboardingPrompt.from_data`` works as intended.
    
    Case: all fields given.
    """
    in_onboarding = True
    name = 'yukari'
    options = [
        OnboardingPromptOption.precreate(202303040007, name = 'ibuki'),
        OnboardingPromptOption.precreate(202303040008, name = 'suika'),
    ]
    required = True
    single_select = True
    prompt_type = OnboardingPromptType.dropdown
    prompt_id = 202303040006
    
    data = {
        'in_onboarding': in_onboarding,
        'title': name,
        'options': [option.to_data(defaults = True, include_internals = True) for option in options],
        'required': required,
        'single_select': single_select,
        'type': prompt_type.value,
        'id': str(prompt_id),
    }
    
    prompt = OnboardingPrompt.from_data(data)
    _assert_fields_set(prompt)
    
    vampytest.assert_eq(prompt.in_onboarding, in_onboarding)
    vampytest.assert_eq(prompt.name, name)
    vampytest.assert_eq(prompt.options, tuple(options))
    vampytest.assert_eq(prompt.required, required)
    vampytest.assert_eq(prompt.single_select, single_select)
    vampytest.assert_is(prompt.type, prompt_type)
    
    vampytest.assert_eq(prompt.id, prompt_id)



def test__OnboardingPrompt__to_data__0():
    """
    Tests whether ``OnboardingPrompt.to_data`` works as intended.
    
    Case: Include defaults and internals.
    """
    in_onboarding = True
    name = 'yukari'
    options = [
        OnboardingPromptOption.precreate(202303040009, name = 'ibuki'),
        OnboardingPromptOption.precreate(202303040010, name = 'suika'),
    ]
    required = True
    single_select = True
    prompt_type = OnboardingPromptType.dropdown
    prompt_id = 202303040011
    
    prompt = OnboardingPrompt.precreate(
        prompt_id,
        in_onboarding = in_onboarding,
        name = name,
        options = options,
        required = required,
        single_select = single_select,
        prompt_type = prompt_type,
    )
    
    expected_output = {
        'in_onboarding': in_onboarding,
        'title': name,
        'options': [option.to_data(defaults = True, include_internals = True) for option in options],
        'required': required,
        'single_select': single_select,
        'type': prompt_type.value,
        'id': str(prompt_id),
    }
    
    vampytest.assert_eq(
        prompt.to_data(defaults = True, include_internals = True),
        expected_output,
    )

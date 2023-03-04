import vampytest

from ...onboarding_prompt_option import OnboardingPromptOption

from ..onboarding_prompt import OnboardingPrompt
from ..preinstanced import OnboardingPromptType


def test__OnboardingPrompt__repr():
    """
    Tests whether ``OnboardingPrompt.__repr__`` works as intended.
    """
    in_onboarding = True
    name = 'yukari'
    options = [
        OnboardingPromptOption(name = 'ibuki'),
        OnboardingPromptOption(name = 'suika'),
    ]
    required = True
    single_select = True
    prompt_type = OnboardingPromptType.dropdown
    
    prompt = OnboardingPrompt(
        in_onboarding = in_onboarding,
        name = name,
        options = options,
        required = required,
        single_select = single_select,
        prompt_type = prompt_type,
    )
    
    vampytest.assert_instance(repr(prompt), str)


def test__OnboardingPrompt__hash():
    """
    Tests whether ``OnboardingPrompt.__hash__`` works as intended.
    """
    in_onboarding = True
    name = 'yukari'
    options = [
        OnboardingPromptOption(name = 'ibuki'),
        OnboardingPromptOption(name = 'suika'),
    ]
    required = True
    single_select = True
    prompt_type = OnboardingPromptType.dropdown
    
    prompt = OnboardingPrompt(
        in_onboarding = in_onboarding,
        name = name,
        options = options,
        required = required,
        single_select = single_select,
        prompt_type = prompt_type,
    )
    
    vampytest.assert_instance(hash(prompt), int)


def test__OnboardingPrompt__eq():
    """
    Tests whether ``OnboardingPrompt.__repr__`` works as intended.
    """
    in_onboarding = True
    name = 'yukari'
    options = [
        OnboardingPromptOption(name = 'ibuki'),
        OnboardingPromptOption(name = 'suika'),
    ]
    required = True
    single_select = True
    prompt_type = OnboardingPromptType.dropdown
    prompt_id = 202303040012
    
    keyword_parameters = {
        'in_onboarding': in_onboarding,
        'name': name,
        'options': options,
        'required': required,
        'single_select': single_select,
        'prompt_type': prompt_type,
    }
    
    prompt = OnboardingPrompt.precreate(prompt_id, **keyword_parameters)
    
    vampytest.assert_eq(prompt, prompt)
    vampytest.assert_ne(prompt, object())
    
    test_prompt = OnboardingPrompt(**keyword_parameters)
    vampytest.assert_eq(prompt, test_prompt)
    
    for field_required, field_value in (
        ('in_onboarding', False),
        ('name', 'yukari'),
        ('options', None),
        ('required', False),
        ('single_select', False),
        ('prompt_type', OnboardingPromptType.multiple_choice),
    ):
        test_prompt = OnboardingPrompt(**{**keyword_parameters, field_required: field_value})
        vampytest.assert_ne(prompt, test_prompt)

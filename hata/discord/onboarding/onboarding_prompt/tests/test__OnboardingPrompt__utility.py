import vampytest

from ...onboarding_prompt_option import OnboardingPromptOption

from ..onboarding_prompt import OnboardingPrompt
from ..preinstanced import OnboardingPromptType

from .test__OnboardingPrompt__constructor import _assert_fields_set


def test__OnboardingPrompt__copy():
    """
    Tests whether ``OnboardingPrompt.copy`` works as intended.
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
    copy = prompt.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(prompt, copy)

    vampytest.assert_eq(prompt, copy)


def test__OnboardingPrompt__copy_with__0():
    """
    Tests whether ``OnboardingPrompt.copy_with`` works as intended.
    
    Case: no fields given.
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
    copy = prompt.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(prompt, copy)

    vampytest.assert_eq(prompt, copy)


def test__OnboardingPrompt__copy_with__1():
    """
    Tests whether ``OnboardingPrompt.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_in_onboarding = True
    old_name = 'yukari'
    old_options = [
        OnboardingPromptOption(name = 'ibuki'),
        OnboardingPromptOption(name = 'suika'),
    ]
    old_required = True
    old_single_select = True
    old_prompt_type = OnboardingPromptType.dropdown
    
    new_in_onboarding = False
    new_name = 'chen'
    new_options = [
        OnboardingPromptOption(name = 'yakumo'),
        OnboardingPromptOption(name = 'ran'),
    ]
    new_required = False
    new_single_select = False
    new_prompt_type = OnboardingPromptType.multiple_choice
    
    prompt = OnboardingPrompt(
        in_onboarding = old_in_onboarding,
        name = old_name,
        options = old_options,
        required = old_required,
        single_select = old_single_select,
        prompt_type = old_prompt_type,
    )
    copy = prompt.copy_with(
        in_onboarding = new_in_onboarding,
        name = new_name,
        options = new_options,
        required = new_required,
        single_select = new_single_select,
        prompt_type = new_prompt_type,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(prompt, copy)

    vampytest.assert_eq(copy.in_onboarding, new_in_onboarding)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.options, tuple(new_options))
    vampytest.assert_eq(copy.required, new_required)
    vampytest.assert_eq(copy.single_select, new_single_select)
    vampytest.assert_is(copy.type, new_prompt_type)


def test__OnboardingPrompt__iter_options():
    """
    Tests whether ``OnboardingPrompt.iter_options`` works as intended.
    """
    option_0 = OnboardingPromptOption(name = 'ibuki')
    option_1 = OnboardingPromptOption(name = 'suika')
    
    for input_value, expected_output in (
        (None, []),
        ([option_0], [option_0]),
        ([option_0, option_1], [option_0, option_1]),
    ):
        prompt = OnboardingPrompt(options = input_value)
        
        vampytest.assert_eq([*prompt.iter_options()], expected_output)

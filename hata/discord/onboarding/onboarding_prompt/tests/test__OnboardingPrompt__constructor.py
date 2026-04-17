import vampytest

from ...onboarding_prompt_option import OnboardingPromptOption

from ..onboarding_prompt import OnboardingPrompt
from ..preinstanced import OnboardingPromptType


def _assert_fields_set(prompt):
    """
    Checks whether every fields are set of the given onboarding prompt.
    
    Parameters
    ----------
    prompt : ``OnboardingPrompt``
        The prompt to check.
    """
    vampytest.assert_instance(prompt, OnboardingPrompt)
    vampytest.assert_instance(prompt.in_onboarding, bool)
    vampytest.assert_instance(prompt.id, int)
    vampytest.assert_instance(prompt.name, str)
    vampytest.assert_instance(prompt.options, tuple, nullable = True)
    vampytest.assert_instance(prompt.required, bool)
    vampytest.assert_instance(prompt.single_select, bool)
    vampytest.assert_instance(prompt.type, OnboardingPromptType)


def test__OnboardingPrompt__new__0():
    """
    Tests whether ``OnboardingPrompt.__new__`` works as intended.
    
    Case: No fields given.
    """
    option = OnboardingPrompt()
    _assert_fields_set(option)


def test__OnboardingPrompt__new__1():
    """
    Tests whether ``OnboardingPrompt.__new__`` works as intended.
    
    Case: Fields given.
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
    _assert_fields_set(prompt)
    
    vampytest.assert_eq(prompt.in_onboarding, in_onboarding)
    vampytest.assert_eq(prompt.name, name)
    vampytest.assert_eq(prompt.options, tuple(options))
    vampytest.assert_eq(prompt.required, required)
    vampytest.assert_eq(prompt.single_select, single_select)
    vampytest.assert_is(prompt.type, prompt_type)


def test__OnboardingPrompt__precreate__0():
    """
    Tests whether ``OnboardingPrompt.precreate`` works as intended.
    
    Case: No fields given.
    """
    prompt_id = 202303040003
    
    prompt = OnboardingPrompt.precreate(
        prompt_id,
    )
    _assert_fields_set(prompt)
    
    vampytest.assert_eq(prompt.id, prompt_id)


def test__OnboardingPrompt__precreate__1():
    """
    Tests whether ``OnboardingPrompt.precreate`` works as intended.
    
    Case: Fields given.
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
    prompt_id = 202303040004
    
    prompt = OnboardingPrompt.precreate(
        prompt_id,
        prompt_type = prompt_type,
        in_onboarding = in_onboarding,
        name = name,
        options = options,
        required = required,
        single_select = single_select,
    )
    _assert_fields_set(prompt)
    
    vampytest.assert_eq(prompt.in_onboarding, in_onboarding)
    vampytest.assert_eq(prompt.name, name)
    vampytest.assert_eq(prompt.options, tuple(options))
    vampytest.assert_eq(prompt.required, required)
    vampytest.assert_eq(prompt.single_select, single_select)
    vampytest.assert_is(prompt.type, prompt_type)
    
    vampytest.assert_eq(prompt.id, prompt_id)

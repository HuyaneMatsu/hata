from copy import deepcopy as deep_copy

import vampytest

from ...onboarding_prompt import OnboardingPrompt

from ..onboarding_screen import OnboardingScreen
from ..utils import populate_prompt_ids_in_onboarding_screen_prompt_options


def _iter_options():
    yield (
        {
            'prompts': None,
        },
        None,
        {
            'prompts': None,
        },
    )
    
    yield (
        {
            'prompts': [],
        },
        None,
        {
            'prompts': [],
        },
    )
    
    yield (
        {
            'prompts': [
                {
                    'title': 'Orin',
                },
                {
                    'title': 'Okuu',
                },
            ],
        },
        None,
        {
            'prompts': [
                {
                    'title': 'Orin',
                    'id': str((1 << 22) + 0)
                },
                {
                    'title': 'Okuu',
                    'id': str((1 << 22) + 1)
                },
            ],
        },
    )
    
    prompt_0 = OnboardingPrompt.precreate(
        202502150030,
        name = 'Orin',
    )
    prompt_1 = OnboardingPrompt.precreate(
        202502150031,
        name = 'Okuu',
    )
    prompt_2 = OnboardingPrompt(
        name = 'Koishi',
    )
    
    onboarding_screen = OnboardingScreen(
        prompts = [prompt_0, prompt_1],
    )
    
    yield (
        {
            **onboarding_screen.to_data(defaults = True),
            'prompts': [
                prompt_0.to_data(defaults = True),
                prompt_1.to_data(defaults = True),
                prompt_2.to_data(defaults = True),
            ],
        },
        onboarding_screen,
        {
            **onboarding_screen.to_data(defaults = True),
            'prompts': [
                {
                    **prompt_0.to_data(defaults = True),
                    'id': str(prompt_0.id),
                }, {
                    **prompt_1.to_data(defaults = True),
                    'id': str(prompt_1.id),
                }, {
                    **prompt_2.to_data(defaults = True),
                    'id': str((1 << 22) + 0),
                },
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__populate_prompt_ids_in_onboarding_screen_prompt_options(prompt_data, onboarding_screen_template):
    """
    tests whether ``populate_prompt_ids_in_onboarding_screen_prompt_options`` works as intended.
    
    Parameters
    ----------
    prompt_data : `dict<str, object>`
        Onboarding prompt data.
    
    onboarding_screen_template : `None | OnboardingScreen`
        Onboarding screen used as a template.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    input_value = deep_copy(prompt_data)
    return populate_prompt_ids_in_onboarding_screen_prompt_options(input_value, onboarding_screen_template)

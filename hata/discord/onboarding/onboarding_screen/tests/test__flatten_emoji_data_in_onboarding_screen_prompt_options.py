from copy import deepcopy as deep_copy

import vampytest

from ....core import BUILTIN_EMOJIS

from ..utils import flatten_emoji_data_in_onboarding_screen_prompt_options


def _iter_options():
    yield (
        {
            'prompts': None,
        },
        {
            'prompts': None,
        },
    )
    
    yield (
        {
            'prompts': [],
        },
        {
            'prompts': [],
        },
    )
    
    emoji = BUILTIN_EMOJIS['x']
    
    yield (
        {
            'prompts': [
                {},
                {
                    'options': None,
                },
                {
                    'options': [],
                },
                {
                    'options': [
                        {}
                    ],
                },
                {
                    'options': [
                        {
                            'emoji': None,
                        },
                        {
                            'emoji': {
                                'id': '2023112700000',
                                'animated': True,
                            },
                        },
                        {
                            'emoji': {
                                'name': emoji.unicode,
                            },
                        },
                    ],
                },
            ],
        },
        {
            'prompts': [
                {},
                {
                    'options': None,
                },
                {
                    'options': [],
                },
                {
                    'options': [
                        {}
                    ],
                },
                {
                    'options': [
                        {
                            'emoji_name': None,
                        },
                        {
                            'emoji_id': '2023112700000',
                            'emoji_animated': True,
                        },
                        {
                            'emoji_name': emoji.unicode,
                        },
                    ],
                },
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__flatten_emoji_data_in_onboarding_screen_prompt_options(input_value):
    """
    tests whether ``flatten_emoji_data_in_onboarding_screen_prompt_options`` works as intended.
    
    input_value : `dict<str, object>`
        Onboarding prompt data.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    input_value = deep_copy(input_value)
    return flatten_emoji_data_in_onboarding_screen_prompt_options(input_value)

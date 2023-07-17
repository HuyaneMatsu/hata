import vampytest

from ...onboarding_prompt import OnboardingPrompt

from ..onboarding_screen import OnboardingScreen
from ..preinstanced import OnboardingMode


def test__OnboardingScreen__repr():
    """
    Tests whether ``OnboardingScreen.__repr__`` works as intended.
    """
    default_channel_ids = [202303040046, 202303040047]
    enabled = True
    mode = OnboardingMode.advanced
    prompts = [
        OnboardingPrompt(name = 'ibuki'),
        OnboardingPrompt(name = 'suika'),
    ]
    
    screen = OnboardingScreen(
        default_channel_ids = default_channel_ids,
        enabled = enabled,
        mode = mode,
        prompts = prompts,
    )
    
    vampytest.assert_instance(repr(screen), str)


def test__OnboardingScreen__hash():
    """
    Tests whether ``OnboardingScreen.__hash__`` works as intended.
    """
    default_channel_ids = [202303040048, 202303040049]
    enabled = True
    mode = OnboardingMode.advanced
    prompts = [
        OnboardingPrompt(name = 'ibuki'),
        OnboardingPrompt(name = 'suika'),
    ]
    
    screen = OnboardingScreen(
        default_channel_ids = default_channel_ids,
        enabled = enabled,
        mode = mode,
        prompts = prompts,
    )
    
    vampytest.assert_instance(hash(screen), int)


def test__OnboardingScreen__eq():
    """
    Tests whether ``OnboardingScreen.__repr__`` works as intended.
    """
    default_channel_ids = [202303040050, 202303040051]
    enabled = True
    mode = OnboardingMode.advanced
    prompts = [
        OnboardingPrompt(name = 'ibuki'),
        OnboardingPrompt(name = 'suika'),
    ]
    guild_id = 202303040052
    
    keyword_parameters = {
        'default_channel_ids': default_channel_ids,
        'enabled': enabled,
        'mode': mode,
        'prompts': prompts,
    }
    
    screen = OnboardingScreen.precreate(guild_id = guild_id, **keyword_parameters)
    
    vampytest.assert_eq(screen, screen)
    vampytest.assert_ne(screen, object())
    
    test_screen = OnboardingScreen(**keyword_parameters)
    vampytest.assert_eq(screen, test_screen)
    
    for field_prompts, field_value in (
        ('default_channel_ids', None),
        ('enabled', False),
        ('mode', OnboardingMode.default),
        ('prompts', None),
    ):
        test_screen = OnboardingScreen(**{**keyword_parameters, field_prompts: field_value})
        vampytest.assert_ne(screen, test_screen)

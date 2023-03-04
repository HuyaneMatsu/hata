import vampytest

from ...onboarding_prompt import OnboardingPrompt

from ..onboarding_screen import OnboardingScreen

from .test__OnboardingScreen__constructor import _assert_fields_set


def test__OnboardingScreen__from_data__0():
    """
    Tests whether ``OnboardingScreen.from_data`` works as intended.
    
    Case: all fields given.
    """
    default_channel_ids = [202303040036, 202303040037]
    enabled = True
    prompts = [
        OnboardingPrompt.precreate(202303040038, name = 'ibuki'),
        OnboardingPrompt.precreate(202303040039, name = 'suika'),
    ]
    guild_id = 202303040040
    
    data = {
        'default_channel_ids': [str(channel_id) for channel_id in default_channel_ids],
        'enabled': enabled,
        'guild_id': str(guild_id),
        'prompts': [prompt.to_data(defaults = True, include_internals = True) for prompt in prompts],
    }
    
    screen = OnboardingScreen.from_data(data)
    _assert_fields_set(screen)
    
    vampytest.assert_eq(screen.default_channel_ids, tuple(default_channel_ids))
    vampytest.assert_eq(screen.enabled, enabled)
    vampytest.assert_eq(screen.prompts, tuple(prompts))
    vampytest.assert_eq(screen.guild_id, guild_id)



def test__OnboardingScreen__to_data__0():
    """
    Tests whether ``OnboardingScreen.to_data`` works as intended.
    
    Case: Include defaults and internals.
    """
    default_channel_ids = [202303040041, 202303040042]
    enabled = True
    prompts = [
        OnboardingPrompt.precreate(202303040043, name = 'ibuki'),
        OnboardingPrompt.precreate(202303040044, name = 'suika'),
    ]
    guild_id = 202303040045
    
    screen = OnboardingScreen.precreate(
        default_channel_ids = default_channel_ids,
        enabled = enabled,
        prompts = prompts,
        guild_id = guild_id,
    )
    
    expected_output = {
        'default_channel_ids': [str(channel_id) for channel_id in default_channel_ids],
        'enabled': enabled,
        'guild_id': str(guild_id),
        'prompts': [prompt.to_data(defaults = True, include_internals = True) for prompt in prompts],
    }
    
    vampytest.assert_eq(
        screen.to_data(defaults = True, include_internals = True),
        expected_output,
    )

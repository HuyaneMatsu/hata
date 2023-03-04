import vampytest

from ...onboarding_prompt import OnboardingPrompt

from ..onboarding_screen import OnboardingScreen


def _assert_fields_set(screen):
    """
    Checks whether every fields are set of the given onboarding screen.
    
    Parameters
    ----------
    screen : ``OnboardingScreen``
        The onboarding screen to check.
    """
    vampytest.assert_instance(screen, OnboardingScreen)
    vampytest.assert_instance(screen.default_channel_ids, tuple, nullable = True)
    vampytest.assert_instance(screen.enabled, bool)
    vampytest.assert_instance(screen.guild_id, int)
    vampytest.assert_instance(screen.prompts, tuple, nullable = True)


def test__OnboardingScreen__new__0():
    """
    Tests whether ``OnboardingScreen.__new__`` works as intended.
    
    Case: No fields given.
    """
    screen = OnboardingScreen()
    _assert_fields_set(screen)


def test__OnboardingScreen__new__1():
    """
    Tests whether ``OnboardingScreen.__new__`` works as intended.
    
    Case: Fields given.
    """
    default_channel_ids = [202303040031, 202303040032]
    enabled = True
    prompts = [
        OnboardingPrompt(name = 'ibuki'),
        OnboardingPrompt(name = 'suika'),
    ]
    
    screen = OnboardingScreen(
        default_channel_ids = default_channel_ids,
        enabled = enabled,
        prompts = prompts,
    )
    _assert_fields_set(screen)
    
    vampytest.assert_eq(screen.default_channel_ids, tuple(default_channel_ids))
    vampytest.assert_eq(screen.enabled, enabled)
    vampytest.assert_eq(screen.prompts, tuple(prompts))


def test__OnboardingScreen__precreate__0():
    """
    Tests whether ``OnboardingScreen.precreate`` works as intended.
    
    Case: No fields given.
    """
    screen = OnboardingScreen.precreate()
    _assert_fields_set(screen)


def test__OnboardingScreen__precreate__1():
    """
    Tests whether ``OnboardingScreen.precreate`` works as intended.
    
    Case: Fields given.
    """
    default_channel_ids = [202303040033, 202303040034]
    enabled = True
    prompts = [
        OnboardingPrompt(name = 'ibuki'),
        OnboardingPrompt(name = 'suika'),
    ]
    guild_id = 202303040035
    
    screen = OnboardingScreen.precreate(
        default_channel_ids = default_channel_ids,
        enabled = enabled,
        prompts = prompts,
        guild_id = guild_id,
    )
    _assert_fields_set(screen)
    
    vampytest.assert_eq(screen.default_channel_ids, tuple(default_channel_ids))
    vampytest.assert_eq(screen.enabled, enabled)
    vampytest.assert_eq(screen.prompts, tuple(prompts))
    
    vampytest.assert_eq(screen.guild_id, guild_id)

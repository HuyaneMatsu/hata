import vampytest

from ....channel import Channel

from ...onboarding_prompt import OnboardingPrompt

from ..onboarding_screen import OnboardingScreen

from .test__OnboardingScreen__constructor import _assert_fields_set


def test__OnboardingScreen__copy():
    """
    Tests whether ``OnboardingScreen.copy`` works as intended.
    """
    default_channel_ids = [202303040053, 202303040054]
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
    copy = screen.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(screen, copy)

    vampytest.assert_eq(screen, copy)


def test__OnboardingScreen__copy_with__0():
    """
    Tests whether ``OnboardingScreen.copy_with`` works as intended.
    
    Case: no fields given.
    """
    default_channel_ids = [202303040055, 202303040056]
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
    copy = screen.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(screen, copy)

    vampytest.assert_eq(screen, copy)


def test__OnboardingScreen__copy_with__1():
    """
    Tests whether ``OnboardingScreen.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_default_channel_ids = [202303040057, 202303040058]
    old_enabled = True
    old_prompts = [
        OnboardingPrompt(name = 'ibuki'),
        OnboardingPrompt(name = 'suika'),
    ]
    
    new_default_channel_ids = [202303040059, 202303040060]
    new_enabled = False
    new_prompts = [
        OnboardingPrompt(name = 'yakumo'),
        OnboardingPrompt(name = 'ran'),
    ]
    
    screen = OnboardingScreen(
        default_channel_ids = old_default_channel_ids,
        enabled = old_enabled,
        prompts = old_prompts,
    )
    copy = screen.copy_with(
        default_channel_ids = new_default_channel_ids,
        enabled = new_enabled,
        prompts = new_prompts,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(screen, copy)

    vampytest.assert_eq(copy.default_channel_ids, tuple(new_default_channel_ids))
    vampytest.assert_eq(copy.enabled, new_enabled)
    vampytest.assert_eq(copy.prompts, tuple(new_prompts))


def test__OnboardingScreen__iter_default_channel_ids():
    """
    Tests whether ``OnboardingScreen.iter_default_channel_ids`` works as intended.
    """
    channel_id_0 = 202303040061
    channel_id_1 = 202303040062
    
    for input_value, expected_output in (
        (None, []),
        ([channel_id_0], [channel_id_0]),
        ([channel_id_0, channel_id_1], [channel_id_0, channel_id_1]),
    ):
        screen = OnboardingScreen(default_channel_ids = input_value)
        
        vampytest.assert_eq([*screen.iter_default_channel_ids()], expected_output)


def test__OnboardingScreen__iter_default_channels():
    """
    Tests whether ``OnboardingScreen.iter_default_channels`` works as intended.
    """
    channel_id_0 = 202303040063
    channel_id_1 = 202303040064
    
    channel_0 = Channel.precreate(channel_id_0)
    channel_1 = Channel.precreate(channel_id_1)
    
    for input_value, expected_output in (
        (None, []),
        ([channel_id_0], [channel_0]),
        ([channel_id_0, channel_id_1], [channel_0, channel_1]),
    ):
        screen = OnboardingScreen(default_channel_ids = input_value)
        
        vampytest.assert_eq([*screen.iter_default_channels()], expected_output)


def test__OnboardingScreen__default_channels():
    """
    Tests whether ``OnboardingScreen.default_channels`` works as intended.
    """
    channel_id_0 = 202303040065
    channel_id_1 = 202303040066
    
    channel_0 = Channel.precreate(channel_id_0)
    channel_1 = Channel.precreate(channel_id_1)
    
    for input_value, expected_output in (
        (None, None),
        ([channel_id_0], (channel_0,)),
        ([channel_id_0, channel_id_1], (channel_0, channel_1)),
    ):
        screen = OnboardingScreen(default_channel_ids = input_value)
        
        vampytest.assert_eq(screen.default_channels, expected_output)


def test__OnboardingScreen__iter_prompts():
    """
    Tests whether ``OnboardingScreen.iter_prompts`` works as intended.
    
    Case: no fields given.
    """
    prompt_0 = OnboardingPrompt(name = 'ibuki')
    prompt_1 = OnboardingPrompt(name = 'suika')
    
    for input_value, expected_output in (
        (None, []),
        ([prompt_0], [prompt_0]),
        ([prompt_0, prompt_1], [prompt_0, prompt_1]),
    ):
        screen = OnboardingScreen(prompts = input_value)
        
        vampytest.assert_eq([*screen.iter_prompts()], expected_output)

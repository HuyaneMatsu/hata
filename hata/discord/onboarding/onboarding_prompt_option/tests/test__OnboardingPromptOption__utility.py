import vampytest

from ....core import BUILTIN_EMOJIS

from ..onboarding_prompt_option import OnboardingPromptOption

from .test__OnboardingPromptOption__constructor import _assert_fields_set


def test__OnboardingPromptOption__copy():
    """
    Tests whether ``OnboardingPromptOption.copy`` works as intended.
    """
    channel_ids = [202302030034, 202302030035]
    description = 'yukari'
    emoji = BUILTIN_EMOJIS['x']
    name = 'yakumo'
    role_ids = [202302030036, 202302030037]
    
    option = OnboardingPromptOption(
        channel_ids = channel_ids,
        description = description,
        emoji = emoji,
        name = name,
        role_ids = role_ids,
    )
    copy = option.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(option, copy)

    vampytest.assert_eq(option, copy)


def test__OnboardingPromptOption__copy_with__0():
    """
    Tests whether ``OnboardingPromptOption.copy_with`` works as intended.
    
    Case: no fields given.
    """
    channel_ids = [202302030038, 202302030039]
    description = 'yukari'
    emoji = BUILTIN_EMOJIS['x']
    name = 'yakumo'
    role_ids = [202302030040, 202302030041]
    
    option = OnboardingPromptOption(
        channel_ids = channel_ids,
        description = description,
        emoji = emoji,
        name = name,
        role_ids = role_ids,
    )
    copy = option.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(option, copy)

    vampytest.assert_eq(option, copy)


def test__OnboardingPromptOption__copy_with__1():
    """
    Tests whether ``OnboardingPromptOption.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_channel_ids = [202302030042, 202302030043]
    old_description = 'yukari'
    old_emoji = BUILTIN_EMOJIS['x']
    old_name = 'yakumo'
    old_role_ids = [202302030044, 202302030045]
    
    new_channel_ids = [202302030046, 202302030047]
    new_description = 'yukari'
    new_emoji = BUILTIN_EMOJIS['heart']
    new_name = 'yakumo'
    new_role_ids = [202302030048, 202302030049]
    
    option = OnboardingPromptOption(
        channel_ids = old_channel_ids,
        description = old_description,
        emoji = old_emoji,
        name = old_name,
        role_ids = old_role_ids,
    )
    copy = option.copy_with(
        channel_ids = new_channel_ids,
        description = new_description,
        emoji = new_emoji,
        name = new_name,
        role_ids = new_role_ids,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(option, copy)

    vampytest.assert_eq(copy.channel_ids, tuple(new_channel_ids))
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.emoji, new_emoji)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.role_ids, tuple(new_role_ids))

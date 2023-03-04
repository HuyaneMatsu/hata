import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..onboarding_prompt_option import OnboardingPromptOption


def _assert_fields_set(option):
    """
    Checks whether every fields are set of the given onboarding prompt option.
    
    Parameters
    ----------
    option : ``OnboardingPromptOption``
        The option to check.
    """
    vampytest.assert_instance(option, OnboardingPromptOption)
    vampytest.assert_instance(option.channel_ids, tuple, nullable = True)
    vampytest.assert_instance(option.description, str, nullable = True)
    vampytest.assert_instance(option.emoji, Emoji, nullable = True)
    vampytest.assert_instance(option.id, int)
    vampytest.assert_instance(option.name, str)
    vampytest.assert_instance(option.role_ids, tuple, nullable = True)


def test__OnboardingPromptOption__new__0():
    """
    Tests whether ``OnboardingPromptOption.__new__`` works as intended.
    
    Case: No fields given.
    """
    option = OnboardingPromptOption()
    _assert_fields_set(option)


def test__OnboardingPromptOption__new__1():
    """
    Tests whether ``OnboardingPromptOption.__new__`` works as intended.
    
    Case: Fields given.
    """
    channel_ids = [202302030009, 202302030010]
    description = 'yukari'
    emoji = BUILTIN_EMOJIS['x']
    name = 'yakumo'
    role_ids = [202302030011, 202302030012]
    
    option = OnboardingPromptOption(
        channel_ids = channel_ids,
        description = description,
        emoji = emoji,
        name = name,
        role_ids = role_ids,
    )
    _assert_fields_set(option)
    
    vampytest.assert_eq(option.channel_ids, tuple(channel_ids))
    vampytest.assert_eq(option.description, description)
    vampytest.assert_eq(option.emoji, emoji)
    vampytest.assert_eq(option.name, name)
    vampytest.assert_eq(option.role_ids, tuple(role_ids))


def test__OnboardingPromptOption__precreate__0():
    """
    Tests whether ``OnboardingPromptOption.precreate`` works as intended.
    
    Case: No fields given.
    """
    option_id = 202302030053
    
    option = OnboardingPromptOption.precreate(
        option_id,
    )
    _assert_fields_set(option)
    
    vampytest.assert_eq(option.id, option_id)


def test__OnboardingPromptOption__precreate__1():
    """
    Tests whether ``OnboardingPromptOption.precreate`` works as intended.
    
    Case: Fields given.
    """
    channel_ids = [202302030054, 202302030055]
    description = 'yukari'
    emoji = BUILTIN_EMOJIS['x']
    name = 'yakumo'
    role_ids = [202302030056, 202302030057]
    option_id = 202302030058
    
    option = OnboardingPromptOption.precreate(
        option_id,
        channel_ids = channel_ids,
        description = description,
        emoji = emoji,
        name = name,
        role_ids = role_ids,
    )
    _assert_fields_set(option)
    
    vampytest.assert_eq(option.channel_ids, tuple(channel_ids))
    vampytest.assert_eq(option.description, description)
    vampytest.assert_eq(option.emoji, emoji)
    vampytest.assert_eq(option.name, name)
    vampytest.assert_eq(option.role_ids, tuple(role_ids))
    
    vampytest.assert_eq(option.id, option_id)

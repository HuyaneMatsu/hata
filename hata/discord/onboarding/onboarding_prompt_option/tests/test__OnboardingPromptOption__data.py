import vampytest

from ....core import BUILTIN_EMOJIS

from ..onboarding_prompt_option import OnboardingPromptOption

from .test__OnboardingPromptOption__constructor import _assert_fields_set


def test__OnboardingPromptOption__from_data__0():
    """
    Tests whether ``OnboardingPromptOption.from_data`` works as intended.
    
    Case: all fields given.
    """
    channel_ids = [202302030013, 202302030014]
    description = 'yukari'
    emoji = BUILTIN_EMOJIS['x']
    name = 'yakumo'
    role_ids = [202302030015, 202302030016]
    option_id = 202302030050
    
    data = {
        'channel_ids': [str(channel_id) for channel_id in channel_ids],
        'description': description,
        'emoji': {'name': emoji.unicode},
        'title': name,
        'role_ids': [str(role_id) for role_id in role_ids],
        'id': str(option_id),
    }
    
    option = OnboardingPromptOption.from_data(data)
    _assert_fields_set(option)
    
    vampytest.assert_eq(option.channel_ids, tuple(channel_ids))
    vampytest.assert_eq(option.description, description)
    vampytest.assert_eq(option.emoji, emoji)
    vampytest.assert_eq(option.id, option_id)
    vampytest.assert_eq(option.name, name)
    vampytest.assert_eq(option.role_ids, tuple(role_ids))



def test__OnboardingPromptOption__to_data__0():
    """
    Tests whether ``OnboardingPromptOption.to_data`` works as intended.
    
    Case: Include defaults and internals.
    """
    channel_ids = [202302030017, 202302030018]
    description = 'yukari'
    emoji = BUILTIN_EMOJIS['x']
    name = 'yakumo'
    role_ids = [202302030019, 202302030020]
    option_id = 202302030051
    
    option = OnboardingPromptOption.precreate(
        option_id,
        channel_ids = channel_ids,
        description = description,
        emoji = emoji,
        name = name,
        role_ids = role_ids,
    )
    
    expected_output = {
        'channel_ids': [str(channel_id) for channel_id in channel_ids],
        'description': description,
        'emoji': {'name': emoji.unicode},
        'title': name,
        'role_ids': [str(role_id) for role_id in role_ids],
        'id': str(option_id),
    }
    
    vampytest.assert_eq(
        option.to_data(defaults = True, include_internals = True),
        expected_output,
    )

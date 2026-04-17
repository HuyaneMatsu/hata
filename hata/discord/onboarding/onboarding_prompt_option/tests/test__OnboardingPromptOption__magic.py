import vampytest

from ....core import BUILTIN_EMOJIS

from ..onboarding_prompt_option import OnboardingPromptOption


def test__OnboardingPromptOption__repr():
    """
    Tests whether ``OnboardingPromptOption.__repr__`` works as intended.
    """
    channel_ids = [202303030021, 202303030022]
    description = 'yukari'
    emoji = BUILTIN_EMOJIS['x']
    name = 'yakumo'
    role_ids = [202303030023, 202303030024]
    
    option = OnboardingPromptOption(
        channel_ids = channel_ids,
        description = description,
        emoji = emoji,
        name = name,
        role_ids = role_ids,
    )
    
    vampytest.assert_instance(repr(option), str)


def test__OnboardingPromptOption__hash():
    """
    Tests whether ``OnboardingPromptOption.__hash__`` works as intended.
    """
    channel_ids = [202303030025, 202303030026]
    description = 'yukari'
    emoji = BUILTIN_EMOJIS['x']
    name = 'yakumo'
    role_ids = [202303030027, 202303030029]
    
    option = OnboardingPromptOption(
        channel_ids = channel_ids,
        description = description,
        emoji = emoji,
        name = name,
        role_ids = role_ids,
    )
    
    vampytest.assert_instance(hash(option), int)


def test__OnboardingPromptOption__eq():
    """
    Tests whether ``OnboardingPromptOption.__repr__`` works as intended.
    """
    channel_ids = [202303030030, 202303030031]
    description = 'yukari'
    emoji = BUILTIN_EMOJIS['x']
    name = 'yakumo'
    role_ids = [202303030032, 202303030033]
    option_id = 202303030052
    
    keyword_parameters = {
        'channel_ids': channel_ids,
        'description': description,
        'emoji': emoji,
        'name': name,
        'role_ids': role_ids,
    }
    
    option = OnboardingPromptOption.precreate(option_id, **keyword_parameters)
    
    vampytest.assert_eq(option, option)
    vampytest.assert_ne(option, object())
    
    test_option = OnboardingPromptOption(**keyword_parameters)
    vampytest.assert_eq(option, test_option)
    
    for field_name, field_value in (
        ('channel_ids', None),
        ('description', None),
        ('emoji', None),
        ('name', 'ran'),
        ('role_ids', None),
    ):
        test_option = OnboardingPromptOption(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(option, test_option)

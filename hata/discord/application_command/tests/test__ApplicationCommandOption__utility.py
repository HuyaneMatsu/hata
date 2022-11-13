import vampytest

from .. import ApplicationCommandOption, ApplicationCommandOptionType


def test__ApplicationCommandOption__copy():
    """
    Tests whether ``ApplicationCommandOption``'s `copy` method works correctly.
    This test tests string sub-fields.
    """
    option = ApplicationCommandOption(
        'owo', 'owo', ApplicationCommandOptionType.string, min_length = 30, max_length = 60
    )
    
    copy = option.copy()
    
    vampytest.assert_not_is(option, copy)
    vampytest.assert_eq(option, copy)

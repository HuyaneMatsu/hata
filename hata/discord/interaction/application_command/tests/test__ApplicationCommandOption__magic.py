import vampytest

from .. import ApplicationCommandOption, ApplicationCommandOptionType


def test__ApplicationCommandOption__repr_0():
    """
    Tests whether ``ApplicationCommandOption``'s `__repr__` method works correctly.
    This test tests string sub-fields.
    """
    option = ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string, min_length=30, max_length=60)
    vampytest.assert_instance(repr(option), str)


def test__ApplicationCommandOption__eq():
    """
    Tests whether ``ApplicationCommandOption``'s `__eq__` method works correctly.
    This test tests string sub-fields.
    """
    vampytest.assert_eq(
        ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string, min_length=30, max_length=60),
        ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string, min_length=30, max_length=60),
    )
    
    vampytest.assert_not_eq(
        ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string, min_length=30, max_length=60),
        ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string, min_length=30, max_length=59),
    )

    vampytest.assert_not_eq(
        ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string, min_length=30, max_length=60),
        ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string),
    )

import vampytest

from ....channel import ChannelType

from .. import ApplicationCommandOption, ApplicationCommandOptionType
from ..constants import APPLICATION_COMMAND_OPTION_MIN_LENGTH_MAX


def test__ApplicationCommandOption__constructor__0():
    """
    Tests whether ``ApplicationCommandOption`` sets fields correctly.
    """
    name = 'owo'
    description = 'not owo'
    type_ = ApplicationCommandOptionType.string
    max_length = 30
    min_length = 10
    
    option = ApplicationCommandOption(
        name,
        description,
        type_,
        max_length = max_length,
        min_length = min_length
    )
    
    vampytest.assert_eq(option.name, name)
    vampytest.assert_eq(option.description, description)
    vampytest.assert_is(option.type, type_)
    vampytest.assert_eq(option.max_length, max_length)
    vampytest.assert_eq(option.min_length, min_length)


def test__ApplicationCommandOption__constructor__max_length__0():
    """
    Tests whether ``ApplicationCommandOption`` sets `max_length` correctly if not given.
    """
    option = ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string)
    vampytest.assert_eq(option.max_length, 0)


def test__ApplicationCommandOption__constructor__max_length__1():
    """
    Tests whether ``ApplicationCommandOption`` raises when `max_length` is given incorrectly.
    """
    with vampytest.assert_raises(TypeError):
        ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string, max_length='owo')


def test__ApplicationCommandOption__constructor__max_length__2():
    """
    Tests whether ``ApplicationCommandOption`` raises when `max_length` is given, but type is incorrect.
    """
    with vampytest.assert_raises(ValueError):
        ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.integer, max_length=30)


def test__ApplicationCommandOption__constructor__max_length__3():
    """
    Tests whether ``ApplicationCommandOption`` sets `.max_length` correctly if given as the limit.
    """
    option = ApplicationCommandOption(
        'owo',
        'owo',
        ApplicationCommandOptionType.string,
        max_length = APPLICATION_COMMAND_OPTION_MIN_LENGTH_MAX,
    )
    
    vampytest.assert_eq(option.max_length, 0)


def test__ApplicationCommandOption__constructor__min_length__0():
    """
    Tests whether ``ApplicationCommandOption`` sets `min_length` correctly if not given.
    """
    option = ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string)
    vampytest.assert_eq(option.min_length, 0)


def test__ApplicationCommandOption__constructor__min_length__1():
    """
    Tests whether ``ApplicationCommandOption`` raises when `min_length` is given incorrectly.
    """
    with vampytest.assert_raises(TypeError):
        ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string, min_length='owo')


def test__ApplicationCommandOption__constructor__min_length__2():
    """
    Tests whether ``ApplicationCommandOption`` raises when `min_length` is given, but type is incorrect.
    """
    with vampytest.assert_raises(ValueError):
        ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.integer, min_length=30)


def test__ApplicationCommandOption__constructor__channel_types__0():
    """
    Tests whether ``ApplicationCommandOption.__new__`` sets `channel_types` correctly.
    """
    for input_value, expected_value in (
        (None, None),
        ([1, ], (ChannelType.private,)),
        ([], None),
        ([ChannelType.private], (ChannelType.private, )),
        ([ChannelType.private, ChannelType.guild_text], (ChannelType.guild_text, ChannelType.private)),
    ):
        option = ApplicationCommandOption(
            'owo', 'owo', ApplicationCommandOptionType.channel, channel_types = input_value
        )
        vampytest.assert_eq(option.channel_types, expected_value)

import vampytest

from .. import ApplicationCommandOption, ApplicationCommandOptionType


def test__ApplicationCommandOption__constructor__max_length_0():
    """
    Tests whether ``ApplicationCommandOption`` sets `max_length` correctly.
    """
    max_length = 30
    option = ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string, max_length=max_length)
    vampytest.assert_eq(option.max_length, max_length)


def test__ApplicationCommandOption__constructor__max_length_1():
    """
    Tests whether ``ApplicationCommandOption`` sets `max_length` correctly if not given.
    """
    option = ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string)
    vampytest.assert_eq(option.max_length, 0)


def test__ApplicationCommandOption__constructor__max_length_2():
    """
    Tests whether ``ApplicationCommandOption`` raises when `max_length` is given incorrectly.
    """
    with vampytest.assert_raises(TypeError):
        ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string, max_length='owo')


def test__ApplicationCommandOption__constructor__max_length_3():
    """
    Tests whether ``ApplicationCommandOption`` raises when `max_length` is given, but type is incorrect.
    """
    with vampytest.assert_raises(ValueError):
        ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.integer, max_length=30)


def test__ApplicationCommandOption__constructor__min_length_0():
    """
    Tests whether ``ApplicationCommandOption`` sets `min_length` correctly.
    """
    min_length = 30
    option = ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string, min_length=min_length)
    vampytest.assert_eq(option.min_length, min_length)


def test__ApplicationCommandOption__constructor__min_length_1():
    """
    Tests whether ``ApplicationCommandOption`` sets `min_length` correctly if not given.
    """
    option = ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string)
    vampytest.assert_eq(option.min_length, 0)


def test__ApplicationCommandOption__constructor__min_length_2():
    """
    Tests whether ``ApplicationCommandOption`` raises when `min_length` is given incorrectly.
    """
    with vampytest.assert_raises(TypeError):
        ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string, min_length='owo')


def test__ApplicationCommandOption__constructor__min_length_3():
    """
    Tests whether ``ApplicationCommandOption`` raises when `min_length` is given, but type is incorrect.
    """
    with vampytest.assert_raises(ValueError):
        ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.integer, min_length=30)

import vampytest

from ....guild import Guild

from ..fields import validate_guild_id


def test__validate_guild_id__0():
    """
    Tests whether `validate_guild_id` works as intended.
    
    Case: passing.
    """
    guild_id = 202303150002
    
    for input_value, expected_output in (
        (None, 0),
        (guild_id, guild_id),
        (Guild.precreate(guild_id), guild_id),
        (str(guild_id), guild_id)
    ):
        output = validate_guild_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_guild_id__1():
    """
    Tests whether `validate_guild_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_guild_id(input_value)


def test__validate_guild_id__2():
    """
    Tests whether `validate_guild_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_guild_id(input_value)

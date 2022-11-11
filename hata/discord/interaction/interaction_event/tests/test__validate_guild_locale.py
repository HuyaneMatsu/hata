import vampytest

from ....localization import Locale

from ..fields import validate_guild_locale


def test__validate_guild_locale__0():
    """
    Validates whether ``validate_guild_locale`` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (Locale.czech, Locale.czech),
        (Locale.czech.value, Locale.czech)
    ):
        output = validate_guild_locale(input_value)
        vampytest.assert_is(output, expected_output)


def test__validate_guild_locale__1():
    """
    Validates whether ``validate_guild_locale`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_guild_locale(input_value)

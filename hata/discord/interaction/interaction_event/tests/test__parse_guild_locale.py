import vampytest

from ....localization import Locale

from ..fields import parse_guild_locale


def test__parse_guild_locale():
    """
    Tests whether ``parse_guild_locale`` works as intended.
    """
    for input_data, expected_output in (
        ({'guild_locale': Locale.czech.value}, Locale.czech),
    ):
        output = parse_guild_locale(input_data)
        vampytest.assert_is(output, expected_output)

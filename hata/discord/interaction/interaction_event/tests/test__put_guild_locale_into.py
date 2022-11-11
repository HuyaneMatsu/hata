import vampytest

from ....localization import Locale

from ..fields import put_guild_locale_into


def test__put_guild_locale_into():
    """
    Tests whether ``put_guild_locale_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (Locale.czech, False, {'guild_locale': Locale.czech.value}),
    ):
        data = put_guild_locale_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)

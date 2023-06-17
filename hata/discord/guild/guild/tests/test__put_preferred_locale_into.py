import vampytest

from ....localization import Locale

from ..fields import put_preferred_locale_into


def test__put_preferred_locale_into():
    """
    Tests whether ``put_preferred_locale_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (Locale.czech, False, {'preferred_locale': Locale.czech.value}),
    ):
        data = put_preferred_locale_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)

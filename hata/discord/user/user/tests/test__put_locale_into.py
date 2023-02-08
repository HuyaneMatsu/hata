import vampytest

from ....localization import Locale

from ..fields import put_locale_into


def test__put_locale_into():
    """
    Tests whether ``put_locale_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (Locale.czech, False, {'locale': Locale.czech.value}),
    ):
        data = put_locale_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)

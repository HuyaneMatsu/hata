import vampytest

from ....localization import Locale

from ..fields import put_locale


def test__put_locale():
    """
    Tests whether ``put_locale`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (Locale.czech, False, {'locale': Locale.czech.value}),
    ):
        data = put_locale(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)

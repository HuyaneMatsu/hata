import vampytest

from ....localization import Locale
from ....localization.utils import LOCALE_DEFAULT

from ..fields import parse_preferred_locale


def test__parse_preferred_locale():
    """
    Tests whether ``parse_preferred_locale`` works as intended.
    """
    for input_data, expected_output in (
        ({}, LOCALE_DEFAULT),
        ({'preferred_locale': Locale.czech.value}, Locale.czech),
    ):
        output = parse_preferred_locale(input_data)
        vampytest.assert_is(output, expected_output)

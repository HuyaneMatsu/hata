import vampytest

from ....localization import Locale

from ..fields import validate_name_localizations


def test__validate_name_localizations():
    """
    Tests whether ``validate_name_localizations`` works as intended.
    """
    for input_value, expected_output in (
        (None, None),
        ({}, None),
        (
            {
                Locale.dutch: 'aya',
                Locale.greek.value: 'yya',
            },
            {
                Locale.dutch: 'aya',
                Locale.greek: 'yya',
            },
        ),
    ):
        output = validate_name_localizations(input_value)
        vampytest.assert_eq(output, expected_output)        

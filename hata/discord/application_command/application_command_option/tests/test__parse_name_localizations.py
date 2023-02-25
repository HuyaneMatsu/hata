import vampytest

from ....localization import Locale

from ..fields import parse_name_localizations


def test__parse_name_localizations():
    """
    Tests whether ``parse_name_localizations`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'name_localizations': None}, None),
        ({'name_localizations': {}}, None),
        (
            {'name_localizations': {
                Locale.dutch.value: 'aya',
                Locale.greek.value: 'yya',
            }},
            {
                Locale.dutch: 'aya',
                Locale.greek: 'yya',
            },
        ),
    ):
        output = parse_name_localizations(input_data)
        vampytest.assert_eq(output, expected_output)        

import vampytest

from ....localization import Locale

from ..fields import parse_description_localizations


def test__parse_description_localizations():
    """
    Tests whether ``parse_description_localizations`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'description_localizations': None}, None),
        ({'description_localizations': {}}, None),
        (
            {'description_localizations': {
                Locale.dutch.value: 'aya',
                Locale.greek.value: 'yya',
            }},
            {
                Locale.dutch: 'aya',
                Locale.greek: 'yya',
            },
        ),
    ):
        output = parse_description_localizations(input_data)
        vampytest.assert_eq(output, expected_output)        

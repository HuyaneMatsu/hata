import vampytest

from ....localization import Locale

from ..fields import put_description_localizations


def test__put_description_localizations():
    """
    Tests whether ``put_description_localizations`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'description_localizations': None}),
        (
            {
                Locale.dutch: 'aya',
                Locale.greek: 'yya',
            },
            False,
            {'description_localizations': {
                Locale.dutch.value: 'aya',
                Locale.greek.value: 'yya',
            }},
        ),
    ):
        output = put_description_localizations(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)        

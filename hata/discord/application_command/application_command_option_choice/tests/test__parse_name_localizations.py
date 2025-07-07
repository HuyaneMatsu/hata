import vampytest

from ....localization import Locale

from ..fields import parse_name_localizations


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'name_localizations': None,
        },
        None,
    )
    
    yield (
        {
            'name_localizations': {},
        },
        None,
    )
    
    yield (
        {
            'name_localizations': {
                Locale.dutch.value: 'aya',
                Locale.greek.value: 'yya',
            },
        },
        {
            Locale.dutch: 'aya',
            Locale.greek: 'yya',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_name_localizations(input_data):
    """
    Tests whether ``parse_name_localizations`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | dict<Locale, str>``
    """
    output = parse_name_localizations(input_data)
    vampytest.assert_instance(output, dict, nullable = True)
    
    if (output is not None):
        for key, value in output.items():
            vampytest.assert_instance(key, Locale)
            vampytest.assert_instance(value, str)
    
    return output

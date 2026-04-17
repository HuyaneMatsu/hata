import vampytest

from ....localization import Locale

from ..fields import parse_description_localizations


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'description_localizations': None,
        },
        None,
    )
    
    yield (
        {
            'description_localizations': {},
        },
        None,
    )
    
    yield (
        {
            'description_localizations': {
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
def test__parse_description_localizations(input_data):
    """
    Tests whether ``parse_description_localizations`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | dict<Locale, str>``
    """
    return parse_description_localizations(input_data)

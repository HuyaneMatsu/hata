import vampytest

from ....localization import Locale

from ..fields import put_description_localizations


def _iter_options():
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'description_localizations': None,
        },
    )
    
    yield (
        {
            Locale.dutch: 'aya',
            Locale.greek: 'yya',
        },
        False,
        {
            'description_localizations': {
                Locale.dutch.value: 'aya',
                Locale.greek.value: 'yya',
            },
        },
    )
    
    yield (
        {
            Locale.dutch: 'aya',
            Locale.greek: 'yya',
        },
        True,
        {
            'description_localizations': {
                Locale.dutch.value: 'aya',
                Locale.greek.value: 'yya',
            },
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_description_localizations(input_value, defaults):
    """
    Tests whether ``put_description_localizations`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | dict<Locale | str>``
        Value to serialize.
    
    defaults : `bool`
        Whether values as their defaults should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_description_localizations(input_value, {}, defaults)        

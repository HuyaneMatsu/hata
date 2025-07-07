import vampytest

from ....localization import Locale

from ..fields import put_name_localizations


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
            'name': {
                'localizations': None,
            },
        },
    )
    
    yield (
        {
            Locale.dutch: 'aya',
            Locale.greek: 'yya',
        },
        False,
        {
            'name': {
                'localizations': {
                    Locale.dutch.value: 'aya',
                    Locale.greek.value: 'yya',
                },
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
            'name': {
                'localizations': {
                    Locale.dutch.value: 'aya',
                    Locale.greek.value: 'yya',
                },
            },
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_name_localizations(input_value, defaults):
    """
    Tests whether ``put_name_localizations`` works as intended.
    
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
    return put_name_localizations(input_value, {}, defaults)        

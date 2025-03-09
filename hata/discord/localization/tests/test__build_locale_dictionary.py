import vampytest

from ..preinstanced import Locale
from ..utils import build_locale_dictionary


def _iter_options():
    yield (
        None,
        None,
    )
    
    yield (
        {},
        None,
    )
    
    yield (
        {Locale.greek.value: 'miau'},
        {Locale.greek: 'miau'},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_locale_dictionary(dictionary):
    """
    Tests whether ``build_locale_dictionary`` works as intended.
    
    Parameters
    ----------
    dictionary : `None | dict<str, object>`
        The dictionary to process.
    
    Returns
    -------
    output : `None | dict<Locale, object>`

    """
    output = build_locale_dictionary(dictionary)
    
    vampytest.assert_instance(output, dict, nullable = True)
    
    if (output is not None):
        for key, value in output.items():
            vampytest.assert_instance(key, Locale)
            vampytest.assert_instance(value, object)
    
    return output

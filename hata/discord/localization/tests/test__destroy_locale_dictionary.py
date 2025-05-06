import vampytest

from ..preinstanced import Locale
from ..utils import destroy_locale_dictionary


def _iter_options():
    yield (
        None,
        None,
    )
    
    yield (
        {Locale.greek: 'miau'},
        {Locale.greek.value: 'miau'},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__destroy_locale_dictionary(dictionary):
    """
    Tests whether ``destroy_locale_dictionary`` works as intended.
    
    Parameters
    ----------
    dictionary : `None | dict<Locale, object>`
        The dictionary to process.
    
    Returns
    -------
    output : `None | dict<str, object>`

    """
    output = destroy_locale_dictionary(dictionary)
    
    vampytest.assert_instance(output, dict, nullable = True)
    
    if (output is not None):
        for key, value in output.items():
            vampytest.assert_instance(key, str)
            vampytest.assert_instance(value, object)
    
    return output

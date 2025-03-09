__all__ = ()

from .preinstanced import Locale


LOCALE_DEFAULT = Locale.english_us
Locale.INSTANCES[''] = LOCALE_DEFAULT


def build_locale_dictionary(dictionary):
    """
    Builds a locale dictionary where they keys are all ``Locale``-s.
    
    Parameters
    ----------
    dictionary : `None | dict<str, object>`
        The dictionary to process.
    
    Returns
    -------
    transformed : `None | dict<Locale, object>`
    """
    if (dictionary is not None) and dictionary:
        return {Locale(key): value for key, value in dictionary.items()}


def destroy_locale_dictionary(dictionary):
    """
    Builds a json serializable dictionary where they keys are all `str`-s.
    
    Parameters
    ----------
    dictionary : `None w dict<Locale | object>`
        The dictionary to process.
    
    Returns
    -------
    transformed : `None | dict<str, object>`
    """
    if dictionary is not None:
        return {key.value: value for key, value in dictionary.items()}


def hash_locale_dictionary(dictionary):
    """
    Hashes a locale dictionary where they keys are all ``Locale``-s.
    
    Parameters
    ----------
    dictionary : `dict<Locale, object>`
        The dictionary to process.
    
    Returns
    -------
    hash_value : `int`
    """
    hash_value = 0
    
    for key, value in dictionary.items():
        hash_value ^= hash(key.value) & hash(value)
    
    return hash_value

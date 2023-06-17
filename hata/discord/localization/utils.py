__all__ = ()

from .preinstanced import Locale


LOCALE_DEFAULT = Locale.english_us
Locale.INSTANCES[''] = LOCALE_DEFAULT


def build_locale_dictionary(dictionary):
    """
    Builds a locale dictionary where they keys are all ``Locale``-s.
    
    Parameters
    ----------
    dictionary : `dict` of (`str`, `object`) items
        The dictionary to process.
    
    Returns
    -------
    transformed : `dict` of (``Locale``, `object`) items
    """
    if (dictionary is not None) and dictionary:
        return {Locale.get(key): value for key, value in dictionary.items()}


def destroy_locale_dictionary(dictionary):
    """
    Builds a json serializable dictionary where they keys are all `str`-s.
    
    Parameters
    ----------
    dictionary : `dict` of (`Locale`, `object`) items
        The dictionary to process.
    
    Returns
    -------
    transformed : `dict` of (`str`, `object`) items
    """
    if dictionary is not None:
        return {key.value: value for key, value in dictionary.items()}


def hash_locale_dictionary(dictionary):
    """
    Hashes a locale dictionary where they keys are all ``Locale``-s.
    
    Parameters
    ----------
    dictionary : `dict` of (`str`, `object`) items
        The dictionary to process.
    
    Returns
    -------
    hash_value : `int`
    """
    hash_value = 0
    
    for key, value in dictionary.items():
        hash_value ^= hash(key.value) & hash(value)
    
    return hash_value

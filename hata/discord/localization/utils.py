__all__ = ()

from .preinstanced import Locale


DEFAULT_LOCALE = Locale.english_us


def get_locale(value):
    """
    Gets the locale of the given value.
    
    Parameters
    ----------
    value : `None`, `str`
        If given as `None`, returns the default locale.
    
    Returns
    -------
    locale : ``Locale``
    """
    if value is None:
        locale = DEFAULT_LOCALE
    else:
        locale = Locale.get(value)
    
    return locale


def build_locale_dictionary(dictionary):
    """
    Builds a locale dictionary where they keys are all ``Locale``-s.
    
    Parameters
    ----------
    dictionary : `dict` of (`str`, `Any`) items
        The dictionary to process.
    
    Returns
    -------
    transformed : `dict` of (``Locale``, `Any`) items
    """
    if (dictionary is not None) and dictionary:
        return {Locale.get(key): value for key, value in dictionary.items()}


def destroy_locale_dictionary(dictionary):
    """
    Builds a json serializable dictionary where they keys are all `str`-s.
    
    Parameters
    ----------
    dictionary : `dict` of (`Locale`, `Any`) items
        The dictionary to process.
    
    Returns
    -------
    transformed : `dict` of (`str`, `Any`) items
    """
    if dictionary is not None:
        return {key.value: value for key, value in dictionary.items()}


def hash_locale_dictionary(dictionary):
    """
    Hashes a locale dictionary where they keys are all ``Locale``-s.
    
    Parameters
    ----------
    dictionary : `dict` of (`str`, `Any`) items
        The dictionary to process.
    
    Returns
    -------
    hash_value : `int`
    """
    hash_value = 0
    
    for key, value in dictionary.items():
        hash_value ^= hash(key.value) & hash(value)
    
    return hash_value

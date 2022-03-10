__all__ = ('DEFAULT_LOCALE', 'get_locale', 'process_locale_dictionary')

from .preinstanced import Locale

DEFAULT_LOCALE = Locale.english_us


def get_locale(value):
    """
    Gets the locale of the given value.
    
    Parameters
    ----------
    value : `None`, `str`
        If given as `None`, returns teh default locale.
    
    Returns
    -------
    locale : ``Locale``
    """
    if value is None:
        locale = DEFAULT_LOCALE
    else:
        locale = Locale.get(value)
    
    return locale


def process_locale_dictionary(dictionary):
    """
    Processes a locale dictionary, where they keys are locales.
    
    Parameters
    ----------
    dictionary : `dict` of (`str`, `Any`) items
        The dictionary to process.
    
    Returns
    -------
    transformed : `dict` of (``Locale``, `Any`) items
    """
    if dictionary is not None:
        return {Locale.get(key): value for key, value in dictionary.items()}

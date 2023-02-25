__all__ = ()

from ..localization import Locale


def maybe_locale(value):
    """
    Converts the given value to locale if it is not already.
    
    Parameters
    ----------
    value : ``Locale``, `str`
        Value to convert to locale.
    
    Returns
    -------
    locale : ``Locale``
    
    Raises
    ------
    TypeError
        - `value`'s type is neither ``Locale`` nor `str`.
    """
    if isinstance(value, Locale):
        locale = value
    
    elif isinstance(value, str):
        locale = Locale.get(value)
    
    else:
        raise TypeError(
            f'`locale`-s can be `{Locale.__name}`, `str`, got {value.__class__.__name__}; {value!r}.'
        )
    
    return locale


def with_translation(source_value, actual_localized_dictionary, translation_table, replace):
    """
    Applies translation of for the given value to the given localized dictionary from the given translation table.
    
    Parameters
    ----------
    source_value : `None`, `str`
        The value to get translations for.
    actual_localized_dictionary : `None`, `dict` of ((`str`, ``Locale``), `str`) items
        Localized dictionary to apply the translations to.
    translation_table : `dict` of ((``Locale``, `str`), (`None`, `dict` (`str`, (`None`, `str`)) items)) items
        Translation table to pull localizations from.
    replace : `bool`
        Whether actual translation should be replaced.
    
    Returns
    -------
    localized_dictionary : `None`, `dict` of ((`str`, ``Locale``), `str`) items
        New localized dictionary.
    """
    if (actual_localized_dictionary is None):
        new_localized_dictionary = None
    else:
        new_localized_dictionary = actual_localized_dictionary.copy()
    
    if (source_value is not None):
        for locale, relations in translation_table.items():
            if relations is None:
                continue
            
            try:
                translation = relations[source_value]
            except KeyError:
                continue
            
            if translation is None:
                continue
            
            locale = maybe_locale(locale)
            
            if new_localized_dictionary is None:
                new_localized_dictionary = {}
            
            if replace:
                new_localized_dictionary[locale] = translation
            else:
                new_localized_dictionary.setdefault(locale, translation)
    
    return new_localized_dictionary

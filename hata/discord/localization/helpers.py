__all__ = ()

from .preinstanced import Locale



def serializable_localized_item_validator(item, parameter_name):
    """
    Json serializable localization dictionary item validator.
    
    Parameters
    ---------
    key : (Locale | str, str)
        An item representing a `locale` - `str` pair.
    
    parameter_name : `str`
        The parameter's name to raise exception with.
    
    Returns
    -------
    validated_item : `(str, str)`
    
    Raises
    ------
    TypeError
        If `key`'s type is incorrect.
    ValueError
        If `key`'s is an empty string.
    """
    key, value = item
    if isinstance(key, Locale):
        validated_key = key.value
    
    elif isinstance(key, str):
        if not key:
            raise ValueError(
                f'`{parameter_name}` keys cannot be empty strings, got item = {item!r}.'
            )
        
        validated_key = key
    
    else:
        raise TypeError(
            f'`{parameter_name}` keys can be `{Locale.__name__}`, `str`, got {type(value).__name__}; {value!r}; '
            f'item = {item!r}.'
        )
    
    if isinstance(value, str):
        if not value:
            raise ValueError(
                f'`{parameter_name}` values cannot be empty strings, got item = {item!r}.'
            )
        
        validated_value = value
    
    else:
        raise TypeError(
            f'`{parameter_name}` values can be `str`, got {type(value).__name__}; {value!r}; item = {item!r}.'
        )
    
    
    return validated_key, validated_value


def localized_dictionary_item_validator(item, parameter_name):
    """
    Localization dictionary item validator.
    
    Parameters
    ---------
    item : `(Locale | str, str)`
        An item representing a `locale` - `str` pair.
    
    parameter_name : `str`
        The parameter's name to raise exception with.
    
    Returns
    -------
    validated_item : `(Locale, str)`
    
    Raises
    ------
    TypeError
        If `key`'s type is incorrect.
    ValueError
        If `key`'s is an empty string.
    """
    key, value = item
    if isinstance(key, Locale):
        validated_key = key
    
    elif isinstance(key, str):
        if not key:
            raise ValueError(
                f'`{parameter_name}` keys cannot be empty strings, got item = {item!r}.'
            )
        
        validated_key = Locale(key)
    
    else:
        raise TypeError(
            f'`{parameter_name}` keys can be `{Locale.__name__}`, `str`, got {type(value).__name__}; {value!r}; '
            f'item = {item!r}.'
        )
    
    if isinstance(value, str):
        if not value:
            raise ValueError(
                f'`{parameter_name}` values cannot be empty strings, got item = {item!r}.'
            )
        
        validated_value = value
    
    else:
        raise TypeError(
            f'`{parameter_name}` values can be `str`, got {type(value).__name__}; {value!r}; item = {item!r}.'
        )
    
    
    return validated_key, validated_value


def localized_dictionary_builder(dictionary, parameter_name):
    """
    Parameters
    ----------
    dictionary : `None | dict<Locale | str, str> | (set | tuple | list)<(Locale | str, str)>`
        The value to convert to localized dictionary.
    
    parameter_name : `str`
        The parameter's name to raise exception with.
    
    Returns
    -------
    validated_dictionary : ``None | dict<Locale, str>``
    
    Raises
    ------
    TypeError
        - If `dictionary`'s or any of it's item's type is incorrect.
    ValueError
        - Empty key or value.
        - Incorrect item length.
    """
    return _dictionary_builder(dictionary, parameter_name, localized_dictionary_item_validator)


def serializable_localized_dictionary_builder(dictionary, parameter_name):
    """
    Builds a json serializable localized dictionary from the given dictionary.
    
    Parameters
    ----------
    dictionary : `None | dict<Locale | str, str> | (set | tuple | list)<(Locale | str, str)>`
        The value to convert to json serializable localized dictionary.
    
    parameter_name : `str`
        The parameter's name to raise exception with.
    
    Returns
    -------
    validated_dictionary : `None | dict<str, str>`
    
    Raises
    ------
    TypeError
        - If `dictionary`'s or any of it's item's type is incorrect.
    ValueError
        - Empty key or value.
        - Incorrect item length.
    """
    return _dictionary_builder(dictionary, parameter_name, serializable_localized_item_validator)


def _dictionary_builder(dictionary, parameter_name, item_validator):
    """
    Builds a dictionary item validated by the given validator from the given one.
    
    Parameters
    ----------
    dictionary : `None | dict<Locale | str, str> | (set | tuple | list)<(Locale | str, str)>`
        The value to convert.
    
    parameter_name : `str`
        The parameter's name to raise exception with.
    
    item_validator : `FunctionType`
        Item validator to pass every every item to.
    
    Returns
    -------
    validated_dictionary : `None | dict<*return<item_validator>>`
    
    Raises
    ------
    TypeError
        - If `dictionary`'s or any of it's item's type is incorrect.
    ValueError
        - Item structure incorrect.
    """
    if dictionary is None:
        validated_dictionary = None
    
    elif isinstance(dictionary, dict):
        validated_dictionary = {}
        
        for item in dictionary.items():
            key, value = item_validator(item, parameter_name)
            validated_dictionary[key] = value
        
        if not validated_dictionary:
            validated_dictionary = None
    
    elif isinstance(dictionary, (tuple, list, set)):
        validated_dictionary = {}
        for item in dictionary:
            if not isinstance(item, tuple):
                raise TypeError(
                    f'`{parameter_name}` items can be `tuple`-s, got {type(item).__name__}; {item!r}; '
                    f'{parameter_name} = {dictionary!r}.'
                )
            
            
            item_length = len(item)
            if item_length != 2:
                raise ValueError(
                    f'`{parameter_name}` items can be `tuple`-s of length `2`, got {item!r}; length = {item_length!r}; '
                    f'{parameter_name} = {dictionary!r}.'
                )
            
            key, value = item_validator(item, parameter_name)
            validated_dictionary[key] = value
        
        if not validated_dictionary:
            validated_dictionary = None
            
    else:
        raise TypeError(
            f'`{parameter_name}` can be `None`, `dict`, `set`, `tuple`, `list`, '
            f'got {type(dictionary).__name__}; {dictionary!r}.'
        )
    
    return validated_dictionary


def get_localized_length(value, value_localizations):
    """
    Gets the length of the given value and of it's localized values.
    
    If a value has localizations, we only count the longest towards the overall length.
    
    Parameters
    ----------
    value : `None | str`
        The default value.
    
    value_localizations : ``None | dict<Locale, str>``
        Localizations of the value.
    
    Returns
    -------
    length : `int`
    """
    if value is None:
        length = 0
    else:
        length = len(value)
    
    if (value_localizations is not None):
        for value in value_localizations.values():
            length = max(len(value), length)
    
    return length

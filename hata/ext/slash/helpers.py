__all__ = ()

from scarletio import from_json

from ...discord.application_command.helpers import maybe_locale


def validate_translation_table(translation_table):
    """
    Validates the given translation table returning a new one.
    
    Parameters
    ----------
    translation_table : `None`, `str`, `dict` of ((``Locale``, `str`), (`None`,
            `dict` of (`str`, (`None`, `str`)) items)) items
        Translation table for the commands of the slasher.
    
    Returns
    -------
    translation_table : `None`, `dict` of (``Locale``, `dict` of (`str`, `str`) items) items
    
    Raises
    ------
    FileNotFoundError
        - If `translation_table` is a string, but not a file.
    TypeError
        - If `translation_table`'s structure is incorrect.
    """
    if translation_table is None:
        return None
    
    if isinstance(translation_table, str):
        return _validate_translation_table_from_file(translation_table)
    
    if isinstance(translation_table, dict):
        return _validate_translation_table_from_dict(translation_table)
    
    raise TypeError(
        f'`translation_table` can be either `None`, `str`, `dict`, got '
        f'{translation_table.__class__.__name__}, {translation_table!r}'
    )


def _validate_translation_table_from_file(file_name):
    """
    Validates the given translation table opening the given `file_name`.
    
    Parameters
    ----------
    file_name : `str`
        The file's name to open. Can be absolute and relative path too.
    
    Returns
    -------
    translation_table : `None`, `dict` of (``Locale``, `dict` of (`str`, `str`) items) items
    
    Raises
    ------
    FileNotFoundError
        - If the file is not found.
    TypeError
        - If the loaded data structure is incorrect.
    """
    with open(file_name, 'r') as file:
        content = file.read()
    
    # empty file? No problem!
    if not content:
        return None
    
    try:
        json_data = from_json(content)
    finally:
        # Unallocate content if exception occurs
        content = None
    
    # No json? No problem!
    if json_data is None:
        return None
    
    if isinstance(json_data, dict):
        return _validate_translation_table_from_dict(json_data)
    
    raise TypeError(
        f'`translation_table` file can contain either `None` or `dict`, got '
        f'{json_data.__class__.__name__}; {json_data!r}.'
    )


def _validate_translation_table_from_dict(translation_table):
    """
    Validates the given translation table dictionary returning a new one.
    
    Parameters
    ----------
    translation_table : `dict` of ((``Locale``, `str`), `dict` of (`str`, (`None`, `str`)) items) items
        Translation table to validate
    
    Returns
    -------
    validated_translation_table : `None`, `dict` of (``Locale``, (`None`, `dict` of (`str`, `str`) items)) items
    
    Raises
    ------
    TypeError
        - If `translation_table`'s structure is incorrect.
    """
    validated_translation_table = None
    
    for locale, relations in translation_table.items():
        locale = maybe_locale(locale)
        relations = _validate_translation_table_relations(relations)
        
        if not relations:
            continue
        
        if validated_translation_table is None:
            validated_translation_table = {}
        
        validated_translation_table[locale] = relations
    
    return validated_translation_table


def _validate_translation_table_relations(relations):
    """
    Validates the given translation table's relations.
    
    Parameters
    ----------
    relations : `None`, `dict` of (`str`, (`None`, `str`)) items
        Relations to validate.
    
    Returns
    -------
    validated_relations : `None`, `dict` of (`str`, `str`) items
    
    Raises
    ------
    TypeError
        - If `relations`'s type or structure is incorrect.
    """
    if relations is None:
        return None
    
    if isinstance(relations, dict):
        return _validate_translation_table_relations_dict(relations)
    
    raise TypeError(
        f'`translation_table`\'s keys (also known as relations) can be `None`, `dict`, got '
        f'{relations.__class__.__name__}; {relations!r}.'
    )


def _validate_translation_table_relations_dict(relations):
    """
    
    Parameters
    ----------
    relations : `dict` of (`str`, (`None`, `str`)) items
        Relations to validate.
    
    Returns
    -------
    validated_relations : `None`, `dict` of (`str`, `str`) items

    Raises
    ------
    TypeError
        - If an item's structure is incorrect.
    """
    validated_relations = None
    
    for key, value in relations.items():
        if not isinstance(key, str):
            raise TypeError(
                f'`relation` keys can be `str`, got {key.__class__.__name__}; {key!r}.'
            )
        
        if value is None:
            continue
        
        if not isinstance(value, str):
            raise TypeError(
                f'`relation` values can be `str`, got {value.__class__.__name__}; {value!r}.'
            )
        
        if (not key) or (not value):
            continue
        
        if validated_relations is None:
            validated_relations = {}
        
        validated_relations[key] = value
        continue
    
    return validated_relations

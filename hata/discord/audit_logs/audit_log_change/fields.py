__all__ = ()


# attribute_name

def validate_attribute_name(attribute_name):
    """
    Validates the given audit log change attribute name.
    
    Parameters
    ----------
    attribute_name : `None | str`
        Attribute name to validate.
    
    Returns
    -------
    attribute_name : `str`
    
    Raises
    ------
    TypeError
        - `attribute_name` is not `None`, `str`.
    ValueError
        - `attribute_name` is not identifier.
    """
    if attribute_name is None:
        return ''
    
    if not isinstance(attribute_name, str):
        raise TypeError(
            f'`attribute_name` can be `None`, `str`, got {attribute_name.__class__.__name__}; {attribute_name!r}.'
        )
    
    if attribute_name and (not attribute_name.isidentifier()):
        raise ValueError(f'`attribute_name` can be an identifier, got {attribute_name!r}.')
    
    return attribute_name


# flags

def validate_flags(flags):
    """
    Validates the given audit log change flags.
    
    Parameters
    ----------
    flags : `None | int`
        Flags to validate.
    
    Returns
    -------
    flags : `int`
    
    Raises
    ------
    TypeError
        - `flags` is not `int`.
    ValueError
        - `flags` is negative.
    """
    if flags is None:
        return 0
    
    if not isinstance(flags, int):
        raise TypeError(f'`flags` can be `int`, got {flags.__class__.__name__}; {flags!r}.')
    
    if flags < 0:
        raise ValueError(f'`flags` can not be negative, got {flags!r}.')
    
    return flags

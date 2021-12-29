__all__ = ()


def raw_name_to_display(raw_name):
    """
    Converts the given raw command or it's parameter's name to it's display name.
    
    Parameters
    ----------
    raw_name : `str`
        The name to convert.
    
    Returns
    -------
    display_name : `str`
        The converted name.
    """
    return '-'.join([w for w in raw_name.strip('_ ').lower().replace(' ', '-').replace('_', '-').split('-') if w])


def normalize_description(description):
    """
    Normalizes a docstrings.
    
    Parameters
    ----------
    description : `str`, `Any`
        The docstring to clear.
    
    Returns
    -------
    cleared : `str`, `Any`
        The cleared docstring. If `docstring` was given as `None` or is detected as empty, will return `None`.
    """
    if (description is None) or (not isinstance(description, str)):
        return description
    
    lines = description.splitlines()
    for index in reversed(range(len(lines))):
        line = lines[index]
        line = line.strip()
        if line:
            lines[index] = line
        else:
            del lines[index]
    
    if not lines:
        return None
    
    return ' '.join(lines)

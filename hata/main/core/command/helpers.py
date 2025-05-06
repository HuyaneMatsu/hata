__all__ = ('command_sort_key', 'normalize_command_name',)


def normalize_command_name(command_name):
    """
    Normalises the given command name.
    
    Parameters
    ----------
    command_name : `str`
        The command name to normalize.
    
    Returns
    -------
    command_name : `str`
        The command's name.
    """
    return '-'.join(command_name.lower().replace('_', ' ').replace('-', ' ').split())


def get_function_name(function, name):
    """
    Tries to get the given function's name.
    
    Parameters
    ----------
    function : `object`
        The function to get it's name.
    name : `None`, `str`
        Alternative name to use if given.
    
    Returns
    -------
    name : `str`
    """
    if name is None:
        try:
            name = function.__name__
        except AttributeError:
            name = type(function).__name__
    
    return normalize_command_name(name)


def normalize_command_description(description):
    """
    Normalizes the given description.
    
    Parameters
    ----------
    description : `None`, `str`
        The description to normalise.
    
    Returns
    -------
    description : `None`, `str`
    """
    if description is None:
        return description
    
    lines = description.split('\n')
    if not lines:
        return None
    
    for index in range(len(lines)):
        lines[index] = lines[index].rstrip()
    
    indentation_to_remove = 0
    
    while True:
        for line in lines:
            if len(line) <= indentation_to_remove:
                continue
            
            if line[indentation_to_remove] in (' ', '\t'):
                continue
            
            break
        
        else:
            indentation_to_remove += 1
            continue
        
        break
    
    
    for index in range(len(lines)):
        lines[index] = lines[index][indentation_to_remove:]
    
    while True:
        if lines[-1]:
            break
        
        del lines[-1]
        if not lines:
            return None
    
    while True:
        if lines[0]:
            break
        
        del lines[0]
        continue
    
    # Add postprocessing modifications / line if required
    documentation_parts = []
    index = 0
    line_count = len(lines)
    
    while True:
        documentation_parts.append(lines[index])
        
        index += 1
        if index == line_count:
            break
        
        documentation_parts.append('\n')
        continue
    
    return ''.join(documentation_parts)


def get_function_description(function, description):
    """
    Tries to get the given function's description.
    
    Parameters
    ----------
    function : `object`
        The function to get it's description.
    description : `None`, `str`
        Alternative description to use if given.
    
    Returns
    -------
    description : `None`, `str`
    """
    if description is None:
        try:
            description = function.__doc__
        except AttributeError:
            description = None
    
    return normalize_command_description(description)


def normalize_aliases(aliases, name):
    """
    Tries to normalize the given
    
    Parameters
    ----------
    aliases : `None | str | iterable<str>`
        Alternative names for the command.
    name : `str`
        The command's name.
    
    Returns
    -------
    normalized_aliases : `None`, `str` of `str`
    """
    if aliases is None:
        return None
    
    
    if isinstance(aliases, str):
        alter = normalize_command_name(aliases)
        if alter == name:
            return None
        
        return {alter}
    
    
    iterator = getattr(aliases, '__iter__', None)
    if iterator is None:
        raise TypeError(
            f'`aliases` can be `None | str | iterable<str>`, got {type(aliases).__name__}; {aliases!r}.'
        )
    
    normalized_aliases = None
    
    for alter in aliases:
        if not isinstance(alter, str):
            raise TypeError(
                f'`aliases` elements can be `str`, got {alter.__class__.__name__}; {alter!r}; aliases={aliases!r}.'
            )
        
        alter = normalize_command_name(aliases)
        if alter == name:
            continue
        
        if (normalized_aliases is None):
            normalized_aliases = set()
        
        normalized_aliases.add(alter)
    
    
    return normalized_aliases


def command_sort_key(command):
    """
    Sort key used to sort commands by name.
    
    Parameters
    ----------
    command : ``Command``, ``CommandCategory``, ``CommandFunction``
        Command to get it's sort key of.
    
    Returns
    -------
    sort_key : `str`
    """
    name = command.name
    if name is None:
        name = ''
    
    return name

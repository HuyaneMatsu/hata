__all__ = ()

from os.path import basename as base_name


def _split_part_by_numbers(part):
    """
    Splits the given string part by numbers. Used by ``_split_bot_name_to_words``.
    
    This function is an iterable generator.
    
    Examples
    --------
    ```py
    325 -> 325
    koishi -> koishi
    koishi3 -> koishi, 3
    3koishi -> 3, koishi
    46koishi12satori -> 46, satori, 12, satori
    ```
    
    Parameters
    ----------
    part : `str`
        String part.
    
    Yields
    ------
    part : `str`
    """
    previous_characters = []
    
    for character in part:
        if previous_characters and previous_characters[-1].isnumeric() != character.isnumeric():
            yield ''.join(previous_characters)
            previous_characters.clear()
        
        previous_characters.append(character)
        continue
    
    if previous_characters:
        yield ''.join(previous_characters)


def _split_part_by_casing(part):
    """
    Splits the given string parts by casing. Used by ``_split_bot_name_to_words``.
    
    This function is an iterable generator.
    
    Examples
    --------
    ```py
    koishi -> koishi
    KOISHI -> KOISHI
    Koishi -> Koishi
    koishiSatori -> koishi, Satori
    KOISHISatori -> KOISHI, Satori
    koishiSATORI -> koishi, SATORI
    KOISHIsatori -> KOISH, Isatori # There is a limit how much we can do
    ```
    
    Parameters
    ----------
    part : `str`
        String part.
    
    Yields
    ------
    part : `str`
    """
    previous_characters = []
    
    for character in part:
        if previous_characters:
            if character.isupper():
                if not previous_characters[-1].isupper():
                    yield ''.join(previous_characters)
                    previous_characters.clear()
            
            else:
                if previous_characters[-1].isupper() and len(previous_characters) > 1:
                    yield ''.join(previous_characters[:-1])
                    del previous_characters[:-1]
        
        previous_characters.append(character)
        continue
    
    if previous_characters:
        yield ''.join(previous_characters)


def _split_bot_name_to_words(bot_name):
    """
    Splits the given name to words. Used by ``get_bot_module_name``, ``get_bot_variable_name`` and
    ``get_bot_constant_name``.
    
    This function is an iterable generator.
    
    Examples
    --------
    ```py
    koishi_satori_69 -> koishi, satori, 69
    KoishiSatori69 -> Koishi, Satori, 69
    KOISHI_SATORI_69 -> KOISHI, Satori, 69
    KOISHISATORI69 -> KOISHISATORI, 69 # there is a limit how much we can do
    ```
    
    Parameters
    ----------
    bot_name : `str`
        A bot's name.
    
    Yields
    ------
    word : `str`
    """
    for part in bot_name.split('_'):
        if part:
            for part in _split_part_by_numbers(part):
                yield from _split_part_by_casing(part)


def get_bot_module_name(bot_name):
    """
    Creates bot module name.
    
    Parameters
    ----------
    bot_name : `str`
        A bot's name.
    
    Returns
    -------
    module_name : `str`
    """
    return '_'.join([part.lower() for part in _split_bot_name_to_words(bot_name)])
    

def get_bot_variable_name(bot_name):
    """
    Creates bot variable name.
    
    Parameters
    ----------
    bot_name : `str`
        A bot's name.
    
    Returns
    -------
    variable_name : `str`
    """
    return ''.join([part.capitalize() for part in _split_bot_name_to_words(bot_name)])


def get_bot_constant_name(bot_name):
    """
    Creates bot constant name.
    
    Parameters
    ----------
    bot_name : `str`
        A bot's name.
    
    Returns
    -------
    constant_name : `str`
    """
    return '_'.join([part.upper() for part in _split_bot_name_to_words(bot_name)])


def get_bot_display_name(bot_name):
    """
    Creates the bot's display name.
    
    Parameters
    ----------
    bot_name : `str`
        A bot's name.
    
    Returns
    -------
    display_name : `str`
    """
    return ' '.join([part.capitalize() for part in _split_bot_name_to_words(bot_name)])


def get_project_module_name(project_name):
    """
    Gets the project's name.
    
    Parameters
    ----------
    project_name : `str`
        The project's name.
    
    Returns
    -------
    project_module_name : `str`
    """
    return get_bot_module_name(project_name)

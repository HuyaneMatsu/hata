__all__ = ()

import re

ENUM_EXPECTED_NAME_PARTS = (
    'type',
    'style',
    'behavior',
    'state',
    'level',
)

ENUM_EXPECTED_INT_MIN_VALUE = 0
ENUM_EXPECTED_INT_MAX_VALUE = 65
ENUM_EXPECTED_STR_MIN_LENGTH = 1
ENUM_EXPECTED_STR_MAX_LENGTH = 128

ENUM_GUESS_CHANCE_MAX = 2

def guess_is_enum(name, value):
    """
    Guesses whether the given value can be an enum.
    
    Parameters
    ----------
    name : `str`
        The parameter's name.
    value : `Any`
        The received value.
    
    Returns
    -------
    chance : `int`
    """
    if isinstance(value, str):
        if (not value.isupper()) and (not value.isupper()):
            return -1
        
        value_length = len(value)
        if (value_length < ENUM_EXPECTED_STR_MIN_LENGTH):
            return -1
        
        if (value_length > ENUM_EXPECTED_STR_MAX_LENGTH):
            return -1
        
        chance = 1
    
    elif isinstance(value, int):
        if (value < ENUM_EXPECTED_INT_MIN_VALUE):
            return -1
        
        if (value > ENUM_EXPECTED_INT_MAX_VALUE):
            return -1
        
        chance = 1
    
    else:
        return -1
    
    for expected_name_part in ENUM_EXPECTED_NAME_PARTS:
        if expected_name_part in name:
            chance += 1
            break
    
    return chance

AVATAR_RP = re.compile('(?:a_)?[0-9a-f]{32}')

ICON_EXPECTED_NAME_PARTS = (
    'icon',
    'avatar',
    'banner',
    'splash',
)

ICON_GUESS_CHANCE_MAX = 2

def guess_is_icon(name, value):
    """
    Guesses whether the given value is an icon.
    
    Parameters
    ----------
    name : `str`
        The parameter's name.
    value : `Any`
        The received value.
    
    Returns
    -------
    chance : `int`
    """
    if value is None:
        # Icons default to `0`
        chance = 0
    
    elif isinstance(value, str):
        if value:
            if (AVATAR_RP.fullmatch(value) is None):
                return -1
            
            chance = 1
        else:
            # Deprecated icon strings might be set as empty value.
            chance = 0
        
    else:
        return -1
    
    for expected_name_part in ICON_EXPECTED_NAME_PARTS:
        if expected_name_part in name:
            chance += 1
            break
    
    return chance

COLOR_EXPECTED_NAME_PARTS = (
    'color',
)

COLOR_EXPECTED_MIN_VALUE = 0x000000
COLOR_EXPECTED_MAX_VALUE = 0xffffff

COLOR_GUESS_MAX = 2

def guess_is_color(name, value):
    """
    Guesses whether the given value is a color.
    
    Parameters
    ----------
    name : `str`
        The parameter's name.
    value : `Any`
        The received value.
    
    Returns
    -------
    chance : `int`
    """
    if value is None:
        # Colors might default to `None` at cases
        chance = 0
    
    elif isinstance(value, int):
        if value < COLOR_EXPECTED_MIN_VALUE:
            return -1
        
        if value > COLOR_EXPECTED_MAX_VALUE:
            return -1
        
        chance = 1
    
    else:
        return -1
    
    for expected_name_part in COLOR_EXPECTED_NAME_PARTS:
        if expected_name_part in name:
            chance += 1
            break
    
    return chance


SNOWFLAKE_EXPECTED_NAMES_PART = (
    'id',
)

SNOWFLAKE_EXPECTED_STRING_MIN_VALUE = 1<<21
SNOWFLAKE_EXPECTED_STRING_MAX_VALUE = (1<<64)-1

SNOWFLAKE_EXPECTED_INT_MIN_VALUE = 0
SNOWFLAKE_EXPECTED_INT_MAX_VALUE = (1<<64)-1

SNOWFLAKE_GUESS_MAX = 3


def guess_is_snowflake(name, value):
    """
    Guesses whether the given value is a snowflake.
    
    Parameters
    ----------
    name : `str`
        The parameter's name.
    value : `Any`
        The received value.
    
    Returns
    -------
    chance : `int`
    """
    if value is None:
        # Snowflake can be `None` at cases. The wrapper uses `0` at these cases
        chance = 0
    
    elif isinstance(value, str):
        if not value.isdecimal():
            return -1
        
        value = int(value)
        if value < SNOWFLAKE_EXPECTED_STRING_MIN_VALUE:
            return -1
        
        if value > SNOWFLAKE_EXPECTED_STRING_MAX_VALUE:
            return -1
        
        chance = 2
    
    elif isinstance(value, int):
        if value < SNOWFLAKE_EXPECTED_INT_MIN_VALUE:
            return -1
        
        if value > SNOWFLAKE_EXPECTED_INT_MAX_VALUE:
            return -1
        
        chance = 1
    
    else:
        return -1
    
    for expected_name_part in SNOWFLAKE_EXPECTED_NAMES_PART:
        if expected_name_part in name:
            chance += 1
            break
    
    return chance


STRING_EXPECTED_NAMES_PART = (
    'description',
    'label',
    'name',
    'value',
    'text',
    'default',
    'placeholder',
    
)


STRING_GUESS_MAX = 2

def guess_is_string_field(name, value):
    """
    Guesses whether the given value is a string field.
    
    Parameters
    ----------
    name : `str`
        The parameter's name.
    value : `Any`
        The received value.
    
    Returns
    -------
    chance : `int`
    """
    if value is None:
        chance = 0
    
    elif isinstance(value, str):
        chance = 1
    
    else:
        return -1
    
    for expected_name_part in STRING_EXPECTED_NAMES_PART:
        if expected_name_part in name:
            chance += 1
            break
    
    return chance


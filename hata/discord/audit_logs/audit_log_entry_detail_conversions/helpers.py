__all__ = ()


def convert_string_to_integer(value):
    """
    Helper function to convert strings to integers, as since shitcord supposedly gives us ints as strings.
    
    Parameters
    ----------
    value : `object`
    
    Returns
    -------
    converted : `int`
    """
    while True:
        if value is None:
            converted = 0
            break
        
        if isinstance(value, int):
            converted = value
            break
        
        if isinstance(value, str):
            if value.isdecimal():
                converted = int(value)
                break
            
            converted = 0
            break
        
        converted = 0
        break
    
    return converted


def convert_string_to_boolean(value):
    """
    Helper function to convert strings to booleans, as since shitcord supposedly gives us booleans as strings.
    
    Parameters
    ----------
    value : `object`
    
    Returns
    -------
    converted : `int`
    """
    while True:
        if value is None:
            converted = False
            break
        
        if isinstance(value, bool):
            converted = value
            break
        
        if isinstance(value, str):
            converted = (value == "1")
            break
        
        converted = False
        break
    
    return converted


def serialise_integer_to_string(value):
    """
    Serialises the integer value to string.
    
    Parameters
    ----------
    value : `int`
    
    Returns
    -------
    serialised : `str`
    """
    return str(value)


def serialise_boolean_to_string(value):
    """
    Serialises the boolean to string.
    
    Parameters
    ----------
    value : `int`
    
    Returns
    -------
    serialised : `str`
    """
    return ("1" if value else "0")

__all__ = ()

ENUM_EXPECTED_NAME_POSTFIXES = (
    '_type',
    '_style',
    '_behavior',
    '_state',
    '_level',
)

ENUM_EXPECTED_INT_MIN_VALUE = 0
ENUM_EXPECTED_INT_MAX_VALUE = 65
ENUM_EXPECTED_STR_MIN_LENGTH = 1
ENUM_EXPECTED_STR_MAX_LENGTH = 128

def guess_is_enum(name, value):
    """
    Guesses whether the given value can be an enum.
    
    Parameters
    ----------
    name : `str`
        The parameter's name.
    value : `Any`
        The received value.
    """
    if isinstance(value, str):
        if (not value.isupper()) and (not value.isupper()):
            return 0.0
        
        value_length = len(value)
        if (value_length < ENUM_EXPECTED_STR_MIN_LENGTH):
            return 0.0
        
        if (value_length > ENUM_EXPECTED_STR_MAX_LENGTH):
            return 0.0
        
        chance = 0.4
    
    elif isinstance(value, int):
        if (value < ENUM_EXPECTED_INT_MIN_VALUE):
            return 0.0
        
        if (value > ENUM_EXPECTED_INT_MAX_VALUE):
            return 0.0
        
        chance = 0.4
    
    else:
        return 0.0
    
    for expected_name_postfix in ENUM_EXPECTED_NAME_POSTFIXES:
        if name.endswith(expected_name_postfix):
            chance += 0.4
            break
    
    return chance

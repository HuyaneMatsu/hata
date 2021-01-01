# -*- coding: utf-8 -*-
from .color import Color

def preconvert_snowflake(snowflake, name):
    """
    Converts the given `snowflake` to an acceptable value by the wrapper.
    
    Parameters
    ----------
    snowflake : `str` or `int`
        The snowflake to convert.
    name : `str`
        The name of the snowflake.
    
    Returns
    -------
    snowflake : `int`
    
    Raises
    ------
    TypeError
        - If `snowflake` was not passed neither as `int` or as `str` instance.
    ValueError
        - If `snowflake` was passed as `str` and cannot be converted to `int`.
        - If the converted `snowflake` is negative or it's bit length is over 64.
    """
    snowflake_type = snowflake.__class__
    if snowflake_type is int:
        pass
    if issubclass(snowflake_type, int):
        snowflake = int(snowflake)
    # JSON uint64 is str
    elif issubclass(snowflake_type, str):
        if 6 < len(snowflake) < 21 and snowflake.isdigit():
            snowflake = int(snowflake)
        else:
            raise ValueError(f'`{name}` can be passed as `int` or `str` instance, got `str` instance, but not a valid'
                f'snowflake (7-20 length, digit only), got {snowflake!r}.')
    else:
        raise TypeError(f'`{name}` can be passed as `int` or `str` instance, got {snowflake_type.__name__}.')
    
    if snowflake < 0 or snowflake > ((1<<64)-1):
        raise ValueError(f'`{name}` can be only uint64, got {snowflake!r}.')
    
    return snowflake

def preconvert_discriminator(discriminator):
    """
    Converts the given `discriminator` to an acceptable value by the wrapper.
    
    Parameters
    ----------
    discriminator : `str` or `int`
        The discriminator of an user to convert.
    
    Returns
    -------
    discriminator : `int`
    
    Raises
    ------
    TypeError
        If `discriminator` was not passed neither as `int` or as `str` instance.
    ValueError
        - If `discriminator` was passed as `str` and it is not numerical or it's length is over `4`.
        - If the `discriminator`'s value is less than `0` or is over than `9999`.
    """
    if (type(discriminator) is int):
        pass
    elif isinstance(discriminator, int):
        discriminator = int(discriminator)
    # Discord sends `discriminator` as `str`, so lets accept that as well.
    elif isinstance(discriminator, str):
        if 0<len(discriminator) < 5 and discriminator.isdigit():
            raise ValueError(f'`discriminator` was given as a `str` instance, but it is not numerical or it\'s length '
                 f'is over `4`, got {discriminator!r}')
        discriminator = int(discriminator)
    else:
        raise TypeError(f'`discriminator` can be passed as `int` or `str` instance, got '
            f'{discriminator.__class__.__name__}.')
    
    if discriminator < 0 or discriminator > 9999:
        raise ValueError(f'`discriminator` can be between 0 and 9999, got got {discriminator!r}.')
    
    return discriminator

def preconvert_color(color):
    """
    Converts the given `color` to an acceptable value by the wrapper.
    
    Parameters
    ----------
    color : `int`
        The color to convert.
    
    Returns
    -------
    color : `Color`
    
    Raises
    ------
    TypeError
        If `color` was not passed as `int` instance.
    ValueError
        If the `color`'s value is less than `0` or is over than `0xffffff`.
    """
    if type(color) is Color:
        pass
    elif isinstance(color, int):
        color = Color(color)
    else:
        raise TypeError(f'`color` can be `{Color.__name__}` or `int` instance, got {color.__class__.__name__}.')
    
    if color < 0 or color > 0xffffff:
        raise ValueError(f'`color` can be between 0 and 0xffffff, got {color!r}.')
    
    return color

def preconvert_str(value, name, lower_limit, upper_limit):
    """
    Converts the given `value` to an acceptable string by the wrapper.
    
    Parameters
    ----------
    value : `str`
        The string to convert,
    name : `str`
        The name of the value.
    lower_limit : `int`
        The minimal length of the string.
    upper_limit : `int`
        The maximal length of the string.
    
    Returns
    -------
    value : `str`
    
    Raises
    ------
    TypeError
        If `value` was not passed as `str` instance.
    ValueError
        If the `value`'s length is less than the given `lower_limit` or is higher than the given than the given
        `upper_limit`.
    """
    if type(value) is str:
        pass
    elif isinstance(value, str):
        value = str(value)
    else:
        raise TypeError(f'`{name}` can be `str` instance, got {value.__class__.__name__}.')
    
    length = len(value)
    if (length != 0) and (length < lower_limit or length > upper_limit):
        raise ValueError(f'`{name}` can be between length {lower_limit} and {upper_limit}, got {value!r}.')
    
    return value

def preconvert_bool(value, name):
    """
    Converts the given `value` to an acceptable boolean by the wrapper.
    
    Parameters
    ----------
    value : `int`
        The value to convert.
    name : `str`
        The name of the value.
    
    Returns
    -------
    value : `str`
    
    Raises
    ------
    TypeError
        If `value` was not passed as `int` instance.
    ValueError
        If value was passed as an `int` instance, but not as `0` or `1` either.
    """
    if (type(value) is bool):
        pass
    elif isinstance(value, int):
        if (value not in (0, 1)):
            raise ValueError(f'`{name}` was given as `int` instance, but neither as `0` or `1`, got {value!r}.')
        value = bool(value)
    else:
        raise TypeError(f'`{name}` can be `bool` or `int` instance as `0` or `1`, got {value.__class__.__name__}.')
    
    return value

def preconvert_flag(flag, name, type_):
    """
    Converts the given `flag` to an acceptable flag by the wrapper.
    
    Parameters
    ----------
    flag : `int`
        The flag to convert.
    name : `str`
        The name of the flag.
    type_ : `int` subtype
        The type of the output flag.
    
    Returns
    -------
    flag : `type_`
    
    Raises
    ------
    TypeError
        If `flag` was not given as `int` instance.
    ValueError
        If `flag` was given as `int` instance, but it's value is less than `0` or it's bit length is over `64`.
    """
    flag_type = flag.__class__
    if (flag_type is type_):
        pass
    elif issubclass(flag_type, int):
        flag = type_(flag)
    else:
        raise TypeError(f'`{name}` can be passed as `{type_.__name__}` instance, got {flag_type.__name__}.')
    
    if flag < 0 or flag > ((1<<64)-1):
        raise ValueError(f'`{name}` can be only uint64, got {flag!r}.')
    
    return flag

def preconvert_preinstanced_type(value, name, type_):
    """
    Converts the given `value` to an acceptable value by the wrapper.
    
    Parameters
    ----------
    value : `Any`
        The value to convert.
    name : `str`
        The name of the value.
    type_ : ``PreinstancedBase`` instance
        The preinstanced type.
    
    Returns
    -------
    value : ``PreinstancedBase`` instance
    
    Raises
    ------
    TypeError
        If `value` was not given as `type_` instance, neither as `type_.value`'s type's instance.
    ValueError
        If there is no preinstanced object for the given `value`.
    """
    value_type = value.__class__
    if (value_type is not type_):
        value_expected_type = type_.VALUE_TYPE
        if value_type is value_expected_type:
            pass
        elif issubclass(value_type, value_expected_type):
            value = value_expected_type(value)
        else:
            raise TypeError(f'`{name}` can be passed as {type_.__name__} or as {value_expected_type.__name__} '
                f'instance, got {value_type.__name__}.')
        
        try:
            value = type_.INSTANCES[value]
        except LookupError:
            raise ValueError(f'There is no predefined `{name}` for the following value: {value!r}.') from None
    
    return value

def preconvert_int(value, name, lower_limit, upper_limit):
    """
    Converts the given `value` to an acceptable integer by the wrapper.
    
    Parameters
    ----------
    value : `Any`
        The value to convert.
    name : `str`
        The name of the value.
    lower_limit : `int`
        The minimal value of `value`.
    upper_limit : `int`
        The maximal value of `value`.
    
    Returns
    -------
    value : `int`
    
    Raises
    ------
    TypeError
        If `value` was not given as `int` instance.
    ValueError
        If `value` is less than `lower_limit`, or is higher than the `upper_limit`.
    """
    if type(value) is int:
        pass
    elif isinstance(value, int):
        value = int(value)
    else:
        raise TypeError(f'`{name}` can be `int` instance, got {value.__class__.__name__}.')
    
    if value < lower_limit or value > upper_limit:
        raise ValueError(f'`{name}` can be between {lower_limit} and {upper_limit}, got {value!r}.')
    
    return value

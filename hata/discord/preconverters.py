# -*- coding: utf-8 -*-
from .color import Color

def preconvert_image_hash(value, name):
    if value is None:
        return 0
    
    if type(value) is int:
        pass
    elif isinstance(value,int):
        value = int(value)
    elif isinstance(value,str):
        try:
            value = int(value,16)
        except ValueError as err:
            raise ValueError(f'Cannot convert `{name}` value: {value!r} to `int` with base of 16.') from err
    else:
        raise TypeError(f'`{name}` can be `NoneType`, `str` or `int` type, got {value.__class__.__name__}.')
    
    if value<0 or value.bit_length()>128:
        raise ValueError(f'`{name}` cannot be negative or longer than 128 bits, got {value!r}.')
        
    return value

def preconvert_animated_image_hash(value, animated, name_1, name_2):
    if (type(animated) is not bool):
        # Edge case, animated is 0 or 1 ?
        if isinstance(animated,int) and (animated in (0,1)):
            animated = bool(animated)
        else:
            raise TypeError(f'`{name_2}` can be type `bool`, got {animated.__class__.__name__}.')
    
    if value is None:
        return 0, False
    
    if type(value) is int:
        pass
    elif isinstance(value,int):
        value = int(value)
    elif isinstance(value,str):
        if value.startswith('a_'):
            value = value[2:]
            animated = True
        
        try:
            value = int(value,16)
        except ValueError as err:
            raise ValueError(f'Cannot convert `{name_1}` value: {value!r} to `int` with base of 16.') from err
    
    else:
        raise TypeError(f'`{name_1}` can be `NoneType`, `str` or `int` type, got {value.__class__.__name__}.')
    
    if value<0 or value.bit_length()>128:
        raise ValueError(f'`{name_1}` cannot be negative or longer than 128 bits, got {value!r}.')
    
    return value, animated

def preconvert_snowflake(snowflake, name):
    if (type(snowflake) is int):
        pass
    if isinstance(snowflake,int):
        snowflake=int(snowflake)
    # JSON uint64 is str
    elif isinstance(snowflake,str) and 6<len(snowflake)<18 and snowflake.isdigit():
        snowflake = int(snowflake)
    else:
        raise TypeError(f'`{name}` can be passed as `int` instance, got {snowflake.__class__.__name__}.')
    
    if snowflake < 0 or snowflake.bit_length()>64:
        raise ValueError(f'`{name}` can be only uint64, got {snowflake!r}.')
    
    return snowflake

def preconvert_discriminator(discriminator):
    if (type(discriminator) is int):
        pass
    elif isinstance(discriminator, int):
        discriminator = int(discriminator)
    # Discord sends `discriminator` as `str`, so lets accept that as well.
    elif isinstance(discriminator, str) and 0<len(discriminator)<5 and discriminator.isdigit():
        discriminator = int(discriminator)
    else:
        raise TypeError(f'`discriminator` can be passed as `int` instance, got {discriminator.__class__.__name__}.')
    
    if discriminator<0 or discriminator>9999:
        raise ValueError(f'`discriminator` can be between 0 and 9999, got got {discriminator!r}.')
    
    return discriminator

def preconvert_color(color):
    if type(color) is Color:
        pass
    elif isinstance(color, int):
        color = Color(color)
    else:
        raise TypeError(f'`color` can be `{Color.__name__}` or `int` instance, got {color.__class__.__name__}.')
    
    if color<0 or color>0xffffff:
        raise ValueError(f'`color` can be between 0 and 0xffffff, got {color!r}.')
    
    return color

def preconvert_str(value, name, lower_limit, upper_limit):
    if type(value) is str:
        pass
    elif isinstance(value,str):
        value = str(value)
    else:
        raise TypeError(f'`{name}` can be `str` instance, got {value.__class__.__name__}.')
    
    length = len(value)
    if (length!=0) and (length < lower_limit or length > upper_limit):
        raise ValueError(f'`{name}` can be between length {lower_limit} and {upper_limit}, got {value!r}.')
    
    return value

def preconvert_bool(value, name):
    if (type(value) is bool):
        pass
    elif isinstance(value,int) and (value in (0,1)):
        value = bool(value)
    else:
        raise TypeError(f'`{name}` can be `bool` instance, got {value.__class__.__name__}.')
        
    return value

def preconvert_flag(flag, name, type_):
    if (type(flag) is type_):
        pass
    elif isinstance(flag, int):
        flag = type_(flag)
    else:
        raise TypeError(f'`{name}` can be passed as `{type_.__name__}` instance, got {flag.__class__.__name__}.')
    
    if flag < 0 or flag.bit_length()>64:
        raise ValueError(f'`{name}` can be only uint64, got {flag!r}.')
    
    return flag

def preconvert_preinstanced_type(value, name, type_):
    if type(value) is type_:
        return value
    
    INSTANCES = type_.INSTANCES
    if type(INSTANCES) is list:
        expected_type = int
    elif type(INSTANCES) is dict:
        expected_type = str
    else:
        raise NotImplementedError
    
    if (not isinstance(value, expected_type)):
        raise TypeError(f'`{name}` can be passed as {type_.__name__} or as {expected_type.__name__} instance, got {value.__class__.__name__}.')
    
    try:
        value = INSTANCES[value]
    except LookupError:
        raise ValueError(f'There is no predefined `{name}` for the following value: {value!r}.')
    
    return value

def preconvert_int(value, name, lower_limit, upper_limit):
    if type(value) is int:
        pass
    elif isinstance(value,int):
        value = str(value)
    else:
        raise TypeError(f'`{name}` can be `str` instance, got {value.__class__.__name__}.')
    
    if value < lower_limit or value > upper_limit:
        raise ValueError(f'`{name}` can be between {lower_limit} and {upper_limit}, got {value!r}.')
    
    return value




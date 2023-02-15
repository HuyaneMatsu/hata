__all__ = ()


def preconvert_snowflake(snowflake, name):
    """
    Converts the given `snowflake` to an acceptable value by the wrapper.
    
    Parameters
    ----------
    snowflake : `str`, `int`
        The snowflake to convert.
    name : `str`
        The name of the snowflake.
    
    Returns
    -------
    snowflake : `int`
    
    Raises
    ------
    TypeError
        - If `snowflake` was not passed neither as `int`, `str`.
    ValueError
        - If `snowflake` was passed as `str` and cannot be converted to `int`.
        - If the converted `snowflake` is negative or it's bit length is over 64.
    """
    snowflake_type = type(snowflake)
    if snowflake_type is int:
        pass
    if issubclass(snowflake_type, int):
        snowflake = int(snowflake)
    # JSON uint64 is str
    elif issubclass(snowflake_type, str):
        if 6 < len(snowflake) < 21 and snowflake.isdigit():
            snowflake = int(snowflake)
        else:
            raise ValueError(
                f'`{name}` can be `int`, `str`, got `str`, but not a valid'
                f'snowflake (7-20 length, digit only), got {snowflake!r}.'
            )
    else:
        raise TypeError(
            f'`{name}` can be `int`, `str`, got {snowflake_type.__name__}; {snowflake!r}.'
        )
    
    if snowflake < 0 or snowflake > ((1 << 64) - 1):
        raise ValueError(
            f'`{name}` can be only uint64, got {snowflake!r}.'
        )
    
    return snowflake


def preconvert_snowflake_array(snowflake_array, name):
    """
    Converts the given `snowflake_array` to an acceptable value by the wrapper.
    
    Parameters
    ----------
    snowflake_array : `None` or `iterable` of (`str`, `int`)
        The snowflakes to convert.
    name : `str`
        The name of the snowflake array.
    
    Returns
    -------
    snowflake_array : `None`, `tuple` of `int`
        The returned value is always sorted.
    
    Raises
    ------
    TypeError
        - If `snowflake_array` is neither `None`, `iterable`
        - If `snowflake_array` contains a non `int` nor `str`.
    ValueError
        - If `snowflake_array`contains a `str`, what cannot be converted to `int`.
        - If a converted `snowflake` is negative or it's bit length is over 64.
    """
    if (snowflake_array is None):
        return None
    
    snowflake_array_processed = None
    
    if getattr(preconvert_snowflake_array, '__iter__', None) is None:
        raise TypeError(
            f'`{name}` can be `list`, `tuple`, `set`, got '
            f'{snowflake_array.__class__.__name__}; {snowflake_array!r}.'
        )
    
    for snowflake in snowflake_array:
        snowflake_type = type(snowflake)
        if snowflake_type is int:
            pass
        if issubclass(snowflake_type, int):
            snowflake = int(snowflake)
        # JSON uint64 is str
        elif issubclass(snowflake_type, str):
            if 6 < len(snowflake) < 21 and snowflake.isdigit():
                snowflake = int(snowflake)
            else:
                raise ValueError(
                    f'`{name}`\'s can contain `int`, `str` elements, got `str`, but not a valid snowflake '
                    f'(7-20 length, digit only), got {snowflake!r}; snowflake_array={snowflake_array!r}.'
                )
        else:
            raise TypeError(
                f'`{name}`\'s can contain `int`, `str` elements, got '
                f'{snowflake_type.__name__}; {snowflake!r}; snowflake_array={snowflake_array!r}.'
            )
        
        if snowflake < 0 or snowflake > ((1 << 64) - 1):
            raise ValueError(
                f'`{name}`\'s elements can be only uint64, got '
                f'{snowflake!r}; snowflake_array={snowflake_array!r}.'
            )
        
        if snowflake_array_processed is None:
            snowflake_array_processed = set()
        
        snowflake_array_processed.add(snowflake)
    
    if (snowflake_array_processed is not None):
        snowflake_array = tuple(sorted(snowflake_array_processed))

    return snowflake_array


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
        If `value` was not passed as `str`.
    ValueError
        If the `value`'s length is less than the given `lower_limit` or is higher than the given than the given
        `upper_limit`.
    """
    if type(value) is str:
        pass
    elif isinstance(value, str):
        value = str(value)
    else:
        raise TypeError(
            f'`{name}` can be `str`, got {value.__class__.__name__}; {value!r}.'
        )
    
    length = len(value)
    if (length != 0) and (length < lower_limit or length > upper_limit):
        raise ValueError(
            f'`{name}` can be between length {lower_limit} and {upper_limit}, got {length!r}; {value!r}.'
        )
    
    return value


def preconvert_iterable_of_str(value, name, iterable_lower_limit, iterable_upper_limit, lower_limit, upper_limit):
    """
    Converts the given `value` to an acceptable iterable of string by the wrapper.
    
    Parameters
    ----------
    value : `str`
        The string to convert,
    name : `str`
        The name of the value.
    iterable_lower_limit : `int`
        The minimal length of `value`.
    iterable_upper_limit : `int`
        The maximal length of `value`.
    lower_limit : `int`
        The minimal length of the string.
    upper_limit : `int`
        The maximal length of the string.
    
    Returns
    -------
    converted_value : `set` of `str`
    
    Raises
    ------
    TypeError
        - If `value` was not passed as an `iterable`.
        - If `value` contains a non `str` element.
    ValueError
        - If the `value`'s length is less than the given `iterable_lower_limit` or is higher than the given than
            the given `iterable_upper_limit`.
        - If `value` contains a string whats length is less than `lower_limit` or is more than `upper_limit`.
    """
    iterator = getattr(type(value), '__iter__', None)
    if iterator is None:
        raise TypeError(
            f'`{name}` can be `iterable`, got {value.__class__.__name__}; {value!r}.'
        )
    
    converted_value = set()
    
    for value_element in iterator(value):
        if type(value_element) is str:
            pass
        elif isinstance(value_element, str):
            value_element = str(value_element)
        else:
            raise TypeError(
                f'`{name}` can contain `str` elements, got {value_element.__class__.__name__}; {value_element!r}; '
                f'value = {value!r}.'
            )
        
        length = len(value_element)
        if length == 0:
            continue
        
        if (length < lower_limit) or (length > upper_limit):
            raise ValueError(
                f'`{name}` can contains elements between length {lower_limit} and {upper_limit}, '
                f'got {length!r} {value_element!r}; value = {value!r}.'
            )
        
        converted_value.add(value_element)
    
    length = len(converted_value)
    if (length != 0) and (length < iterable_lower_limit or length > iterable_upper_limit):
        raise ValueError(
            f'`{name} can be in between length {iterable_lower_limit} and {iterable_upper_limit}, '
            f'got {length!r}; {value!r}.'
        )
    
    return converted_value


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
        If `value` was not passed as `int`.
    ValueError
        If value was passed as an `int`, but not as `0`, `1` either.
    """
    if (type(value) is bool):
        pass
    elif isinstance(value, int):
        if (value not in (0, 1)):
            raise ValueError(
                f'`{name}` was given as `int`, but neither as `0`, `1`, got {value!r}.'
            )
        value = bool(value)
    else:
        raise TypeError(
            f'`{name}` can be `bool`, `int` as `0`, `1`, got {value.__class__.__name__}; {value!r}.'
        )
    
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
        If `flag` was not given as `int`.
    ValueError
        If `flag` was given as `int`, but it's value is less than `0` or it's bit length is over `64`.
    """
    flag_type = flag.__class__
    if (flag_type is type_):
        pass
    elif issubclass(flag_type, int):
        flag = type_(flag)
    else:
        raise TypeError(
            f'`{name}` can be `{type_.__name__}`, got {flag_type.__name__}; {flag!r}.'
        )
    
    if flag < 0 or flag > ((1 << 64) - 1):
        raise ValueError(
            f'`{name}` can be only uint64, got {flag!r}.'
        )
    
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
    type_ : ``PreinstancedBase``
        The preinstanced type.
    
    Returns
    -------
    value : ``PreinstancedBase``
    
    Raises
    ------
    TypeError
        If `value` was not given as `type_`, neither as `type_.value`'s type's instance.
    ValueError
        If there is no preinstanced object for the given `value`.
    """
    value_type = value.__class__
    if (value_type is not type_):
        value_expected_type = type_.VALUE_TYPE
        if value is None:
            value = type_.get(value)
        
        elif value_type is value_expected_type:
            pass
        
        elif issubclass(value_type, value_expected_type):
            value = value_expected_type(value)
        
        else:
            raise TypeError(
                f'`{name}` can be `{type_.__name__}`, `{value_expected_type.__name__}` , got '
                f'{value_type.__name__}; {value!r}.'
            )
        
        try:
            value = type_.INSTANCES[value]
        except LookupError:
            raise ValueError(
                f'There is no predefined `{name}` for value: {value!r}.'
            ) from None
    
    return value


def _pre_validate_int(value, name):
    """
    Converts the given `value` to `int`.

    Parameters
    ----------
    value : `Any`
        The value to convert.
    name : `str`
        The name of the value.
    
    Returns
    -------
    value : `int`
    
    Raises
    ------
    TypeError
        If `value` was not given as `int`.
    """
    if type(value) is int:
        pass
    elif isinstance(value, int):
        value = int(value)
    else:
        raise TypeError(
            f'`{name}` can be `int`, got {value.__class__.__name__}; {value!r}.'
        )

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
        If `value` was not given as `int`.
    ValueError
        If `value` is less than `lower_limit`, or is higher than the `upper_limit`.
    """
    value = _pre_validate_int(value, name)
    
    if (value < lower_limit) or (value > upper_limit):
        raise ValueError(
            f'`{name}` can be between {lower_limit} and {upper_limit}, got {value!r}.'
        )
    
    return value


def preconvert_int_options(value, name, options):
    """
    Converts the given `value` to an acceptable integer by the wrapper.
    
    Parameters
    ----------
    value : `Any`
        The value to convert.
    name : `str`
        The name of the value.
    options : `frozenset`
        The options, from which `value` should be one.
    
    Returns
    -------
    value : `int`
    
    Raises
    ------
    TypeError
        If `value` was not given as `int`.
    ValueError
        If `value` is less than `lower_limit`, or is higher than the `upper_limit`.
    """
    value = _pre_validate_int(value, name)
    
    if value not in options:
        raise ValueError(
            f'`{name}` can be any of: {", ".join(str(option) for option in options)}, got {value!r}.'
        )
    
    return value


def preconvert_float(value, name, lower_limit, upper_limit):
    """
    Converts the given `value` to an acceptable float by the wrapper.
    
    Parameters
    ----------
    value : `Any`
        The value to convert.
    name : `str`
        The name of the value.
    lower_limit : `float`
        The minimal value of `value`.
    upper_limit : `float`
        The maximal value of `value`.
    
    Returns
    -------
    value : `float`
    
    Raises
    ------
    TypeError
        If `value` was not given as `float`.
    ValueError
        If `value` is less than `lower_limit`, or is higher than the `upper_limit`.
    """
    if type(value) is float:
        pass
    elif isinstance(value, float):
        value = int(value)
    else:
        float_converter = getattr(type(value), '__float__', None)
        if float_converter is None:
            raise TypeError(
                f'`{name}` can be `float`, got {value.__class__.__name__}; {value!r}.'
            )
        
        value = float_converter(value)
    
    if (value < lower_limit) or (value > upper_limit):
        raise ValueError(
            f'`{name}` can be between {lower_limit} and {upper_limit}, got {value!r}.'
        )
    
    return value


def get_type_names(type_or_types):
    """
    Gets the given type(s)'s name closed within \` characters.
    
    Parameters
    ----------
    type_or_types : `type`, `tuple` of `type`
        The type(s) to get name of.
    
    Returns
    -------
    type_names : `str`
    """
    type_name_parts = []
    
    if isinstance(type_or_types, type):
        type_name_parts.append('`')
        type_name_parts.append(type_or_types.__name__)
        type_name_parts.append('`')
    else:
        length = len(type_or_types)
        if length:
            index = 0
            while True:
                type_ = type_or_types[index]
                index += 1
                
                type_name_parts.append('`')
                type_name_parts.append(type_.__name__)
                type_name_parts.append('`')
                
                if index == length:
                    break
                
                type_name_parts.append(', ')
                continue
    
    return ''.join(type_name_parts)

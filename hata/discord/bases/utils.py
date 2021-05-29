__all__ = ('id_sort_key', 'instance_or_id_to_instance', 'instance_or_id_to_snowflake', 'maybe_snowflake',
    'maybe_snowflake_pair', 'maybe_snowflake_token_pair',)


def id_sort_key(entity):
    """
    Sort key for ``DiscordEntity`` instances.
    
    Parameters
    ----------
    entity : ``DiscordEntity``
        The discord entity to get identifier of.
    
    Returns
    -------
    entity_id : `int`
        The entity's identifier.
    """
    return entity.id


def instance_or_id_to_instance(obj, type_, name):
    """
    Converts the given `obj` to it's `type_` representation.
    
    Parameters
    ----------
    obj : `int`, `str` or`type_` instance
        The object to convert.
    type_ : `type` or (`tuple` of `type`)
        The type to convert.
    name : `str`
        The respective name of the object.
    
    Returns
    -------
    instance : `type_`
    
    Raises
    ------
    TypeError
        If `obj` was not given neither as `type_`, `str` or `int` instance.
    ValueError
        If `obj` was given as `str` or as `int` instance, but not as a valid snowflake, so `type_` cannot be precreated
        with it.
    
    Notes
    -----
    The given `type_` must have a `.precreate` function`.
    """
    obj_type = obj.__class__
    if issubclass(obj_type, type_):
        instance = obj
    else:
        if obj_type is int:
            snowflake = obj
        elif issubclass(obj_type, str):
            if 6 < len(obj) < 18 and obj.isdigit():
                snowflake = int(obj)
            else:
                raise ValueError(f'`{name}` was given as `str` instance, but not as a valid snowflake, got {obj!r}.')
        
        elif issubclass(obj_type, int):
            snowflake = int(obj)
        else:
            if type(type_) is tuple:
                type_name = ', '.join(t.__name__ for t in type_)
            else:
                type_name = type_.__name__
            
            raise TypeError(f'`{name}` can be given either as {type_name} instance, or as `int` or `str` representing '
                f'a snowflake, got {obj_type.__name__}.')
        
        if snowflake < 0 or snowflake > ((1<<64)-1):
            raise ValueError(f'`{name}` was given either as `int` or as `str` instance, but not as representing a '
                f'`uint64`, got {obj!r}.')
        
        if type(type_) is tuple:
            type_ = type_[0]
        
        instance = type_.precreate(snowflake)
    
    return instance


def instance_or_id_to_snowflake(obj, type_, name):
    """
    Validates the given `obj` whether it is instance of the given `type_`, or is a valid snowflake representation.
    
    Parameters
    ----------
    obj : `int`, `str` or`type_` instance
        The object to validate.
    type_ : `type` of (`tuple` of `type`)
        Expected type.
    name : `str`
        The respective name of the object.
    
    Returns
    -------
    snowflake : `int`
    
    Raises
    ------
    TypeError
        If `obj` was not given neither as `type_`, `str` or `int` instance.
    ValueError
        If `obj` was given as `str` or as `int` instance, but not as a valid snowflake.
    
    Notes
    -----
    The given `type_`'s instances must have a `.id` attribute.
    """
    obj_type = obj.__class__
    if issubclass(obj_type, type_):
        snowflake = obj.id
    else:
        if obj_type is int:
            snowflake = obj
        elif issubclass(obj_type, str):
            if 6 < len(obj) < 18 and obj.isdigit():
                snowflake = int(obj)
            else:
                raise ValueError(f'`{name}` was given as `str` instance, but not as a valid snowflake, got {obj!r}.')
        
        elif issubclass(obj_type, int):
            snowflake = int(obj)
        else:
            if type(type_) is tuple:
                type_name = ', '.join(t.__name__ for t in type_)
            else:
                type_name = type_.__name__
            
            raise TypeError(f'`{name}` can be given either as {type_name} instance, or as `int` or `str` representing '
                f'a snowflake, got {obj_type.__name__}.')
        
        if snowflake < 0 or snowflake>((1<<64)-1):
            raise ValueError(f'`{name}` was given either as `int` or as `str` instance, but not as representing a '
                f'`uint64`, got {obj!r}.')
    
    return snowflake


def maybe_snowflake(value):
    """
    Converts the given `value` to `snowflake` if applicable. If not returns `None`.
    
    Parameters
    ----------
    value : `str`, `int` or `Any`
        A value what might be snowflake.
    
    Returns
    -------
    value : `int` or `None`
    
    Raises
    ------
    AssertionError
        - If `value` was passed as `str` and cannot be converted to `int`.
        - If the `value` is negative or it's bit length is over 64.
    """
    if isinstance(value, int):
        pass
    elif isinstance(value, str):
        if value.isdigit():
            if __debug__:
                if not 6 < len(value) < 21:
                    raise AssertionError('An `id` was given as `str` instance, but it\'s value is out of 64uint '
                        f'range, got {value!r}.')
            
            value = int(value)
        else:
            return None
    else:
        return None
    
    if __debug__:
        if value < 0 or value > ((1<<64)-1):
            raise AssertionError('An `id` was given as `str` instance, but it\'s value is out of 64uint range, got '
                f'{value!r}.')
    
    return value


def maybe_snowflake_pair(value):
    """
    Checks whether the given value is a `tuple` of 2 snowflakes. If it, returns it, if not returns `None`.
    
    Parameters
    ----------
    value : `tuple` of (`str`, `int`) or `Any`
        A value what might be snowflake.
    
    Returns
    -------
    value : `tuple` (`int`, `int`) or `None`
    
    Raises
    ------
    AssertionError
        - If `value` contains a `str` element, what cannot be converted to `int`.
        - If `value` contains a value, what is negative or it's bit length is over 64.
    """
    if isinstance(value, tuple):
        if len(value) == 2:
            value_1, value_2 = value
            value_1 = maybe_snowflake(value_1)
            if value_1 is None:
                value = None
            else:
                value_2 = maybe_snowflake(value_2)
                if value_2 is None:
                    value = None
                else:
                    value = (value_1, value_2)
        else:
            value = None
    else:
        value = None
    
    return value


def maybe_snowflake_token_pair(value):
    """
    Checks whether the given value is a `tuple` of `2` elements: an identifier and a token. If not, returns `None`.
    
    Parameters
    ----------
    value : `tuple` of (`str`, `int`) or `Any`
        A value what might be snowflake.
    
    Returns
    -------
    value : `tuple` (`str`, `int`) or `None`
    
    Raises
    ------
    AssertionError
        - If `value` contains a `str` element, what cannot be converted to `int`.
        - If `value` contains a value, what is negative or it's bit length is over 64.
    """
    if isinstance(value, tuple):
        if len(value) == 2:
            value_1, value_2 = value
            value_1 = maybe_snowflake(value_1)
            if value_1 is None:
                value = None
            else:
                if isinstance(value_2, str):
                    value = (value_1, value_2)
                else:
                    value = None
        else:
            value = None
    else:
        value = None
    
    return value

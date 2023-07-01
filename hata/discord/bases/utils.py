__all__ = (
    'id_sort_key', 'instance_or_id_to_instance', 'instance_or_id_to_snowflake',
    'iterable_of_instance_or_id_to_instances', 'iterable_of_instance_or_id_to_snowflakes', 'maybe_snowflake',
    'maybe_snowflake_pair', 'maybe_snowflake_token_pair'
)


def id_sort_key(entity):
    """
    Sort key for ``DiscordEntity``-s.
    
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
    obj : `int`, `str` or`type_`
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
        If `obj` was not given neither as `type_`, `str`, `int`.
    ValueError
        If `obj` was given as `str`, `int`, but not as a valid snowflake, so `type_` cannot be precreated
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
            if 6 < len(obj) < 22 and obj.isdigit():
                snowflake = int(obj)
            else:
                raise ValueError(f'`{name}` was given as `str`, but not as a valid snowflake, got {obj!r}.')
        
        elif issubclass(obj_type, int):
            snowflake = int(obj)
        else:
            if type(type_) is tuple:
                type_name = ', '.join(t.__name__ for t in type_)
            else:
                type_name = type_.__name__
            
            raise TypeError(f'`{name}` can be given either as {type_name} instance, or as `int`, `str` representing '
                f'a snowflake, got {obj_type.__name__}.')
        
        if snowflake < 0 or snowflake > ((1 << 64) - 1):
            raise ValueError(f'`{name}` was given either as `int`, `str`, but not as representing a '
                f'`uint64`, got {obj!r}.')
        
        if type(type_) is tuple:
            type_ = type_[0]
        
        instance = type_.precreate(snowflake)
    
    return instance


def iterable_of_instance_or_id_to_instances(iterable_obj, type_, name):
    """
    Converts the given `iterable_obj` to it's `type_`'s representation.
    
    Parameters
    ----------
    iterable_obj : `iterable` of `int`, `str` or`type_`
        The object to convert.
    type_ : `type` or (`tuple` of `type`)
        The type to convert.
    name : `str`
        The respective name of the object.
    
    Returns
    -------
    instances : `set` of `type_`
    
    Raises
    ------
    TypeError
        If `obj` was not given neither as `type_`, `str`, `int`.
    ValueError
        If `obj` was given as `str`, `int`, but not as a valid snowflake, so `type_` cannot be precreated
        with it.
    
    Notes
    -----
    The given `type_` must have a `.precreate` function`.
    """
    iterator = getattr(type(iterable_obj), '__iter__', None)
    if iterator is None:
        raise TypeError(f'`{name}` can be `iterable`, got {iterable_obj.__class__.__name__}.')
    
    instances = set()
    
    for obj in iterator(iterable_obj):
        obj_type = obj.__class__
        if issubclass(obj_type, type_):
            instance = obj
        else:
            if obj_type is int:
                snowflake = obj
            elif issubclass(obj_type, str):
                if 6 < len(obj) < 22 and obj.isdigit():
                    snowflake = int(obj)
                else:
                    raise ValueError(f'`{name}` contains a `str`, but not as a valid snowflake, got {obj!r}.')
            
            elif issubclass(obj_type, int):
                snowflake = int(obj)
            else:
                if type(type_) is tuple:
                    type_name = ', '.join(t.__name__ for t in type_)
                else:
                    type_name = type_.__name__
                
                raise TypeError(f'`{name}` can contain either {type_name} instance, or an `int`, `str` representing '
                    f'a snowflake, got {obj_type.__name__}.')
            
            if snowflake < 0 or snowflake > ((1 << 64) - 1):
                raise ValueError(f'`{name}` contains an `int` or a `str`, but not as representing a '
                    f'`uint64`, got {obj!r}.')
            
            if type(type_) is tuple:
                type_ = type_[0]
        
            instance = type_.precreate(snowflake)
        
        instances.add(instance)
    
    return instances


def iterable_of_instance_or_id_to_snowflakes(iterable_obj, type_, name):
    """
    Converts the given `iterable_obj` to it's `type_`'s representation.
    
    Parameters
    ----------
    iterable_obj : `iterable` of `int`, `str` or`type_`
        The object to convert.
    type_ : `type` or (`tuple` of `type`)
        The type to convert.
    name : `str`
        The respective name of the object.
    
    Returns
    -------
    instances : `set` of `int`
    
    Raises
    ------
    TypeError
        If `obj` was not given neither as `type_`, `str`, `int`.
    ValueError
        If `obj` was given as `str`, `int`, but not as a valid snowflake, so `type_` cannot be precreated
        with it.
    """
    iterator = getattr(type(iterable_obj), '__iter__', None)
    if iterator is None:
        raise TypeError(f'`{name}` can be `iterable`, got {iterable_obj.__class__.__name__}.')
    
    snowflakes = set()
    
    for obj in iterator(iterable_obj):
        obj_type = obj.__class__
        if issubclass(obj_type, type_):
            snowflake = obj.id
        else:
            if obj_type is int:
                snowflake = obj
            elif issubclass(obj_type, str):
                if 6 < len(obj) < 22 and obj.isdigit():
                    snowflake = int(obj)
                else:
                    raise ValueError(f'`{name}` contains a `str`, but not as a valid snowflake, got {obj!r}.')
            
            elif issubclass(obj_type, int):
                snowflake = int(obj)
            else:
                if type(type_) is tuple:
                    type_name = ', '.join(t.__name__ for t in type_)
                else:
                    type_name = type_.__name__
                
                raise TypeError(f'`{name}` can contain either {type_name} instance, or an `int`, `str` representing '
                    f'a snowflake, got {obj_type.__name__}.')
            
            if snowflake < 0 or snowflake > ((1 << 64) - 1):
                raise ValueError(f'`{name}` contains an `int` or a `str`, but not as representing a '
                    f'`uint64`, got {obj!r}.')
        
        snowflakes.add(snowflake)
    
    return snowflakes


def instance_or_id_to_snowflake(obj, type_, name):
    """
    Validates the given `obj` whether it is instance of the given `type_`, or is a valid snowflake representation.
    
    Parameters
    ----------
    obj : `int`, `str` or`type_`
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
        If `obj` was not given neither as `type_`, `str`, `int`.
    ValueError
        If `obj` was given as `str`, `int`, but not as a valid snowflake.
    
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
            if 6 < len(obj) < 22 and obj.isdigit():
                snowflake = int(obj)
            else:
                raise ValueError(f'`{name}` was given as `str`, but not as a valid snowflake, got {obj!r}.')
        
        elif issubclass(obj_type, int):
            snowflake = int(obj)
        else:
            if type(type_) is tuple:
                type_name = ', '.join(t.__name__ for t in type_)
            else:
                type_name = type_.__name__
            
            raise TypeError(f'`{name}` can be given either as {type_name} instance, or as `int`, `str` representing '
                f'a snowflake, got {obj_type.__name__}.')
        
        if (snowflake < 0) or (snowflake > ((1 << 64) - 1)):
            raise ValueError(f'`{name}` was given either as `int`, `str`, but not as representing a '
                f'`uint64`, got {obj!r}.')
    
    return snowflake


def maybe_snowflake(value):
    """
    Converts the given `value` to `snowflake` if applicable. If not returns `None`.
    
    Parameters
    ----------
    value : `str`, `int`, `object`
        A value what might be snowflake.
    
    Returns
    -------
    value : `None`, `int`
    
    Raises
    ------
    AssertionError
        - If `value` was passed as `str` and cannot be converted to `int`.
        - If the `value` is negative or it's bit length is over 64.
    """
    if isinstance(value, int):
        pass
    
    elif isinstance(value, str):
        try:
            value = int(value)
        except ValueError:
            return None
    
    else:
        return None
    
    if (value < 0) or (value > ((1 << 64) - 1)):
        raise ValueError(
            f'An `id` was given with a value out of the expected 64uint range, got {value!r}.'
        )
    
    return value


def maybe_snowflake_pair(value):
    """
    Checks whether the given value is a `tuple` of 2 snowflakes. If it, returns it, if not returns `None`.
    
    Parameters
    ----------
    value : `tuple` of (`str`, `int`) or `object`
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
    value : `tuple` of (`str`, `int`) or `object`
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

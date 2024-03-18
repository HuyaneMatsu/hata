__all__ = ()


def build_edit_payload(old_entity, new_entity, field_converters, keyword_parameters):
    """
    Edit payload builder.
    
    Parameters
    ----------
    old_entity : `None`, `object with to_data(defaults)`
        Original entity.
    
    new_entity : `None` `object with to_data(defaults)`
        New entity to serialize to.
    
    field_converters : `dict` of (`str`, `tuple` (`callable`, `callable`)) items
        Fields converters to use.
    
    keyword_parameters : `dict` of (`str`, `object`) items
        Keyword parameters passed to the original function.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
        The built payload.
    
    Raises
    ------
    TypeError
        - Extra or unused parameter.
    """
    if (new_entity is None):
        data = {}
    else:
        data = new_entity.to_data(defaults = True)
        
        if (old_entity is not None):
            for old_field_name, old_field_value in old_entity.to_data(defaults = True).items():
                try:
                    new_field_value = data[old_field_name]
                except KeyError:
                    pass
                else:
                    if (old_field_value == new_field_value):
                        del data[old_field_name]
    
    add_payload_fields_from_keyword_parameters(field_converters, keyword_parameters, data, True)
    return data


def build_create_payload(entity, field_converters, keyword_parameters):
    """
    Create payload builder.
    
    Parameters
    ----------
    entity : `None`, `object with to_data(defaults)`
        An entity which can be serialized.
    
    field_converters : `dict` of (`str`, `tuple` (`callable`, `callable`)) items
        Fields converters to use.
    
    keyword_parameters : `dict` of (`str`, `object`) items
        Keyword parameters passed to the original function.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
        The built payload.
    
    Raises
    ------
    TypeError
        - Extra or unused parameter.
    """
    if (entity is None):
        data = {}
    else:
        data = entity.to_data(defaults = False)
    
    if keyword_parameters:
        add_payload_fields_from_keyword_parameters(field_converters, keyword_parameters, data, False)
    
    return data


def add_payload_fields_from_keyword_parameters(
    field_converters, keyword_parameters, data, defaults, *, raise_unused = True
):
    """
    Generic payload builder used by ``build_edit_payload`` and by ``build_create_payload``.
    
    Parameters
    ----------
    field_converters : `dict` of (`str`, `tuple` (`callable`, `callable`)) items
        Fields converters to use.
    
    keyword_parameters : `dict` of (`str`, `object`) items
        Keyword parameters passed to the original function.
    
    data : `dict` of (`str`, `object`) items
        The built payload.
    
    defaults : `bool`
        Whether default values should be included.
    
    raise_unused : `bool` = `True`, Optional (Keyword only)
        Whether exception should be raised when there are unused keyword parameters.
    
    Raises
    ------
    TypeError
        - Extra or unused parameter.
    
    Returns
    -------
    unused : `None | dict<str, object>`
    """
    unused = None
    
    while keyword_parameters:
        field_name, field_value = keyword_parameters.popitem()
        
        try:
            validator, putter = field_converters[field_name]
        except KeyError:
            if unused is None:
                unused = {}
            
            unused[field_name] = field_value
            continue
        
        putter(validator(field_value), data, defaults)
    
    if raise_unused and (unused is not None):
        raise TypeError(
            f'Unused or extra parameters: {unused!r}.'
        )
    return unused

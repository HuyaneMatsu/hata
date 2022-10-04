__all__ = ()


def build_edit_payload(old_entity, new_entity, field_converters, keyword_parameters):
    """
    Edit payload builder.
    
    Parameters
    ----------
    old_entity : `None`, `object with to_data(defaults)`
        Original entity.
    
    new_entity : `None` `object with to_data(defaults)`
        New entity to serialise to.
    
    field_converters : `dict` of (`str`, `tuple` (`callable`, `callable`)) items
        Fields converters to use.
    
    keyword_parameters : `dict` of (`str`, `object`) items
        Keyword parameters passed to the original function.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
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
        An entity which can be serialised.
    
    field_converters : `dict` of (`str`, `tuple` (`callable`, `callable`)) items
        Fields converters to use.
    
    keyword_parameters : `dict` of (`str`, `object`) items
        Keyword parameters passed to the original function.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
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


def add_payload_fields_from_keyword_parameters(field_converters, keyword_parameters, data, defaults):
    """
    Generic payload builder used by ``build_edit_payload`` and by ``build_create_payload``.
    
    Parameters
    ----------
    field_converters : `dict` of (`str`, `tuple` (`callable`, `callable`)) items
        Fields converters to use.
    
    keyword_parameters : `dict` of (`str`, `object`) items
        Keyword parameters passed to the original function.
    
    data : `dict` of (`str`, `Any`) items
        The built payload.
    
    defaults : `bool`
        Whether default values should be included.
    
    Raises
    ------
    TypeError
        - Extra or unused parameter.
    """
    unused = None
    
    while keyword_parameters:
        field_name, field_value = keyword_parameters.popitem()
        
        try:
            validator, putter = field_converters[field_name]
        except KeyError:
            if unused is None:
                unused = {}
            
            unused[field_name] = keyword_parameters
            continue
        
        putter(validator(field_value), data, defaults)
    
    if (unused is not None):
        raise TypeError(
            f'Unused or extra parameters: {unused!r}.'
        )

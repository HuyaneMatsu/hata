__all__ = ()


def process_precreate_parameters_and_raise_extra(keyword_parameters, fields):
    """
    Top level function over ``process_precreate_parameters``.
    
    Parameters
    ----------
    keyword_parameters : `dict` of (`str`, `object`) items
        Keyword parameters passed to a precreate method.
    fields : `dict` of (`str`, `tuple` (`str`, `callable`) items
        Accepted fields by their key as parameters name and their values as `attribute-name - validator`.
    
    Returns
    -------
    processed : `list` of `tuple` (`str`, `object`) items
        The processed values in `attribute-name - value` relation.
    
    Raises
    ------
    BaseException
        - Any exception raised by a field validator.
        - Extra parameters.
    """
    processed = []
    extra = process_precreate_parameters(keyword_parameters, fields, processed)
    raise_extra(extra)
    return processed


def process_precreate_parameters(keyword_parameters, fields, processed):
    """
    Processes keyword parameters passed to a precreate function.
    
    Parameters
    ----------
    keyword_parameters : `dict` of (`str`, `object`) items
        Keyword parameters passed to a precreate method.
    fields : `dict` of (`str`, `tuple` (`str`, `callable`) items
        Accepted fields by their key as parameters name and their values as `attribute-name - validator`.
    processed : `list` of `tuple` (`str`, `object`) items
        Already processed values in `attribute-name - value` relation.
    
    Returns
    -------
    extra : `None`, `dict` of (`str`, `object`) items
        Extra keyword parameters.
    
    Raises
    ------
    BaseException
        - Any exception raised by a field validator.
    """
    extra = None
    
    while keyword_parameters:
        field_name, field_value = keyword_parameters.popitem() 
        try:
            attribute_name, validator = fields[field_name]
        except KeyError:
            if extra is None:
                extra = {}
            extra[field_name] = field_value
            continue
        
        attribute_value = validator(field_value)
        processed.append((attribute_name, attribute_value))
        continue
    
    return extra


def raise_extra(extra):
    """
    Raises exception if there are extra fields.
    
    Parameters
    ----------
    extra : `None`, `dict` of (`str`, `object`) items
        Extra keyword parameters.
    
    Raises
    ------
    TypeError
        - Extra parameters.
    """
    if (extra is not None):
        raise TypeError(
            f'Extra fields received: {extra!r}.'
        )

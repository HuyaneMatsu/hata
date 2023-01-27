__all__ = ()

from ...activity import Activity

from ..activity_update import ActivityUpdate


def _validate_entity_list(entity_list_name, entity_type, entity_list):
    """
    Validates an entity list. Used by `validate_added` and `validate_removed`.
    
    Parameters
    ----------
    entity_list_name : `str`
        The name of the entity list.
    entity_list : `None`, `iterable` of `entity_type`
        The entity list to validate.
    
    Returns
    -------
    entity_list : `None`, `list` of `entity_type`
    
    Raises
    ------
    TypeError
        - If `entity_list`'s type is incorrect.
    """
    if entity_list is None:
        return None
    
    if getattr(entity_list, '__iter__', None) is None:
        raise TypeError(
            f'`{entity_list_name}` can be `None`, `iterable` of `{entity_type.__name__}`, got '
            f'{entity_list.__class__.__name__}; {entity_list!r}.'
        )
    
    entities_validated = None
    
    for entity in entity_list:
        if not isinstance(entity, entity_type):
            raise TypeError(
                f'`{entity_list_name}` elements can be `{entity_type.__name__}`, got '
                f'{entity.__class__.__name__}; {entity!r}; {entity_list_name} = {entity_list!r}'
            )
        
        if entities_validated is None:
            entities_validated = []
        
        entities_validated.append(entity)
    
    return entities_validated


def validate_added(added):
    """
    Validates the `added` field of an activity change.
    
    Parameters
    ----------
    added : `None`, `iterable` of ``Activity``
        Added activity to validate.
    
    Returns
    -------
    added : `None`, `list` of ``Activity``
    
    Raises
    ------
    TypeError
        - If `added`'s type is incorrect.
    """
    return _validate_entity_list('added', Activity, added)


def validate_updated(updated):
    """
    Validates the `updated` field of an activity change.
    
    Parameters
    ----------
    updated : `None`, `iterable` of ``ActivityUpdate``
        Added activity to validate.
    
    Returns
    -------
    updated : `None`, `list` of ``ActivityUpdate``
    
    Raises
    ------
    TypeError
        - If `updated`'s type is incorrect.
    """
    return _validate_entity_list('updated', ActivityUpdate, updated)


def validate_removed(removed):
    """
    Validates the `removed` field of an activity change.
    
    Parameters
    ----------
    removed : `None`, `iterable` of ``Activity``
        Added activity to validate.
    
    Returns
    -------
    removed : `None`, `list` of ``Activity``
    
    Raises
    ------
    TypeError
        - If `removed`'s type is incorrect.
    """
    return _validate_entity_list('removed', Activity, removed)

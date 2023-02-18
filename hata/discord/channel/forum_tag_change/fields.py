__all__ = ()

from ..forum_tag import ForumTag
from ..forum_tag_update import ForumTagUpdate


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
    Validates the `added` field of an forum tag change.
    
    Parameters
    ----------
    added : `None`, `iterable` of ``ForumTag``
        Added forum tag to validate.
    
    Returns
    -------
    added : `None`, `list` of ``ForumTag``
    
    Raises
    ------
    TypeError
        - If `added`'s type is incorrect.
    """
    return _validate_entity_list('added', ForumTag, added)


def validate_updated(updated):
    """
    Validates the `updated` field of an forum tag change.
    
    Parameters
    ----------
    updated : `None`, `iterable` of ``ForumTagUpdate``
        Added forum tag to validate.
    
    Returns
    -------
    updated : `None`, `list` of ``ForumTagUpdate``
    
    Raises
    ------
    TypeError
        - If `updated`'s type is incorrect.
    """
    return _validate_entity_list('updated', ForumTagUpdate, updated)


def validate_removed(removed):
    """
    Validates the `removed` field of an forum tag change.
    
    Parameters
    ----------
    removed : `None`, `iterable` of ``ForumTag``
        Added forum tag to validate.
    
    Returns
    -------
    removed : `None`, `list` of ``ForumTag``
    
    Raises
    ------
    TypeError
        - If `removed`'s type is incorrect.
    """
    return _validate_entity_list('removed', ForumTag, removed)

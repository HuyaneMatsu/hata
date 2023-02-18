__all__ = ()

from ...field_validators import entity_validator_factory

from ..forum_tag import ForumTag

# forum_tag

validate_forum_tag = entity_validator_factory('forum_tag', ForumTag)

# old_attributes

def validate_old_attributes(old_attributes):
    """
    Validates the given ``old_attributes`` field.`.
    
    Parameters
    ----------
    old_attributes : `None`, `dict` of (`str`, `object`) items
        The `old_attributes` value to validate.
    
    Returns
    -------
    old_attributes : `dict` of (`str`, `object`) items
    
    Raises
    ------
    TypeError
        - If `old_attributes`'s type is incorrect.
    """
    if old_attributes is None:
        return {}
    
    if not isinstance(old_attributes, dict):
        raise TypeError(
            f'`old_attributes` can be `None`, `dict` of (`str`, `object`) items, '
            f'got {old_attributes.__class__.__name__}; {old_attributes!r}.'
        )
    
    validated_old_attributes = {}
    
    for key, value in old_attributes.items():
        if not isinstance(key, str):
            raise TypeError(
                f'`old_attributes` keys can be `str` instances, got '
                f'{key.__class__.__name__}; {key!r}; old_attributes = {old_attributes!r}.'
            )
        
        validated_old_attributes[key] = value
    
    return validated_old_attributes

__all__ = ()

from scarletio import include

from ....bases import maybe_snowflake
from ....field_parsers import entity_id_parser_factory
from ....field_putters import entity_id_optional_putter_factory


Channel = include('Channel')


parse_parent_id = entity_id_parser_factory('parent_id')
put_parent_id_into = entity_id_optional_putter_factory('parent_id')


def validate_parent_id(parent_id):
    """
    Validates the given `parent_id` field.
    
    Parameters
    ----------
    parent_id : `None`, `str`, `int`, ``Channel``
        The channel's parent's identifier.
    
    Returns
    -------
    parent_id : `int`
    
    Raises
    ------
    TypeError
        - If `parent_id` is not `None`, `str`.
    ValueError
        - If `parent_id` is out of the expected range.
    """
    if parent_id is None:
        processed_parent_id = 0
    
    elif isinstance(parent_id, Channel):
        processed_parent_id = parent_id.id
    
    else:
        processed_parent_id = maybe_snowflake(parent_id)
        if processed_parent_id is None:
            raise TypeError(
                f'`parent_id` can be `int`, `{Channel.__name__}`, `int`, got '
                f'{parent_id.__class__.__name__}; {parent_id!r}.'
            )
    
    return processed_parent_id

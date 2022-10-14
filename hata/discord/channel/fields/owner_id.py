__all__ = ()

from scarletio import include

from ...bases import maybe_snowflake
from ...field_parsers import entity_id_parser_factory
from ...field_putters import entity_id_optional_putter_factory


ClientUserBase = include('ClientUserBase')


parse_owner_id = entity_id_parser_factory('owner_id')


def validate_owner_id(owner_id):
    """
    Validates the given `owner_id` field.
    
    Parameters
    ----------
    owner_id : `None`, `str`, `int`, ``ClientUserBase``
        The user's identifier who created the group or the thread channel.
    
    Returns
    -------
    owner_id : `int`
    
    Raises
    ------
    TypeError
        - If `owner_id` is not `None`, `str`.
    ValueError
        - If `owner_id` is out of the expected range.
    """
    if owner_id is None:
        processed_owner_id = 0
    
    elif isinstance(owner_id, ClientUserBase):
        processed_owner_id = owner_id.id
    
    else:
        processed_owner_id = maybe_snowflake(owner_id)
        if processed_owner_id is None:
            raise TypeError(
                f'`owner_id` can be `int`, `{ClientUserBase.__name__}`, `int`, got '
                f'{owner_id.__class__.__name__}; {owner_id!r}.'
            )
    
    return processed_owner_id


put_owner_id_into = entity_id_optional_putter_factory('owner_id')

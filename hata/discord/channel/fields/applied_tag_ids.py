__all__ = ()

from ...bases import maybe_snowflake

from ..forum_tag import ForumTag


def parse_applied_tag_ids(data):
    """
    Parses out the `applied_tag_ids` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    applied_tag_ids : `None`, `tuple` of `int`
    """
    applied_tag_id_array = data.get('applied_tags', None)
    if (applied_tag_id_array is None) or (not applied_tag_id_array):
        applied_tag_ids = None
    else:
        applied_tag_ids = tuple(sorted(int(tag_id) for tag_id in applied_tag_id_array))
    return applied_tag_ids


def validate_applied_tag_ids(applied_tag_ids):
    """
    Validates the given `applied_tag_ids` field.
    
    Parameters
    ----------
    applied_tag_ids : `None`, `iterable` of (`int`, ``ForumTag``)
        The tags' identifier which have been applied to the thread. Applicable for threads of a forum.

    
    Returns
    -------
    applied_tag_ids : `None`, `tuple` of `int`
    
    Raises
    ------
    TypeError
        - If `applied_tag_ids` is not `None`, `iterable` of (`int`, ``ForumTag``).
    """
    if applied_tag_ids is None:
        return None
    
    if (getattr(applied_tag_ids, '__iter__', None) is None):
        raise TypeError(
            f'`applied_tag_ids` can be `None`, `iterable` of (`int`, `{ForumTag.__name__}`), '
            f'got {applied_tag_ids.__class__.__name__}; {applied_tag_ids!r}.'
        )
    
    applied_tag_ids_processed = None
    
    for applied_tag_id in applied_tag_ids:
        if isinstance(applied_tag_id, ForumTag):
             applied_tag_id_processed = applied_tag_id.id
        
        else:
            applied_tag_id_processed = maybe_snowflake(applied_tag_id)
            if applied_tag_id_processed is None:
                raise TypeError(
                    f'`applied_tag_ids` can contain `int`, `{ForumTag.__name__}` elements, got '
                    f'{applied_tag_id.__class__.__name__}; {applied_tag_id!r}; applied_tag_ids={applied_tag_ids!r}.'
                )
        
        if applied_tag_ids_processed is None:
            applied_tag_ids_processed = set()
        
        applied_tag_ids_processed.add(applied_tag_id_processed)
    
    if applied_tag_ids_processed is None:
        return None
    
    return tuple(sorted(applied_tag_ids_processed))


def put_applied_tag_ids_into(applied_tag_ids, data, defaults):
    """
    Puts the `applied_tag_ids`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    applied_tag_ids : `None`, `tuple` of `int`
        The tags' identifier which have been applied to the thread. Applicable for threads of a forum.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if defaults or (applied_tag_ids is not None):
        if applied_tag_ids is None:
            applied_tag_id_array = []
        else:
            applied_tag_id_array = [str(tag_id) for tag_id in applied_tag_ids]
        
        data['applied_tags'] = applied_tag_id_array
    
    return data

__all__ = ()

from ..forum_tag import ForumTag


def parse_available_tags(data):
    """
    Parses out the `available_tags` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    available_tags : `None`, `tuple` of ``ForumTag``
    """
    available_tag_data_array = data.get('available_tags', None)
    if (available_tag_data_array is None) or (not available_tag_data_array):
        available_tags = None
    else:
        available_tags = tuple(sorted(ForumTag.from_data(tag_data) for tag_data in available_tag_data_array))

    return available_tags


def validate_available_tags(available_tags):
    """
    Validates the given `available_tags` field.
    
    Parameters
    ----------
    available_tags : `None`, `iterable` of ``ForumTag``
        The tags to validate.
    
    Returns
    -------
    available_tags : `None`, `tuple` of ``ForumTag``
    """
    if available_tags is None:
        return None
    
    if (getattr(available_tags, '__iter__', None) is None):
        raise TypeError(
            f'`available_tags` can be `None`, `iterable` of `{ForumTag.__name__}`, got '
            f'{available_tags.__class__.__name__}; {available_tags!r}.'
        )
        
    available_tags_processed = None
    
    for raw_tag in available_tags:
        if not isinstance(raw_tag, ForumTag):
            raise TypeError(
                f'`available_tags` can contain `{ForumTag.__name__}` elements, got '
                f'{raw_tag.__class__.__name__}; {raw_tag!r}; available_tags = {available_tags!r}.'
            )
        
        if (available_tags_processed is None):
            available_tags_processed = set()
        
        available_tags_processed.add(raw_tag)
    
    if (available_tags_processed is not None):
        available_tags_processed = tuple(sorted(available_tags_processed))
    
    return available_tags_processed


def put_available_tags_into(available_tags, data, defaults):
    """
    Puts the `available_tags`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    available_tags : `None`, `tuple` of ``ForumTag``
        The channel's tags.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if (available_tags is None):
        if defaults:
            data['available_tags'] = []
    else:
        data['available_tags'] = [tag.to_data(include_internals = True) for tag in available_tags]
    
    return data

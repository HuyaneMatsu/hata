__all__ = ()

from ...color import Color


def value_deserializer_id(value):
    """
    Shared `get_id` conversion.
    
    Parameters
    ----------
    value : `None | str`
        Raw value to convert.
    
    Returns
    -------
    value : `int`
    """
    if value is None:
        value = 0
    else:
        value = int(value)
    
    return value


def value_serializer_id(value):
    """
    Shared `put_id` conversion.
    
    Parameters
    ----------
    value : `int`
        Processed value to convert.
    
    Returns
    -------
    value : `None | str`
    """
    if value:
        value = str(value)
    else:
        value = None
    
    return value


def value_deserializer_ids(value):
    """
    Shared `get_ids` conversion.
    
    Parameters
    ----------
    value : `None | list<str>`
        Raw value to convert.
    
    Returns
    -------
    value : `None | tuple<int>`
    """
    if value is None:
        pass
    elif not value:
        value = None
    else:
        value = (*sorted(int(entity_id) for entity_id in value),)
    
    return value


def value_serializer_ids(value):
    """
    Shared `put_ids` conversion.
    
    Parameters
    ----------
    value : `None | tuple<int>`
        Processed value to convert.
    
    Returns
    -------
    value : `list<str>`
    """
    if value is None:
        value = []
    else:
        value = [str(entity_id) for entity_id in value]
    
    return value


def value_deserializer_name(value):
    """
    Shared `get_name` conversion.
    
    Parameters
    ----------
    value : `None | str`
        Raw value to convert.
    
    Returns
    -------
    value : `str`
    """
    if value is None:
        value = ''
    
    return value


def value_serializer_name(value):
    """
    Shared `put_name` conversion.
    
    Parameters
    ----------
    value : `str`
        Processed value to convert.
    
    Returns
    -------
    value : `str`
    """
    return value


def value_deserializer_string_array(value):
    """
    Shared `get_string_array` conversion.
    
    Parameters
    ----------
    value : `None | list<str>`
        Raw value to convert.
    
    Returns
    -------
    value : `None | tuple<str>`
    """
    if value is None:
        pass
    elif (not value):
        value = None
    else:
        value = (*sorted(value),)
    return value


def value_serializer_string_array(value):
    """
    Shared `put_string_array` conversion.
    
    Parameters
    ----------
    value : `None | tuple<str>`
        Processed value to convert.
    
    Returns
    -------
    value : `list<str>`
    """
    if value is None:
        value = []
    else:
        value = [*value]
    return value


def value_deserializer_description(value):
    """
    Shared `get_description` conversion.
    
    Parameters
    ----------
    value : `None | str`
        Raw value to convert.
    
    Returns
    -------
    value : `None | str`
    """
    if value is None:
        pass
    elif (not value):
        value = None
    return value


def value_serializer_description(value):
    """
    Shared `put_description` conversion.
    
    Parameters
    ----------
    value : `None | str`
        Processed value to convert.
    
    Returns
    -------
    value : `str`
    """
    if value is None:
        value = ''
    
    return value


def value_deserializer_html_color(value):
    """
    Shared `get_html_color` conversion.
    
    Parameters
    ----------
    value : `None | str`
        Raw value to convert.
    
    Returns
    -------
    value : `None | Color`
    """
    if value is not None:
        value = Color.from_html(value)
    
    return value


def value_serializer_html_color(value):
    """
    Shared `put_html_color` conversion.
    
    Parameters
    ----------
    value : `None | Color`
        Processed value to convert.
    
    Returns
    -------
    value : `None | str`
    """
    if (value is not None):
        value = value.as_html
    
    return value

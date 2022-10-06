__all__ = ()

from ...preconverters import preconvert_int_options

from ..constants import AUTO_ARCHIVE_DEFAULT, AUTO_ARCHIVE_OPTIONS


def parse_auto_archive_after(data):
    """
    Parses out the `auto_archive_after` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    auto_archive_after : `int`
    """
    try:
        sub_data = data['thread_metadata']
    except KeyError:
        auto_archive_after = AUTO_ARCHIVE_DEFAULT
    else:
        auto_archive_after = sub_data.get('auto_archive_duration', None)
        if auto_archive_after is None:
            auto_archive_after = AUTO_ARCHIVE_DEFAULT
        else:
            auto_archive_after *= 60

    return auto_archive_after


def validate_auto_archive_after(auto_archive_after):
    """
    Validates the given `auto_archive_after` field.
    
    Parameters
    ----------
    auto_archive_after : `int`
        Duration in seconds to automatically archive the thread after recent activity.
    
    Returns
    -------
    auto_archive_after : `int`
    
    Raises
    ------
    TypeError
        - If `auto_archive_after` is not `int` instance.
    ValueError
        - If `auto_archive_after` is not any of the expected values.
    """
    return preconvert_int_options(
        auto_archive_after,
        'auto_archive_after',
        AUTO_ARCHIVE_OPTIONS,
    )


def put_auto_archive_after_into(auto_archive_after, data, defaults, *, flatten_thread_metadata = False):
    """
    Puts the `auto_archive_after`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    auto_archive_after : `int`
        Duration in seconds to automatically archive the thread after recent activity.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    flatten_thread_metadata : `bool` = `False`, Optional (Keyword only)
        Whether the field should be flattened instead of nested.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if defaults or (auto_archive_after != AUTO_ARCHIVE_DEFAULT):
        if flatten_thread_metadata:
            data_to_use = data
        
        else:
            try:
                data_to_use = data['thread_metadata']
            except KeyError:
                data_to_use = {}
                data['thread_metadata'] = data_to_use
        
        data_to_use['auto_archive_duration'] = auto_archive_after // 60
    
    return data

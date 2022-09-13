__all__ = ()

from ...preconverters import preconvert_int_options

from ..constants import AUTO_ARCHIVE_DEFAULT, AUTO_ARCHIVE_OPTIONS


def parse_default_thread_auto_archive_after(data):
    """
    Parses out the `default_thread_auto_archive_after` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    default_thread_auto_archive_after : `int`
    """
    default_thread_auto_archive_after = data.get('default_auto_archive_duration', None)
    if default_thread_auto_archive_after is None:
        default_thread_auto_archive_after = AUTO_ARCHIVE_DEFAULT
    else:
        default_thread_auto_archive_after *= 60

    return default_thread_auto_archive_after


def validate_default_thread_auto_archive_after(default_thread_auto_archive_after):
    """
    Validates the given `default_thread_auto_archive_after` field.
    
    Parameters
    ----------
    default_thread_auto_archive_after : `int`
        The duration to validate.
    
    Returns
    -------
    default_thread_auto_archive_after : `int`
    
    Raises
    ------
    TypeError
        - If `default_thread_auto_archive_after` is not `int` instance.
    ValueError
        - If `default_thread_auto_archive_after` is not any of the expected values.
    """
    return preconvert_int_options(
        default_thread_auto_archive_after,
        'default_thread_auto_archive_after',
        AUTO_ARCHIVE_OPTIONS,
    )

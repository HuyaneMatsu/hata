__all__ = ()

from ..constants import AUTO_ARCHIVE_DEFAULT


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

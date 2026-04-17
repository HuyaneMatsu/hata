__all__ = ()

FLAG_HAS_BEFORE = 1 << 0
FLAG_HAS_AFTER = 1 << 1


FLAG_NAMES = (
    (FLAG_HAS_BEFORE, 'has_before'),
    (FLAG_HAS_AFTER, 'has_after'),
)


def get_flags_name(flags):
    """
    Gets the name of the given flags.
    
    Parameters
    ----------
    flags : `int`
        Flags to get their name of.
    
    Returns
    -------
    flags_name : `str`
    """
    if not flags:
        return 'none'
    
    return ', '.join([flag_name for flag_mask, flag_name in FLAG_NAMES if flags & flag_mask])

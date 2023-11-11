__all__ = ()

FLAG_HAS_BEFORE = 1 << 0
FLAG_HAS_AFTER = 1 << 1

FLAG_IS_MODIFICATION = 1 << 2
FLAG_IS_REMOVAL = 1 << 3
FLAG_IS_ADDITION = 1 << 4
FLAG_IS_IGNORED = 1 << 5
FLAG_IS_DEFAULT = 1 << 6


FLAG_NAMES = (
    (FLAG_HAS_BEFORE, 'has_before'),
    (FLAG_HAS_AFTER, 'has_after'),
    (FLAG_IS_MODIFICATION, 'is_modification'),
    (FLAG_IS_REMOVAL, 'is_removal'),
    (FLAG_IS_ADDITION, 'is_addition'),
    (FLAG_IS_IGNORED, 'is_ignored'),
    (FLAG_IS_DEFAULT, 'is_default'),
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

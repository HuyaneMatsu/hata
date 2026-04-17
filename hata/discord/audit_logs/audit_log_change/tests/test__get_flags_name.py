import vampytest

from ..flags import FLAG_HAS_AFTER, FLAG_HAS_BEFORE, get_flags_name



def _iter_options():
    yield 0, 'none'
    yield FLAG_HAS_BEFORE, 'has_before'
    yield FLAG_HAS_BEFORE | FLAG_HAS_AFTER, 'has_before, has_after'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_flags_name(flags):
    """
    Tests whether ``get_flags_name`` works as intended.
    
    Parameters
    ----------
    flags : `int`
        Flags to get their name of.
    
    Returns
    -------
    output : `bool`
    """
    return get_flags_name(flags)

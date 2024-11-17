import vampytest

from ..flag_meta import _is_reverse_descriptors_contradiction


def _iter_options():
    yield (
        set(),
        False,
    )
    
    yield (
        {
            ('hey', 0),
        },
        False,
    )
    
    yield (
        {
            ('hey', 0),
            ('mister', 0),
        },
        False,
    )
    
    yield (
        {
            ('hey', 0),
            ('mister', 1),
        },
        True,
    )
    
    yield (
        {
            ('hey', 0),
            ('mister', 0),
            ('sister', 0),
        },
        False,
    )
    
    yield (
        {
            ('hey', 0),
            ('mister', 0),
            ('sister', 1),
        },
        True,
    )
    
    yield (
        {
            ('hey', -1),
            ('mister', -1),
        },
        False,
    )
    
    yield (
        {
            ('hey', -1),
            ('mister', 1),
        },
        False,
    )
    
    yield (
        {
            ('hey', -1),
            ('mister', 1),
            ('sister', 0),
        },
        True,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_reverse_descriptors_contradiction(accumulated_reverse_descriptors):
    """
    Tests whether ``_is_reverse_descriptors_contradiction`` works as intended.
    
    Parameters
    ----------
    accumulated_reverse_descriptors : `set<(str, bool)>`
        Accumulated `__reverse_descriptors__` values.
    
    Returns
    -------
    output : `bool`
    """
    output = _is_reverse_descriptors_contradiction(accumulated_reverse_descriptors)
    vampytest.assert_instance(output, bool)
    return output

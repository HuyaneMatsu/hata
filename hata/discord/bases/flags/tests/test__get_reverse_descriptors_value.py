import vampytest

from ..flag_meta import _get_reverse_descriptors_value


def _iter_options():
    yield (
        set(),
        -1,
    )
    
    yield (
        {
            ('hey', 0),
        },
        0,
    )
    
    yield (
        {
            ('hey', -1),
        },
        -1,
    )
    
    yield (
        {
            ('hey', 1),
        },
        1,
    )
    
    yield (
        {
            ('hey', 0),
            ('mister', 0),
        },
        0,
    )
    
    yield (
        {
            ('hey', 1),
            ('mister', 1),
        },
        1,
    )
    
    yield (
        {
            ('hey', -1),
            ('mister', -1),
        },
        -1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_reverse_descriptors_value(accumulated_reverse_descriptors):
    """
    Tests whether ``_get_reverse_descriptors_value`` works as intended.
    
    Parameters
    ----------
    accumulated_reverse_descriptors : `set<(str, bool)>`
        Accumulated `__reverse_descriptors__` values.
    
    Returns
    -------
    output : `bool`
    """
    output = _get_reverse_descriptors_value(accumulated_reverse_descriptors)
    vampytest.assert_instance(output, int)
    return output

import vampytest

from ..flag_meta import _build_reverse_descriptors_contradiction_exception_message


def _iter_options():
    yield (
        {
            ('hey', True),
            ('mister', False),
        },
        'There is contradiction in `__reverse_descriptors__` values: hey -> True, mister -> False.'
    )
    
    yield (
        {
            ('hey', True),
            ('mister', False),
            ('sister', True),
        },
        'There is contradiction in `__reverse_descriptors__` values: hey -> True, mister -> False, sister -> True.'
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_reverse_descriptors_contradiction_exception_message(accumulated_reverse_descriptors):
    """
    Tests whether ``_build_reverse_descriptors_contradiction_exception_message`` works as intended.
    
    Parameters
    ----------
    accumulated_reverse_descriptors : `set<(str, bool)>`
        Accumulated `__reverse_descriptors__` values.
    
    Returns
    -------
    output : `str`
    """
    output = _build_reverse_descriptors_contradiction_exception_message(accumulated_reverse_descriptors)
    vampytest.assert_instance(output, str)
    return output

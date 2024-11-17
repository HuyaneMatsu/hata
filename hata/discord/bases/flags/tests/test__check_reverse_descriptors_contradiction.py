import vampytest

from ..flag_meta import _check_reverse_descriptors_contradiction


def _iter_options__passing():
    yield set()
    
    yield {
        ('hey', True),
    }
    
    yield {
        ('hey', True),
        ('mister', True),
    }


def _iter_options__value_error():
    yield {
        ('hey', True),
        ('mister', False),
    }


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__check_reverse_descriptors_contradiction(accumulated_reverse_descriptors):
    """
    Tests whether ``_check_reverse_descriptors_contradiction`` works as intended.
    
    Parameters
    ----------
    accumulated_reverse_descriptors : `set<(str, bool)>`
        Accumulated `__reverse_descriptors__` values.
    
    Raises
    ------
    ValueError
    """
    _check_reverse_descriptors_contradiction(accumulated_reverse_descriptors)

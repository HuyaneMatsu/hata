import vampytest

from ..flag_meta import _check_shifts_overlap


def _iter_options__passing():
    yield set()
    
    yield {
        ('hey', 2, None),
        ('mister', 3, None),
        ('sister', 4, None),
    }

    yield {
        ('hey', 2, None),
        ('mister', 3, None),
        ('sister', 4, None),
        ('koishi', 3, None),
        ('koishi', 3, None),
    }


def _iter_options__value_error():
    yield {
        ('hey', 2, None),
        ('mister', 3, None),
        ('sister', 4, None),
        ('koishi', 3, None),
        ('koishi', 4, None),
        ('satori', 4, None),
        ('satori', 5, None),
    }


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__check_shifts_overlap(accumulated_shifts):
    """
    Tests whether ``_check_shifts_overlap`` works as intended.
    
    Parameters
    ----------
    accumulated_shifts : `set<(str, int, None | FlagDeprecation)>`
        The accumulated shifts by their name.
    
    Raises
    ------
    ValueError
    """
    _check_shifts_overlap(accumulated_shifts)

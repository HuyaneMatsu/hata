import vampytest

from ..flag_meta import _collect_reverse_descriptors_from_type_parents


class _TestMeta(type):
    pass


class _TestType0(metaclass = _TestMeta):
    __reverse_descriptors__ = 1


class _testType1(metaclass = _TestMeta):
    __reverse_descriptors__ = 0


class _testType2(metaclass = _TestMeta):
    __reverse_descriptors__ = -1


def _iter_options():
    yield (
        (int,),
        set(),
    )
    
    yield (
        (int, _TestType0),
        {
            ('_TestType0', 1),
        },
    )
    
    yield (
        (int, _TestType0, _testType1, _testType2),
        {
            ('_TestType0', 1),
            ('_testType1', 0),
            ('_testType2', -1)
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__collect_reverse_descriptors_from_type_parents(type_parents):
    """
    Tests whether ``_collect_reverse_descriptors_from_type_parents`` works as intended.
    
    Parameters
    ----------
    type_parents : `tuple<type>`
        The parent types of the type to create.
    
    Returns
    -------
    output : `set<(str, int)>`
    
    Raises
    ------
    TypeError
    """
    accumulated_reverse_descriptors = set()
    
    _collect_reverse_descriptors_from_type_parents(_TestMeta, type_parents, accumulated_reverse_descriptors)
    return accumulated_reverse_descriptors

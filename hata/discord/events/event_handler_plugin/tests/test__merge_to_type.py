import vampytest

from ..helpers import _merge_to_type


def _iter_options():
    yield None, None, list, None
    yield [1, 2], None, list, [1, 2]
    yield None, [3, 4], list, [3, 4]
    yield [1, 2], [3, 4], list, [1, 2, 3, 4]

    yield None, None, set, None
    yield [1, 2], None, set, {1, 2}
    yield None, [3, 4], set, {3, 4}
    yield [1, 2], [3, 4], set, {1, 2, 3, 4}

    yield None, None, tuple, None
    yield [1, 2], None, tuple, (1, 2)
    yield None, [3, 4], tuple, (3, 4)
    yield [1, 2], [3, 4], tuple, (1, 2, 3, 4)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__merge_to_type(iterable_0, iterable_1, target_type):
    """
    Tests whether ``.target_type`` works as intended.
    
    Parameters
    ----------
    iterable_0 : `None | iterable`
        the first iterable to merge.
    
    iterable_1 : `None | iterable`
        the second iterable to merge.
    
    target_type : `type`
        The expected output type.
    
    Returns
    -------
    output : `None | instance<target_type>`
    """
    output = _merge_to_type(iterable_0, iterable_1, target_type)
    vampytest.assert_instance(output, target_type, nullable = True)
    return output

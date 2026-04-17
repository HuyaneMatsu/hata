from types import FunctionType

import vampytest

from ..snapshot import RandomErrorMessageGetterDifference


def _assert_fields_set(difference):
    """
    Tests whether the difference has all of its attributes set.
    
    Parameters
    ----------
    difference : ``RandomErrorMessageGetterDifference``
        The difference to check.
    """
    vampytest.assert_instance(difference, RandomErrorMessageGetterDifference)
    vampytest.assert_instance(difference.set_random_error_message_getter, FunctionType, nullable = True)
    vampytest.assert_instance(difference.set_random_error_message_getter, FunctionType, nullable = True)


def test__RandomErrorMessageGetterDifference__new():
    """
    Tests whether ``RandomErrorMessageGetterDifference.__new__`` works as intended.
    """
    difference = RandomErrorMessageGetterDifference()
    _assert_fields_set(difference)
    
    vampytest.assert_is(difference.set_random_error_message_getter, None)
    vampytest.assert_is(difference.set_random_error_message_getter, None)


def test__RandomErrorMessageGetterDifference__repr():
    """
    Tests whether ``RandomErrorMessageGetterDifference.__repr__`` works as intended.
    """
    set_random_error_message_getter = lambda : 'mia'
    removed_random_error_message_getter = lambda : 'mai'
    
    difference = RandomErrorMessageGetterDifference()
    difference.set(set_random_error_message_getter)
    difference.remove(removed_random_error_message_getter)
    
    output = repr(difference)
    vampytest.assert_instance(output, str)


def test__RandomErrorMessageGetterDifference__set():
    """
    Tests whether ``RandomErrorMessageGetterDifference.set`` works as intended.
    """
    set_random_error_message_getter = lambda : 'mia'
    
    difference = RandomErrorMessageGetterDifference()
    difference.set(set_random_error_message_getter)
    
    vampytest.assert_is(difference.set_random_error_message_getter, set_random_error_message_getter)


def test__RandomErrorMessageGetterDifference__remove():
    """
    Tests whether ``RandomErrorMessageGetterDifference.remove`` works as intended.
    """
    removed_random_error_message_getter = lambda : 'mia'
    
    difference = RandomErrorMessageGetterDifference()
    difference.remove(removed_random_error_message_getter)
    
    vampytest.assert_is(difference.removed_random_error_message_getter, removed_random_error_message_getter)


def test__RandomErrorMessageGetterDifference__set__match():
    """
    Tests whether ``RandomErrorMessageGetterDifference.set`` works as intended.
    
    Case: set and removed match in a single instance.
    """
    set_random_error_message_getter = lambda : 'mia'
    
    difference = RandomErrorMessageGetterDifference()
    difference.remove(set_random_error_message_getter)
    difference.set(set_random_error_message_getter)
    
    vampytest.assert_is(difference.set_random_error_message_getter, None)
    vampytest.assert_is(difference.removed_random_error_message_getter, None)


def test__RandomErrorMessageGetterDifference__remove__match():
    """
    Tests whether ``RandomErrorMessageGetterDifference.remove`` works as intended.
    
    Case: set and removed match in a single instance.
    """
    removed_random_error_message_getter = lambda : 'mia'
    
    difference = RandomErrorMessageGetterDifference()
    difference.set(removed_random_error_message_getter)
    difference.remove(removed_random_error_message_getter)
    
    vampytest.assert_is(difference.removed_random_error_message_getter, None)
    vampytest.assert_is(difference.set_random_error_message_getter, None)


def _iter_options__bool():
    yield (
        (),
        False,
    )
    
    yield (
        (
            (RandomErrorMessageGetterDifference.set, ((lambda : 'mia'), )),
        ),
        True,
    )

    yield (
        (
            (RandomErrorMessageGetterDifference.remove, ((lambda : 'mia'), )),
        ),
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__RandomErrorMessageGetterDifference__bool(operations):
    """
    Tests whether ``RandomErrorMessageGetterDifference.__bool__`` works as intended.
    
    Parameters
    ----------
    operations : `tuple<(FunctionType, tuple<object>)>`
        Operations to execute on the instance. And their parameters too ofc.
    
    Returns
    -------
    output : `bool`
    """
    difference = RandomErrorMessageGetterDifference()
    
    for operation, parameters in operations:
        operation(difference, *parameters)
    
    output = bool(difference)
    vampytest.assert_instance(output, bool)
    return output


def test__RandomErrorMessageGetterDifference__copy():
    """
    Tests whether ``RandomErrorMessageGetterDifference.copy`` works as intended.
    """
    set_random_error_message_getter = lambda : 'mia'
    removed_random_error_message_getter = lambda : 'mai'
    
    difference = RandomErrorMessageGetterDifference()
    difference.set(set_random_error_message_getter)
    difference.remove(removed_random_error_message_getter)
    
    copy = difference.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_is(copy.set_random_error_message_getter, set_random_error_message_getter)
    vampytest.assert_is(copy.removed_random_error_message_getter, removed_random_error_message_getter)


def test__RandomErrorMessageGetterDifference__reverse_copy():
    """
    Tests whether ``RandomErrorMessageGetterDifference.reverse_copy`` works as intended.
    """
    set_random_error_message_getter = lambda : 'mia'
    removed_random_error_message_getter = lambda : 'mai'
    
    difference = RandomErrorMessageGetterDifference()
    difference.set(set_random_error_message_getter)
    difference.remove(removed_random_error_message_getter)
    
    copy = difference.reverse_copy()
    _assert_fields_set(copy)
    
    vampytest.assert_is(copy.set_random_error_message_getter, removed_random_error_message_getter)
    vampytest.assert_is(copy.removed_random_error_message_getter, set_random_error_message_getter)


def test__RandomErrorMessageGetterDifference__sub__none():
    """
    Tests whether ``RandomErrorMessageGetterDifference.__sub__`` works as intended.
    
    Case: Other is `None`.
    """
    set_random_error_message_getter = lambda : 'mia'
    removed_random_error_message_getter = lambda : 'mai'
    
    difference = RandomErrorMessageGetterDifference()
    difference.set(set_random_error_message_getter)
    difference.remove(removed_random_error_message_getter)
    
    output = difference - None
    _assert_fields_set(output)
    
    vampytest.assert_is(output.set_random_error_message_getter, set_random_error_message_getter)
    vampytest.assert_is(output.removed_random_error_message_getter, removed_random_error_message_getter)


def test__RandomErrorMessageGetterDifference__rsub__none():
    """
    Tests whether ``RandomErrorMessageGetterDifference.__rsub__`` works as intended.
    
    Case: Other is `None`.
    """
    set_random_error_message_getter = lambda : 'mia'
    removed_random_error_message_getter = lambda : 'mai'
    
    difference = RandomErrorMessageGetterDifference()
    difference.set(set_random_error_message_getter)
    difference.remove(removed_random_error_message_getter)
    
    output = None - difference
    _assert_fields_set(output)
    
    vampytest.assert_is(output.set_random_error_message_getter, removed_random_error_message_getter)
    vampytest.assert_is(output.removed_random_error_message_getter, set_random_error_message_getter)


def test__RandomErrorMessageGetterDifference__sub__full_cancel_out():
    """
    Tests whether ``RandomErrorMessageGetterDifference.__sub__`` works as intended.
    
    Case: Full cancel out.
    """
    set_random_error_message_getter = lambda : 'mia'
    removed_random_error_message_getter = lambda : 'mai'
    
    difference_0 = RandomErrorMessageGetterDifference()
    difference_0.set(set_random_error_message_getter)
    difference_0.remove(removed_random_error_message_getter)
    
    difference_1 = RandomErrorMessageGetterDifference()
    difference_1.set(removed_random_error_message_getter)
    difference_1.remove(set_random_error_message_getter)
    
    output = difference_0 - difference_1
    _assert_fields_set(output)
    
    vampytest.assert_is(output.set_random_error_message_getter, None)
    vampytest.assert_is(output.removed_random_error_message_getter, None)


def test__RandomErrorMessageGetterDifference__sub__no_cancel_out():
    """
    Tests whether ``RandomErrorMessageGetterDifference.__sub__`` works as intended.
    
    Case: No cancel out.
    """
    set_random_error_message_getter_0 = lambda : 'mia'
    removed_random_error_message_getter_0 = lambda : 'mai'
    set_random_error_message_getter_1 = lambda : 'mia'
    removed_random_error_message_getter_1 = lambda : 'mai'
    
    difference_0 = RandomErrorMessageGetterDifference()
    difference_0.set(set_random_error_message_getter_0)
    difference_0.remove(removed_random_error_message_getter_0)
    
    difference_1 = RandomErrorMessageGetterDifference()
    difference_1.set(removed_random_error_message_getter_1)
    difference_1.remove(set_random_error_message_getter_1)
    
    output = difference_0 - difference_1
    _assert_fields_set(output)
    
    vampytest.assert_is(output.set_random_error_message_getter, set_random_error_message_getter_0)
    vampytest.assert_is(output.removed_random_error_message_getter, removed_random_error_message_getter_0)


def test__RandomErrorMessageGetterDifference__sub__set_cancel_out():
    """
    Tests whether ``RandomErrorMessageGetterDifference.__sub__`` works as intended.
    
    Case: Set cancel out.
    """
    set_random_error_message_getter = lambda : 'mia'
    removed_random_error_message_getter = lambda : 'mai'
    
    difference_0 = RandomErrorMessageGetterDifference()
    difference_0.set(set_random_error_message_getter)
    difference_0.remove(removed_random_error_message_getter)
    
    difference_1 = RandomErrorMessageGetterDifference()
    difference_1.set(None)
    difference_1.remove(set_random_error_message_getter)
    
    output = difference_0 - difference_1
    _assert_fields_set(output)
    
    vampytest.assert_is(output.set_random_error_message_getter, None)
    vampytest.assert_is_not(output.removed_random_error_message_getter, None)


def test__RandomErrorMessageGetterDifference__sub__removed_cancel_out():
    """
    Tests whether ``RandomErrorMessageGetterDifference.__sub__`` works as intended.
    
    Case: Removed cancel out.
    """
    set_random_error_message_getter = lambda : 'mia'
    removed_random_error_message_getter = lambda : 'mai'
    
    difference_0 = RandomErrorMessageGetterDifference()
    difference_0.set(set_random_error_message_getter)
    difference_0.remove(removed_random_error_message_getter)
    
    difference_1 = RandomErrorMessageGetterDifference()
    difference_1.set(removed_random_error_message_getter)
    difference_1.remove(None)
    
    output = difference_0 - difference_1
    _assert_fields_set(output)
    
    vampytest.assert_is_not(output.set_random_error_message_getter, None)
    vampytest.assert_is(output.removed_random_error_message_getter, None)


def test__RandomErrorMessageGetterDifference__sub__correct_difference():
    """
    Tests whether ``RandomErrorMessageGetterDifference.__sub__`` works as intended.
    
    Case: Correct difference of just additions.
    """
    set_random_error_message_getter = lambda : 'mia'
    removed_random_error_message_getter = lambda : 'mai'
    
    difference_0 = RandomErrorMessageGetterDifference()
    difference_0.set(set_random_error_message_getter)
    difference_0.remove(None)
    
    difference_1 = RandomErrorMessageGetterDifference()
    difference_1.set(removed_random_error_message_getter)
    difference_1.remove(None)
    
    output = difference_0 - difference_1
    _assert_fields_set(output)
    
    vampytest.assert_is(output.set_random_error_message_getter, set_random_error_message_getter)
    vampytest.assert_is(output.removed_random_error_message_getter, removed_random_error_message_getter)

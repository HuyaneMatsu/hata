from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..flag import FlagBase
from ..flag_descriptors import FlagDescriptor

from .helpers import FlagDeprecationCountTrigger


class TestFlag(FlagBase):
    koishi = FlagDescriptor(
        4,
        deprecation = FlagDeprecationCountTrigger(
            'spider',
            DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        )
    )
    satori = FlagDescriptor(5)
    orin = FlagDescriptor(6)


def test__FlagBase__new():
    """
    Tests whether ``FlagBase.__new__`` works as intended.
    """
    value = 8
    
    flag = FlagBase(value)
    
    vampytest.assert_instance(flag, FlagBase)
    vampytest.assert_eq(flag, value)


def test__FlagBase__repr():
    """
    Tests whether ``FlagBase.__repr__`` works as intended.
    """
    value = 8
    
    flag = FlagBase(value)
    
    output = repr(flag)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, f'{FlagBase.__name__}({value!r})')


def test__FlagBase__get_shift_of__generic():
    """
    Tests whether ``FlagBase._get_shift_of`` works as intended.
    
    Case: generic.
    """
    value = 8
    
    flag = TestFlag(value)
    
    output = flag._get_shift_of('satori')
    
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, TestFlag.satori.shift)


def test__FlagBase__get_shift_of__deprecated():
    """
    Tests whether ``FlagBase._get_shift_of`` works as intended.
    
    Case: generic.
    """
    value = 8
    
    flag = TestFlag(value)
    
    TestFlag.koishi.deprecation.triggered = 0
    output = flag._get_shift_of('koishi')
    
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, TestFlag.koishi.shift)
    vampytest.assert_eq(TestFlag.koishi.deprecation.triggered, 1)


def test__FlagBase__get_shift_of__under_fixed():
    """
    Tests whether ``FlagBase._get_shift_of`` works as intended.
    
    Case: underscore prefixed.
    """
    value = 8
    
    flag = TestFlag(value)
    
    output = flag._get_shift_of('_51')
    
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 51)


def test__FlagBase__get_shift_of__invalid():
    """
    Tests whether ``FlagBase._get_shift_of`` works as intended.
    
    Case: underscore prefixed.
    """
    value = 8
    
    flag = TestFlag(value)
    
    with vampytest.assert_raises(LookupError):
        flag._get_shift_of('nyan')


def _iter_options__get_item__passing():
    yield 0, TestFlag.satori.flag_name, False
    yield TestFlag.satori.mask, TestFlag.satori.flag_name, True


def _iter_options__get_item__lookup_error():
    yield 0, 'nyan'


@vampytest._(vampytest.call_from(_iter_options__get_item__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__get_item__lookup_error()).raising(LookupError))
def test__FlagBase__getitem(value, key):
    """
    Tests whether ``FlagBase.__getitem__`` works as intended.
    
    Parameters
    ----------
    value : int`
        Value to create flag from.
    
    key : `str`
        The key to get the flag for.
    
    Raises
    ------
    LookupError
    """
    flag = TestFlag(value)
    output = flag[key]
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__keys():
    yield (
        0,
        set(),
    )
    
    yield (
        TestFlag.koishi.mask,
        set(),
    )
    
    yield (
        TestFlag.satori.mask | TestFlag.orin.mask,
        {TestFlag.satori.flag_name, TestFlag.orin.flag_name},
    )


@vampytest._(vampytest.call_from(_iter_options__keys()).returning_last())
def test__FlagBase__keys(value):
    """
    Tests whether ``FlagBase.keys`` works as intended.
    
    Parameters
    ----------
    value : int`
        Value to create flag from.
    
    Returns
    -------
    output : `set<str>`
    """
    flag = TestFlag(value)
    return {*flag.keys()}


def _iter_options__values():
    yield (
        0,
        set(),
    )
    yield (
        TestFlag.koishi.mask,
        set(),
    )
    yield (
        TestFlag.satori.mask | TestFlag.orin.mask,
        {TestFlag.satori.shift, TestFlag.orin.shift},
    )


@vampytest._(vampytest.call_from(_iter_options__values()).returning_last())
def test__FlagBase__values(value):
    """
    Tests whether ``FlagBase.values`` works as intended.
    
    Parameters
    ----------
    value : int`
        Value to create flag from.
    
    Returns
    -------
    output : `set<int>`
    """
    flag = TestFlag(value)
    return {*flag.values()}


def _iter_options__items():
    yield (
        0,
        {(TestFlag.satori.flag_name, False), (TestFlag.orin.flag_name, False)},
    )
    yield (
        TestFlag.koishi.mask,
        {(TestFlag.satori.flag_name, False), (TestFlag.orin.flag_name, False)},
    )
    yield (
        TestFlag.satori.mask | TestFlag.orin.mask,
        {(TestFlag.satori.flag_name, True), (TestFlag.orin.flag_name, True)},
    )


@vampytest._(vampytest.call_from(_iter_options__items()).returning_last())
def test__FlagBase__items(value):
    """
    Tests whether ``FlagBase.items`` works as intended.
    
    Parameters
    ----------
    value : int`
        Value to create flag from.
    
    Returns
    -------
    output : `set<(str, int)>`
    """
    flag = TestFlag(value)
    return {*flag.items()}


def _iter_options__set_checks():
    yield 1, 1, FlagBase.is_subset, True
    yield 3, 1, FlagBase.is_subset, False
    yield 1, 3, FlagBase.is_subset, True
    yield 1, 2, FlagBase.is_subset, False
    yield 2, 1, FlagBase.is_subset, False
    
    yield 1, 1, FlagBase.is_superset, True
    yield 3, 1, FlagBase.is_superset, True
    yield 1, 3, FlagBase.is_superset, False
    yield 1, 2, FlagBase.is_superset, False
    yield 2, 1, FlagBase.is_superset, False
    
    yield 1, 1, FlagBase.is_strict_subset, False
    yield 3, 1, FlagBase.is_strict_subset, False
    yield 1, 3, FlagBase.is_strict_subset, True
    yield 1, 2, FlagBase.is_strict_subset, False
    yield 2, 1, FlagBase.is_strict_subset, False
    
    yield 1, 1, FlagBase.is_strict_superset, False
    yield 3, 1, FlagBase.is_strict_superset, True
    yield 1, 3, FlagBase.is_strict_superset, False
    yield 1, 2, FlagBase.is_strict_superset, False
    yield 2, 1, FlagBase.is_strict_superset, False


@vampytest._(vampytest.call_from(_iter_options__set_checks()).returning_last())
def test___FlagBase__set_checks(value_0, value_1, set_check):
    """
    Tests whether ``FlagBase``'s set checks work as intended.
    
    Parameters
    ----------
    value_0 : `int`
        Value to test with.
    
    value_1 : `int`
        Value to test with.
    
    set_check : `FunctionType`
        The set check function to invoke.
    
    Returns
    -------
    output : `bool`
    """
    flag_0 = TestFlag(value_0)
    flag_1 = TestFlag(value_1)
    output = set_check(flag_0, flag_1)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__update_by_keys():
    yield (
        0,
        {},
        0,
    )
    
    yield (
        TestFlag.orin.mask,
        {
            TestFlag.satori.flag_name: True,
        },
        TestFlag.satori.mask | TestFlag.orin.mask,
    )
    
    yield (
        TestFlag.satori.mask | TestFlag.orin.mask,
        {
            TestFlag.satori.flag_name: False,
        },
        TestFlag.orin.mask,
    )
    
    yield (
        TestFlag.satori.mask,
        {
            TestFlag.satori.flag_name: True,
        },
        TestFlag.satori.mask,
    )
    
    yield (
        TestFlag.satori.mask | TestFlag.orin.mask,
        {
            TestFlag.satori.flag_name: True,
        },
        TestFlag.satori.mask | TestFlag.orin.mask,
    )


@vampytest._(vampytest.call_from(_iter_options__update_by_keys()).returning_last())
def test__FlagBase__update_by_keys(value, keyword_parameters):
    """
    Tests whether ``FlagBase.update_by_keys`` works as intended.
    
    Parameters
    ----------
    value : `int`
        Value to test with.
    
    keyword_parameters : `dict<str, object>`
        Keyword parameters to call `.update_by_keys` with.
    
    Returns
    -------
    output : ``FlagBase``
    """
    output = TestFlag(value).update_by_keys(**keyword_parameters)
    vampytest.assert_instance(output, FlagBase)
    return output

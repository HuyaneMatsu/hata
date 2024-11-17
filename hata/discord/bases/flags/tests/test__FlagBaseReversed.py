from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..flag import FlagBaseReversed
from ..flag_descriptors import FlagDescriptor

from .helpers import FlagDeprecationCountTrigger


class TestFlag(FlagBaseReversed):
    koishi = FlagDescriptor(
        4,
        deprecation = FlagDeprecationCountTrigger(
            'spider',
            DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        )
    )
    satori = FlagDescriptor(5)
    orin = FlagDescriptor(6)


def _iter_options__get_item__passing():
    yield 0, TestFlag.satori.flag_name, True
    yield TestFlag.satori.mask, TestFlag.satori.flag_name, False


def _iter_options__get_item__lookup_error():
    yield 0, 'nyan'


@vampytest._(vampytest.call_from(_iter_options__get_item__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__get_item__lookup_error()).raising(LookupError))
def test__FlagBaseReversed__getitem(value, key):
    """
    Tests whether ``FlagBaseReversed.__getitem__`` works as intended.
    
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
        {TestFlag.satori.flag_name, TestFlag.orin.flag_name},
    )
    
    yield (
        TestFlag.koishi.mask,
        {TestFlag.satori.flag_name, TestFlag.orin.flag_name},
    )
    
    yield (
        TestFlag.satori.mask | TestFlag.orin.mask,
        set(),
    )


@vampytest._(vampytest.call_from(_iter_options__keys()).returning_last())
def test__FlagBaseReversed__keys(value):
    """
    Tests whether ``FlagBaseReversed.keys`` works as intended.
    
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
        {TestFlag.satori.shift, TestFlag.orin.shift},
    )
    yield (
        TestFlag.koishi.mask,
        {TestFlag.satori.shift, TestFlag.orin.shift},
    )
    yield (
        TestFlag.satori.mask | TestFlag.orin.mask,
        set(),
    )


@vampytest._(vampytest.call_from(_iter_options__values()).returning_last())
def test__FlagBaseReversed__values(value):
    """
    Tests whether ``FlagBaseReversed.values`` works as intended.
    
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
        {(TestFlag.satori.flag_name, True), (TestFlag.orin.flag_name, True)},
    )
    yield (
        TestFlag.koishi.mask,
        {(TestFlag.satori.flag_name, True), (TestFlag.orin.flag_name, True)},
    )
    yield (
        TestFlag.satori.mask | TestFlag.orin.mask,
        {(TestFlag.satori.flag_name, False), (TestFlag.orin.flag_name, False)},
    )


@vampytest._(vampytest.call_from(_iter_options__items()).returning_last())
def test__FlagBaseReversed__items(value):
    """
    Tests whether ``FlagBaseReversed.items`` works as intended.
    
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
    yield 1, 1, FlagBaseReversed.is_subset, True
    yield 3, 1, FlagBaseReversed.is_subset, True
    yield 1, 3, FlagBaseReversed.is_subset, False
    yield 1, 2, FlagBaseReversed.is_subset, False
    yield 2, 1, FlagBaseReversed.is_subset, False
    
    yield 1, 1, FlagBaseReversed.is_superset, True
    yield 3, 1, FlagBaseReversed.is_superset, False
    yield 1, 3, FlagBaseReversed.is_superset, True
    yield 1, 2, FlagBaseReversed.is_superset, False
    yield 2, 1, FlagBaseReversed.is_superset, False
    
    yield 1, 1, FlagBaseReversed.is_strict_subset, False
    yield 3, 1, FlagBaseReversed.is_strict_subset, True
    yield 1, 3, FlagBaseReversed.is_strict_subset, False
    yield 1, 2, FlagBaseReversed.is_strict_subset, False
    yield 2, 1, FlagBaseReversed.is_strict_subset, False
    
    yield 1, 1, FlagBaseReversed.is_strict_superset, False
    yield 3, 1, FlagBaseReversed.is_strict_superset, False
    yield 1, 3, FlagBaseReversed.is_strict_superset, True
    yield 1, 2, FlagBaseReversed.is_strict_superset, False
    yield 2, 1, FlagBaseReversed.is_strict_superset, False


@vampytest._(vampytest.call_from(_iter_options__set_checks()).returning_last())
def test___FlagBaseReversed__set_checks(value_0, value_1, set_check):
    """
    Tests whether ``FlagBaseReversed``'s set checks work as intended.
    
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
        TestFlag.orin.mask,
    )
    
    yield (
        TestFlag.satori.mask | TestFlag.orin.mask,
        {
            TestFlag.satori.flag_name: False,
        },
        TestFlag.satori.mask | TestFlag.orin.mask,
    )
    
    yield (
        TestFlag.satori.mask,
        {
            TestFlag.satori.flag_name: True,
        },
        0,
    )
    
    yield (
        TestFlag.satori.mask | TestFlag.orin.mask,
        {
            TestFlag.satori.flag_name: True,
        },
        TestFlag.orin.mask,
    )


@vampytest._(vampytest.call_from(_iter_options__update_by_keys()).returning_last())
def test__FlagBaseReversed__update_by_keys(value, keyword_parameters):
    """
    Tests whether ``FlagBaseReversed.update_by_keys`` works as intended.
    
    Parameters
    ----------
    value : `int`
        Value to test with.
    
    keyword_parameters : `dict<str, object>`
        Keyword parameters to call `.update_by_keys` with.
    
    Returns
    -------
    output : ``FlagBaseReversed``
    """
    output = TestFlag(value).update_by_keys(**keyword_parameters)
    vampytest.assert_instance(output, FlagBaseReversed)
    return output

from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest

from ..flag_deprecation import FORMAT_CODE, FlagDeprecation


def _assert_fields_set(flag_deprecation):
    """
    Asserts whether every fields are set of the given deprecation.
    
    Parameters
    ----------
    flag_deprecation : ``FlagDeprecation``
        The flag deprecation to test.
    """
    vampytest.assert_instance(flag_deprecation, FlagDeprecation)
    vampytest.assert_instance(flag_deprecation.allowed, bool)
    vampytest.assert_instance(flag_deprecation.removed_after, str)
    vampytest.assert_instance(flag_deprecation.use_instead, str)


def test__FlagDeprecation__new__least_fields():
    """
    Tests whether ``FlagDeprecation.__new__`` works as intended.
    
    Case: least fields given.
    """
    use_instead = 'koishi'
    removed_after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    flag_deprecation = FlagDeprecation(
        use_instead,
        removed_after,
    )
    _assert_fields_set(flag_deprecation)
    
    vampytest.assert_eq(flag_deprecation.allowed, True)
    vampytest.assert_eq(flag_deprecation.removed_after, format(removed_after, FORMAT_CODE))
    vampytest.assert_eq(flag_deprecation.use_instead, use_instead)


def test__FlagDeprecation__new__all_fields():
    """
    Tests whether ``FlagDeprecation.__new__`` works as intended.
    
    Case: all fields given.
    """
    use_instead = 'koishi'
    removed_after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    trigger_after = DateTime.now(tz = TimeZone.utc) + TimeDelta(days = 5000)
    
    flag_deprecation = FlagDeprecation(
        use_instead,
        removed_after,
        trigger_after = trigger_after,
    )
    _assert_fields_set(flag_deprecation)
    
    vampytest.assert_eq(flag_deprecation.allowed, False)
    vampytest.assert_eq(flag_deprecation.removed_after, format(removed_after, FORMAT_CODE))
    vampytest.assert_eq(flag_deprecation.use_instead, use_instead)


def _iter_options__eq():
    use_instead = 'koishi'
    removed_after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    trigger_after = DateTime.now(tz = TimeZone.utc) + TimeDelta(days = 5000)
    
    keyword_parameters = {
        'use_instead': use_instead,
        'removed_after': removed_after,
        'trigger_after': trigger_after,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'use_instead': 'satori',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'removed_after': DateTime(2016, 7, 14, tzinfo = TimeZone.utc)
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'trigger_after': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__FlagDeprecation__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``FlagDeprecation.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    flag_deprecation_0 = FlagDeprecation(**keyword_parameters_0)
    flag_deprecation_1 = FlagDeprecation(**keyword_parameters_1)
    
    output = flag_deprecation_0 == flag_deprecation_1
    vampytest.assert_instance(output, bool)
    return output


def test__FlagDeprecation__hash():
    """
    Tests whether ``FlagDeprecation.__hash__`` works as intended.
    """
    use_instead = 'koishi'
    removed_after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    trigger_after = DateTime.now(tz = TimeZone.utc) + TimeDelta(days = 5000)
    
    flag_deprecation = FlagDeprecation(
        use_instead,
        removed_after,
        trigger_after = trigger_after,
    )
    
    output = hash(flag_deprecation)
    vampytest.assert_instance(output, int)


def test__FlagDeprecation__repr():
    """
    Tests whether ``FlagDeprecation.__repr__`` works as intended.
    """
    use_instead = 'koishi'
    removed_after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    trigger_after = DateTime.now(tz = TimeZone.utc) + TimeDelta(days = 5000)
    
    flag_deprecation = FlagDeprecation(
        use_instead,
        removed_after,
        trigger_after = trigger_after,
    )
    
    output = repr(flag_deprecation)
    vampytest.assert_instance(output, str)


def test__FlagDeprecation__trigger__disallowed():
    """
    Tests whether ``FlagDeprecation.trigger`` works as intended.
    
    Case: disallowed.
    """
    use_instead = 'koishi'
    removed_after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    trigger_after = DateTime.now(tz = TimeZone.utc) + TimeDelta(days = 5000)
    
    flag_deprecation = FlagDeprecation(
        use_instead,
        removed_after,
        trigger_after = trigger_after,
    )
    
    type_name = 'orin'
    flag_name = 'okuu'
    stack_level = 4
    
    def warn_mock(
        message,
        warning_type,
        *,
        stacklevel = 1,
    ):
        raise RuntimeError()
    
    
    mocked = vampytest.mock_globals(
        FlagDeprecation.trigger,
        warn = warn_mock,
    )
    
    output = mocked(flag_deprecation, type_name, flag_name, stack_level)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__FlagDeprecation__trigger__allowed():
    """
    Tests whether ``FlagDeprecation.trigger`` works as intended.
    
    Case: allowed.
    """
    use_instead = 'koishi'
    removed_after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    flag_deprecation = FlagDeprecation(
        use_instead,
        removed_after,
    )
    
    type_name = 'orin'
    flag_name = 'okuu'
    stack_level = 4
    warn_called = 0
    
    def warn_mock(
        message,
        warning_type,
        *,
        stacklevel = 1,
    ):
        vampytest.assert_instance(message, str)
        vampytest.assert_is(warning_type, FutureWarning)
        vampytest.assert_instance(stacklevel, int)
        
        nonlocal type_name
        nonlocal flag_name
        nonlocal stack_level
        nonlocal flag_deprecation
        nonlocal warn_called
        
        vampytest.assert_in(type_name, message)
        vampytest.assert_in(flag_name, message)
        vampytest.assert_in(flag_deprecation.use_instead, message)
        vampytest.assert_in(flag_deprecation.removed_after, message)
        vampytest.assert_eq(stack_level, stack_level)
        
        warn_called += 1
        
    
    mocked = vampytest.mock_globals(
        FlagDeprecation.trigger,
        warn = warn_mock,
    )
    
    output = mocked(flag_deprecation, type_name, flag_name, stack_level)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)

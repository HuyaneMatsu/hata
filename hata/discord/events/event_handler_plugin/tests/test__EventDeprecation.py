from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest

from ..event_deprecation import FORMAT_CODE, EventDeprecation


def _assert_fields_set(event_deprecation):
    """
    Asserts whether every fields are set of the given deprecation.
    
    Parameters
    ----------
    event_deprecation : ``EventDeprecation``
        The flag deprecation to test.
    """
    vampytest.assert_instance(event_deprecation, EventDeprecation)
    vampytest.assert_instance(event_deprecation.allowed, bool)
    vampytest.assert_instance(event_deprecation.removed_after, str)
    vampytest.assert_instance(event_deprecation.use_instead, str)


def test__EventDeprecation__new__least_fields():
    """
    Tests whether ``EventDeprecation.__new__`` works as intended.
    
    Case: least fields given.
    """
    removed_after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    use_instead = 'koishi'
    
    event_deprecation = EventDeprecation(
        use_instead,
        removed_after,
    )
    _assert_fields_set(event_deprecation)
    
    vampytest.assert_eq(event_deprecation.allowed, True)
    vampytest.assert_eq(event_deprecation.removed_after, format(removed_after, FORMAT_CODE))
    vampytest.assert_eq(event_deprecation.use_instead, use_instead)


def test__EventDeprecation__new__all_fields():
    """
    Tests whether ``EventDeprecation.__new__`` works as intended.
    
    Case: all fields given.
    """
    removed_after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    trigger_after = DateTime.now(tz = TimeZone.utc) + TimeDelta(days = 5000)
    use_instead = 'koishi'
    
    event_deprecation = EventDeprecation(
        use_instead,
        removed_after,
        trigger_after = trigger_after,
    )
    _assert_fields_set(event_deprecation)
    
    vampytest.assert_eq(event_deprecation.allowed, False)
    vampytest.assert_eq(event_deprecation.removed_after, format(removed_after, FORMAT_CODE))
    vampytest.assert_eq(event_deprecation.use_instead, use_instead)


def _iter_options__eq():
    removed_after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    trigger_after = DateTime.now(tz = TimeZone.utc) + TimeDelta(days = 5000)
    use_instead = 'koishi'
    
    keyword_parameters = {
        'removed_after': removed_after,
        'trigger_after': trigger_after,
        'use_instead': use_instead,
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
def test__EventDeprecation__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``EventDeprecation.__eq__`` works as intended.
    
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
    event_deprecation_0 = EventDeprecation(**keyword_parameters_0)
    event_deprecation_1 = EventDeprecation(**keyword_parameters_1)
    
    output = event_deprecation_0 == event_deprecation_1
    vampytest.assert_instance(output, bool)
    return output


def test__EventDeprecation__hash():
    """
    Tests whether ``EventDeprecation.__hash__`` works as intended.
    """
    removed_after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    trigger_after = DateTime.now(tz = TimeZone.utc) + TimeDelta(days = 5000)
    use_instead = 'koishi'
    
    event_deprecation = EventDeprecation(
        use_instead,
        removed_after,
        trigger_after = trigger_after,
    )
    
    output = hash(event_deprecation)
    vampytest.assert_instance(output, int)


def test__EventDeprecation__repr():
    """
    Tests whether ``EventDeprecation.__repr__`` works as intended.
    """
    removed_after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    trigger_after = DateTime.now(tz = TimeZone.utc) + TimeDelta(days = 5000)
    use_instead = 'koishi'
    
    event_deprecation = EventDeprecation(
        use_instead,
        removed_after,
        trigger_after = trigger_after,
    )
    
    output = repr(event_deprecation)
    vampytest.assert_instance(output, str)


def test__EventDeprecation__trigger__disallowed():
    """
    Tests whether ``EventDeprecation.trigger`` works as intended.
    
    Case: disallowed.
    """
    removed_after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    trigger_after = DateTime.now(tz = TimeZone.utc) + TimeDelta(days = 5000)
    use_instead = 'koishi'
    
    event_deprecation = EventDeprecation(
        use_instead,
        removed_after,
        trigger_after = trigger_after,
    )
    
    use_instead = 'orin'
    stack_level = 4
    
    def warn_mock(
        message,
        warning_type,
        *,
        stacklevel = 1,
    ):
        raise RuntimeError()
    
    
    mocked = vampytest.mock_globals(
        EventDeprecation.trigger,
        warn = warn_mock,
    )
    
    output = mocked(event_deprecation, use_instead, stack_level)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__EventDeprecation__trigger__allowed():
    """
    Tests whether ``EventDeprecation.trigger`` works as intended.
    
    Case: allowed.
    """
    removed_after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    use_instead = 'koishi'
    
    event_deprecation = EventDeprecation(
        use_instead,
        removed_after,
    )
    
    event_name = 'orin'
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
        
        nonlocal event_name
        nonlocal stack_level
        nonlocal event_deprecation
        nonlocal warn_called
        
        vampytest.assert_in(event_name, message)
        vampytest.assert_in(event_deprecation.use_instead, message)
        vampytest.assert_in(event_deprecation.removed_after, message)
        vampytest.assert_eq(stack_level, stack_level)
        
        warn_called += 1
        
    
    mocked = vampytest.mock_globals(
        EventDeprecation.trigger,
        warn = warn_mock,
    )
    
    output = mocked(event_deprecation, event_name, stack_level)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)

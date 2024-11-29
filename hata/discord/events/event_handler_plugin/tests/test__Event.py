from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..event import Event
from ..event_deprecation import EventDeprecation


async def func_0(a, b):
    pass


async def func_1(a, b, c = None):
    pass


def _assert_fields_set(event):
    """
    Asserts whether the event has all of its fields set.
    
    Parameters
    ----------
    event : ``Event``
        The event to test.
    """
    vampytest.assert_instance(event.default_handler, object)
    vampytest.assert_instance(event.deprecation, EventDeprecation, nullable = True)
    vampytest.assert_instance(event.instance_default_handler, bool)
    vampytest.assert_instance(event.parameter_count, int)


def test__Event__new():
    """
    Tests whether ``Event.__new__`` works as intended.
    """
    parameter_count = 2
    default_handler = func_0
    deprecation = EventDeprecation(
        'satori',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
    )
    
    event = Event(parameter_count, default_handler, deprecation = deprecation)
    
    _assert_fields_set(event)
    vampytest.assert_is(event.default_handler, default_handler)
    vampytest.assert_eq(event.deprecation, deprecation)
    vampytest.assert_eq(event.instance_default_handler, False)
    vampytest.assert_eq(event.parameter_count, parameter_count)


def test__Event__repr():
    """
    Tests whether ``Event.__repr__`` works as intended.
    """
    parameter_count = 2
    default_handler = func_0
    deprecation = EventDeprecation(
        'satori',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
    )
    
    event = Event(parameter_count, default_handler, deprecation = deprecation)
    
    output = repr(event)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    parameter_count = 2
    default_handler = func_1
    deprecation = EventDeprecation(
        'satori',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
    )
    
    keyword_parameters = {
        'parameter_count': parameter_count,
        'default_handler': default_handler,
        'deprecation': deprecation,
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
            'parameter_count': 3,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'default_handler': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'deprecation': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__Event__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``Event.__eq__`` works as intended.
    
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
    event_0 = Event(**keyword_parameters_0)
    event_1 = Event(**keyword_parameters_1)
    
    output = event_0 == event_1
    vampytest.assert_instance(output, bool)
    return output


def test__Event__hash():
    """
    Tests whether ``Event.__hash__`` works as intended.
    """
    parameter_count = 2
    default_handler = func_0
    deprecation = EventDeprecation(
        'satori',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
    )
    
    event = Event(parameter_count, default_handler, deprecation = deprecation)
    
    output = hash(event)
    vampytest.assert_instance(output, int)

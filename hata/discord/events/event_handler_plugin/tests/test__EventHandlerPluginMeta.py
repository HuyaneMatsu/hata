from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...core import DEFAULT_EVENT_HANDLER

from ..event import Event
from ..event_deprecation import EventDeprecation
from ..event_deprecation_descriptor import EventDeprecationDescriptor
from ..meta import EventHandlerPluginMeta


async def func_0(a, b):
    pass


def test__EventHandlerPluginMeta__new():
    """
    Tests whether ``EventHandlerPluginMeta.__new__`` works as intended.
    """
    # First level
    type_name = 'test_type'
    type_parents = (object,)
    type_attributes = {
        'hey': Event(2, func_0),
        'mister': Event(3),
        'remilia': Event(
            1,
            deprecation = EventDeprecation(
                'hey',
                DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
            ),
        ),
        '__slots__': ('orin',),
    }
    
    output_0 = EventHandlerPluginMeta(type_name, type_parents, type_attributes)
    
    vampytest.assert_instance(output_0, EventHandlerPluginMeta)
    vampytest.assert_eq(output_0.__name__, type_name)
    vampytest.assert_eq(output_0.__slots__, ('hey', 'mister', 'orin'),)
    vampytest.assert_eq(
        output_0._plugin_event_names,
        frozenset((
            'hey',
            'mister',
        )),
    )
    vampytest.assert_eq(
        output_0._plugin_default_handlers,
        (
            ('hey', func_0, False),
            ('mister', DEFAULT_EVENT_HANDLER, False),
        ),
    )
    vampytest.assert_eq(
        output_0._plugin_parameter_counts,
        {
            'hey': 2,
            'mister': 3,
        },
    )
    vampytest.assert_eq(
        output_0._plugin_event_deprecations,
        frozenset((
            (
                'remilia',
                EventDeprecation(
                    'hey',
                    DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
                ),
            ),
        )),
    )
    vampytest.assert_eq(
        output_0.remilia,
        EventDeprecationDescriptor(
            'remilia',
            EventDeprecation(
                'hey',
                DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
            ),
        ),
    )
    
    
    # Second level
    type_name = 'test_aya'
    type_parents = (output_0,)
    type_attributes = {
        'sister': Event(2, func_0),
        '__slots__': ('okuu',),
        'flandre': Event(
            4,
            deprecation = EventDeprecation(
                'sister',
                DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
            ),
        ),
    }
    
    output_1 = EventHandlerPluginMeta(type_name, type_parents, type_attributes)
    
    vampytest.assert_subtype(output_1, output_0)
    vampytest.assert_instance(output_1, EventHandlerPluginMeta)
    vampytest.assert_eq(output_1.__name__, type_name)
    vampytest.assert_eq(output_1.__slots__, ('okuu', 'sister'),)
    vampytest.assert_eq(
        output_1._plugin_event_names,
        frozenset((
            'hey',
            'mister',
            'sister',
        )),
    )
    vampytest.assert_eq(
        output_1._plugin_default_handlers,
        (
            ('hey', func_0, False),
            ('mister', DEFAULT_EVENT_HANDLER, False),
            ('sister', func_0, False),
        ),
    )
    vampytest.assert_eq(
        output_1._plugin_parameter_counts,
        {
            'hey': 2,
            'mister': 3,
            'sister': 2,
        },
    )
    vampytest.assert_eq(
        output_1._plugin_event_deprecations,
        frozenset((
            (
                'remilia',
                EventDeprecation(
                    'hey',
                    DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
                ),
            ),
            (
                'flandre',
                EventDeprecation(
                    'sister',
                    DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
                ),
            ),
        )),
    )
    vampytest.assert_eq(
        output_1.flandre,
        EventDeprecationDescriptor(
            'flandre',
            EventDeprecation(
                'sister',
                DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
            ),
        ),
    )


def test__EventHandlerPluginMeta__call():
    """
    Tests whether ``EventHandlerPluginMeta.__call__`` works as intended.
    """
    type_name = 'test_type'
    type_parents = (object,)
    type_attributes = {
        'hey': Event(2, func_0),
        'mister': Event(3),
    }
    
    output = EventHandlerPluginMeta(type_name, type_parents, type_attributes)
    
    instance = output()
    
    vampytest.assert_instance(instance, output)
    vampytest.assert_is(instance.hey, func_0)
    vampytest.assert_is(instance.mister, DEFAULT_EVENT_HANDLER)

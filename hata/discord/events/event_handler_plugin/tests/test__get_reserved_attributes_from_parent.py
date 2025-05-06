from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...core import DEFAULT_EVENT_HANDLER

from ..event_deprecation import EventDeprecation
from ..meta import _get_reserved_attributes_from_parent


async def func_0(a, b):
    pass


class DirectParent(object):
    __slots__ = ('hey', 'mister')
    _plugin_event_names = frozenset(('hey', 'mister'))
    _plugin_default_handlers = (
        ('hey', func_0, False),
        ('mister', DEFAULT_EVENT_HANDLER, False),
    )
    _plugin_parameter_counts = {
        'hey': 2,
        'mister': 3,
    }
    _plugin_event_deprecations = frozenset((
        (
            'remilia',
            EventDeprecation(
                'orin',
                DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
            ),
        ),
        (
            'flandre',
            EventDeprecation(
                'okuu',
                DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
            ),
        ),
    ))


def _iter_options__passing():
    yield (
        type,
        DirectParent,
        (),
        (
            DirectParent._plugin_event_names,
            DirectParent._plugin_default_handlers,
            DirectParent._plugin_parameter_counts,
            DirectParent._plugin_event_deprecations,
        ),
    )
    
    yield (
        int,
        object,
        (object, ),
        (
            None,
            None,
            None,
            None,
        ),
    )


def _iter_options__runtime_error():
    yield (
        int,
        object,
        (DirectParent,),
    )


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__runtime_error()).raising(RuntimeError))
def test__get_reserved_attributes_from_parent(meta_type, direct_parent, type_parents):
    """
    Tests whether ``_get_reserved_attributes_from_parent`` works as intended.
    
    Parameters
    ----------
    meta_type : `type`
        The meta-type.
    
    direct_parent : `type`
        The directly inherited type.
    
    type_parents : `tuple<type>`
        Cumulative parent types.
    
    Returns
    -------
    output : `(None | frozenset<str>, None | tuple<(str, async-callable, bool)>, \
            None | dict<str, int>, None | frozenset<(str, EventDeprecation)>)`
    
    Raises
    ------
    RuntimeError
    """
    output = _get_reserved_attributes_from_parent(meta_type, direct_parent, type_parents)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 4)
    return output

from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..event import Event
from ..event_deprecation import EventDeprecation
from ..meta import _collect_event_deprecations


def _iter_options():
    deprecation_0 = EventDeprecation(
        'orin',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
    )
    
    deprecation_1 = EventDeprecation(
        'okuu',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
    )
    
    yield (
        [],
        None,
        None,
    )
    
    yield (
        [
            ('hey', Event(4, deprecation = deprecation_0)),
        ],
        None,
        frozenset((
            ('hey', deprecation_0),
        )),
    )
    
    yield (
        [
            ('hey', Event(4, deprecation = deprecation_0)),
            ('mister', Event(2, deprecation = deprecation_1)),
        ],
        None,
        frozenset((
            ('hey', deprecation_0),
            ('mister', deprecation_1),
        )),
    )
    
    yield (
        [
            ('hey', Event(4, deprecation = deprecation_0)),
        ],
        frozenset((
            ('mister', deprecation_1),
        )),
        frozenset((
            ('hey', deprecation_0),
            ('mister', deprecation_1),
        )),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test___collect_event_deprecations(events_deprecated, parent_event_deprecations):
    """
    Tests whether ``_collect_event_deprecations`` works as intended.
    
    Parameters
    ----------
    events_deprecated : `list<(str, Event)>`
        Events to collect from.
    
    parent_event_deprecations : `None | frozenset<(str, EventDeprecation)>`
        Event deprecations of the parent.
    
    Returns
    -------
    output : `None | frozenset<(str, EventDeprecation)>`
    """
    output = _collect_event_deprecations(events_deprecated, parent_event_deprecations)
    vampytest.assert_instance(output, frozenset, nullable = True)
    return output

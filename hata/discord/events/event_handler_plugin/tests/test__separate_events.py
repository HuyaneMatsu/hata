from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..event import Event
from ..event_deprecation import EventDeprecation
from ..meta import _separate_events


def _iter_options():
    yield (
        {
            'orin': 'carting',
        },
        (
            (
                [],
                [],
            ),
            {
                'orin': 'carting',
            },
        )
    )
    
    yield (
        {
            'orin': 'carting',
            'hey': Event(2),
            'mister': Event(3),
        },
        (
            (
                [
                    ('hey', Event(2)),
                    ('mister', Event(3)),
                ],
                [],
            ),
            {
                'orin': 'carting',
            },
        )
    )
    
    yield (
        {
            'orin': 'carting',
            'hey': Event(
                2,
                deprecation = EventDeprecation(
                    'orin',
                    DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
                ),
            ),
        },
        (
            (
                [],
                [
                    (
                        'hey',
                        Event(
                            2,
                            deprecation = EventDeprecation(
                                'orin',
                                DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
                            ),
                        ),
                    ),
                ]
            ),
            {
                'orin': 'carting',
            },
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__separate_events(type_attributes):
    """
    Tests whether ``_separate_events`` works as intended.
    
    Parameters
    ----------
    type_attributes : `dict<str, object>`
        Type attributes.
    
    Returns
    -------
    output : `(list<(str, Event)>, list<(str, Event)>)`
    type_attributes : `dict<str, object>`
    """
    type_attributes = type_attributes.copy()
    output = _separate_events(type_attributes)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    return output, type_attributes

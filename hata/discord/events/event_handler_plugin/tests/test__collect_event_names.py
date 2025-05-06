import vampytest

from ..event import Event
from ..meta import _collect_event_names


def _iter_options():
    yield (
        [],
        None,
        None,
    )
    
    yield (
        [
            ('hey', Event(2)),
        ],
        None,
        frozenset((
            'hey',
        )),
    )
    
    yield (
        [
            ('hey', Event(2)),
            ('mister', Event(3)),
        ],
        None,
        frozenset((
            'hey',
            'mister',
        )),
    )
    
    yield (
        [
            ('hey', Event(2)),
        ],
        frozenset((
            'mister',
        )),
        frozenset((
            'hey',
            'mister',
        )),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__collect_event_names(events, parent_event_names):
    """
    Tests whether ``_collect_event_names`` works as intended.
    
    Parameters
    ----------
    events : `list<(str, Event)>`
        Events to collect from.
    
    parent_event_names : `None | frozenset<str>`
        Event names of the parent type.
    
    Returns
    -------
    output : `None | frozenset<str>`
    """
    output = _collect_event_names(events, parent_event_names)
    vampytest.assert_instance(output, frozenset, nullable = True)
    return output

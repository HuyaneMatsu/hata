import vampytest

from ..event import Event
from ..meta import _collect_parameter_counts


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
        {
            'hey': 2,
        },
    )
    
    yield (
        [
            ('hey', Event(2)),
            ('mister', Event(3)),
        ],
        None,
        {
            'hey': 2,
            'mister': 3,
        },
    )
    
    yield (
        [
            ('hey', Event(2)),
        ],
        {
            'mister': 3,
        },
        {
            'hey': 2,
            'mister': 3,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test___collect_parameter_counts(events, parent_parameter_counts):
    """
    Tests whether ``_collect_parameter_counts`` works as intended.
    
    Parameters
    ----------
    events : `list<(str, Event)>`
        Events to collect from.
    
    parent_parameter_counts : `None | dict<str, int>`
        Parameter counts of the parent type.
    
    Returns
    -------
    output : `None | dict<str, int>`
    """
    output = _collect_parameter_counts(events, parent_parameter_counts)
    vampytest.assert_instance(output, dict, nullable = True)
    return output

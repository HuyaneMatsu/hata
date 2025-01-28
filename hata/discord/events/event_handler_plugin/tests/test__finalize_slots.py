import vampytest

from ..event import Event
from ..meta import _finalize_slots


async def func_0(a, b):
    pass


class type_1:
    async def __call__(self, a, b):
        pass


def _iter_options():
    yield (
        [],
        set(),
        (),
    )
    
    yield (
        [
            ('hey', Event(2)),
        ],
        set(),
        (
            'hey',
        ),
    )
    
    yield (
        [
            ('hey', Event(2)),
            ('mister', Event(3)),
        ],
        set(),
        (
            'hey',
            'mister',
        ),
    )
    
    yield (
        [
            ('hey', Event(2)),
        ],
        {
            'mister',
        },
        (
            'hey',
            'mister',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__finalize_slots(events, slots):
    """
    Tests whether ``_finalize_slots`` works as intended.
    
    Parameters
    ----------
    events : `list<(str, Event)>`
        Events to collect from.
    
    slots : `set<str>`
        Already collected slots.
    
    Returns
    -------
    output : `tuple<str>`
    """
    slots = slots.copy()
    output = _finalize_slots(events, slots)
    vampytest.assert_instance(output, tuple)
    return output

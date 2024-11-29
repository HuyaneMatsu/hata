import vampytest

from ...core import DEFAULT_EVENT_HANDLER

from ..event import Event
from ..meta import _collect_default_handlers


async def func_0(a, b):
    pass


class type_1:
    async def __call__(self, a, b):
        pass


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
        (
            ('hey', DEFAULT_EVENT_HANDLER, False),
        ),
    )
    
    yield (
        [
            ('hey', Event(2)),
            ('mister', Event(3)),
        ],
        None,
        (
            ('hey', DEFAULT_EVENT_HANDLER, False),
            ('mister', DEFAULT_EVENT_HANDLER, False),
        ),
    )
    
    yield (
        [
            ('hey', Event(2, func_0)),
        ],
        None,
        (
            ('hey', func_0, False),
        ),
    )
    
    yield (
        [
            ('hey', Event(2, type_1)),
        ],
        None,
        (
            ('hey', type_1, True),
        ),
    )
    
    yield (
        [
            ('hey', Event(2)),
        ],
        (
            ('mister', DEFAULT_EVENT_HANDLER, False),
        ),
        (
            ('mister', DEFAULT_EVENT_HANDLER, False),
            ('hey', DEFAULT_EVENT_HANDLER, False),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test___collect_default_handlers(events, parent_default_handlers):
    """
    Tests whether ``_collect_default_handlers`` works as intended.
    
    Parameters
    ----------
    events : `list<(str, Event)>`
        Events to collect from.
    
    parent_default_handlers : `None | tuple<(str, async-callable, bool)>`
        Default handlers of parents.
    
    Returns
    -------
    output : `None | tuple<(str, async-callable, bool)>`
    """
    output = _collect_default_handlers(events, parent_default_handlers)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output

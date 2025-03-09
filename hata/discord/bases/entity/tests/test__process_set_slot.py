import vampytest

from ..slotted_meta import _process_set_slot


def _iter_options():
    class TypeThatAddsSlot():
        def __set_slot__(self, attribute_name, type_attributes, type_slots):
            type_slots.add('_' + attribute_name)
            type_slots.add('miau')
            
    
    # noting to add from.
    yield (
        {
            'hey': 'mister',
        },
        set(),
        set(),
    )
    
    # ignore types
    yield (
        {
            'hey': TypeThatAddsSlot,
        },
        set(),
        set(),
    )
    
    # ignore types
    yield (
        {
            'hey': TypeThatAddsSlot(),
        },
        set(),
        {'miau', '_hey'},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__process_set_slot(type_attributes, final_slots):
    """
    Tests whether ``_process_set_slot`` works as intended.
    
    Parameters
    ----------
    type_attributes : `dict<str, object>`
        The type attributes of the created type.
    
    final_slots : `set<str>`
        Slots for the created type.
    
    Returns
    -------
    output : `set<str>`
    """
    final_slots = final_slots.copy()
    _process_set_slot(type_attributes, final_slots)
    return final_slots

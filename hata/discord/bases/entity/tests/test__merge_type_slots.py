import vampytest

from ..slotted_meta import _merge_type_slots


def _iter_options():
    class TypeWithWeakref():
        __slots__ = ('__weakref__',)
    
    class TypeWithInheritableSlots0():
        _TypeWithInheritableSlots0__slots = ('miau', 'nyan')
    
    class TypeWithInheritableSlots1():
        _TypeWithInheritableSlots1__slots = ('mrr',)
    
    class TypeDoNotDiscard():
        mrr = 56
    
    class TypeDoDiscard():
        __slots__ = ('mrr',)
    
    
    yield (
        None,
        (),
        {},
        set(),
    )
    
    # inherit slots
    yield (
        TypeWithInheritableSlots0,
        (TypeWithInheritableSlots0, TypeWithInheritableSlots1),
        {},
        {
            'miau',
            'nyan',
            'mrr',
        },
    )
    
    # inherit if not slot
    yield (
        TypeDoNotDiscard,
        (TypeDoNotDiscard, TypeWithInheritableSlots1),
        {},
        {
            'mrr',
        },
    )
    
    # omit if slot
    yield (
        TypeDoDiscard,
        (TypeDoDiscard, TypeWithInheritableSlots1),
        {},
        set(),
    )
    
    # detect slots
    yield (
        None,
        (),
        {
            '__slots__' : (
                'nyan',
                'nyanner',
            ),
        },
        {
            'nyan',
            'nyanner',
        },
    )
    
    # Keep new weakref
    yield (
        None,
        (),
        {
            '__slots__' : (
                '__weakref__',
            ),
        },
        {
            '__weakref__',
        },
    )
    
    # do not keep new weakref if we already have it
    yield (
        TypeWithWeakref,
        (TypeWithWeakref,),
        {
            '__slots__' : (
                '__weakref__',
            ),
        },
        set(),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__merge_type_slots(direct_parent, type_parents, type_attributes):
    """
    Tests whether ``_merge_type_slots`` works as intended.
    
    Parameters
    ----------
    direct_parent : `None | type`
        The direct parent of the respective type.
    
    type_parents : `tuple<type>`
        The parent types of the creates type.
    
    type_attributes : `dict<str, object>`
        The type attributes of the created type.
    
    Returns
    -------
    output : `set<str>`
    """
    output = _merge_type_slots(direct_parent, type_parents, type_attributes)
    vampytest.assert_instance(output, set)
    return output

import vampytest

from ..slotted_meta import Slotted


def test__Slotted__new():
    """
    Tests whether ``Slotted.__new__`` works as intended.
    """
    class SideParent():
        _SideParent__slots = ('miau',)
    
    class DirectParent():
        __slots__ = ('mister',)
        def __hash__(self):
            return 0
    
    class SetSlotter():
        def __set_slot__(self, attribute_name, type_attributes, type_slots):
            type_slots.add('_' + attribute_name)
    
    
    output = Slotted(
        'name',
        (DirectParent, SideParent),
        {
            '__slots__': ('nyan', 'cat',),
            'avar': SetSlotter(),
        },
    )
    
    vampytest.assert_eq(
        output.__slots__,
        ('_avar', 'cat', 'miau', 'nyan'),
    )
    vampytest.assert_is(
        output.__hash__,
        DirectParent.__hash__,
    )

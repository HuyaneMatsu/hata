import vampytest

from ..discord_entity_meta import DiscordEntityMeta, ENTITY_ID_PLACEHOLDER


def test__DiscordEntityMeta__new():
    """
    Tests whether ``DiscordEntityMeta.__new__`` works as intended.
    """
    class SideParent():
        _SideParent__slots = ('miau',)
    
    class DirectParent():
        id = ENTITY_ID_PLACEHOLDER
        __slots__ = ('mister', '__weakref__')
        def __hash__(self):
            return 0
    
    class SetSlotter():
        def __set_slot__(self, attribute_name, type_attributes, type_slots):
            type_slots.add('_' + attribute_name)
    
    
    output = DiscordEntityMeta(
        'name',
        (DirectParent, SideParent),
        {
            '__slots__': ('nyan', 'cat',),
            'avar': SetSlotter(),
        },
        immortal = True,
    )
    
    vampytest.assert_eq(
        output.__slots__,
        ('_avar', 'cat', 'id', 'miau', 'nyan'),
    )
    vampytest.assert_is(
        output.__hash__,
        DirectParent.__hash__,
    )

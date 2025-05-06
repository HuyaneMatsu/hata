__all__ = ()

from ..place_holder import PlaceHolder

from .slotted_meta import _get_direct_parent, _inherit_hash, _merge_type_slots, _process_set_slot, Slotted


ENTITY_ID_PLACEHOLDER = PlaceHolder(
    0,
    """
    Returns the discord entity's unique identifier number
    
    Returns
    -------
    id : `int`
    """
)


class DiscordEntityMeta(Slotted):
    """
    Meta type of Discord entities. Use ``DiscordEntity`` as parent type instead of using this type directly as a
    meta type.
    """
    def __new__(cls, type_name, type_parents, type_attributes, *, immortal = False):
        """
        Creates a Discord entity type. Sub-type ``DiscordEntity`` instead of using this type directly as a meta type.
        
        Parameters
        ----------
        type_name : `str`
            The created type's name.
        
        type_parents : `tuple<type>`
            The parent types of the creates type.
        
        type_attributes : `dict<str, object>`
            The type attributes of the created type.
        
        immortal : `bool` = `False`, Optional (Keyword only)
            Whether the created type's instances should support weakreferencing. If the inherited type supports
            weakreferencing, then the sub-type will as well of course.
        
        Returns
        -------
        type : ``DiscordEntityMeta``
        
        Notes
        -----
        The created instances are always slotted.
        
        When more types are inherited then use `__slots` at the secondary types for adding additional member
        descriptors.
        """
        direct_parent = _get_direct_parent(cls, type_name, type_parents)
        final_slots = _merge_type_slots(direct_parent, type_parents, type_attributes)
        _process_set_slot(type_attributes, final_slots)
        _inherit_hash(direct_parent, type_attributes)
        
        if immortal:
            for type_parent in type_parents:
                if hasattr(type_parent, '__weakref__'):
                    break
            else:
                final_slots.add('__weakref__')
        
        if (
            (direct_parent is not None) and
            ('id' not in type_attributes) and
            hasattr(direct_parent, 'id') and
            (direct_parent.id is ENTITY_ID_PLACEHOLDER)
        ):
            final_slots.add('id')
        
        type_attributes['__slots__'] = tuple(sorted(final_slots))
        
        return type.__new__(cls, type_name, type_parents, type_attributes)

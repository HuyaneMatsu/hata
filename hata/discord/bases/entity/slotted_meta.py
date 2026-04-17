__all__ = ('Slotted', )

from itertools import islice
from types import MemberDescriptorType


def _get_direct_parent(meta_type, type_name, type_parents):
    """
    Gets the direct parent of the specified type definition and it's merged slots.
    
    Parameters
    ----------
    type_name : `str`
        The created type's name.
    
    type_parents : `tuple<type>`
        The parent types of the creates type.
    
    type_attributes : `dict<str, object>`
        The type attributes of the created type.
    
    Returns
    -------
    direct_parent : `None | type`
        The direct parent of the respective type.
    
    Raises
    ------
    RuntimeError
    """
    parent_count = len(type_parents)
    if parent_count > 0:
        direct_parent = type_parents[0]
    else:
        direct_parent = None
    
    for type_parent in islice(type_parents, 1, None):
        if isinstance(type_parent, meta_type):
            raise RuntimeError(
                f'`{type_name}` wanted to inherit a `{meta_type.__name__}` type not as it\'s direct '
                f'(0th) parent type.'
            )
    
    return direct_parent


def _inherit_hash(direct_parent, type_attributes):
    """
    Inherits the hasher into the type attributes because someone decided to pop it.
    
    Parameters
    ----------
    direct_parent : `None | type`
        The direct parent of the respective type.
    
    type_attributes : `dict<str, object>`
        The type attributes of the created type.
    """
    # Sub-types might miss hash, lmeow
    if (direct_parent is not None) and type_attributes.get('__hash__', None) is None:
        type_attributes['__hash__'] = direct_parent.__hash__


def _merge_type_slots(direct_parent, type_parents, type_attributes):
    """
    Merges the new values into the slots of the type.
    
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
    final_slots : `set<str>`
        Slots for the created type.
    """
    final_slots = set()
    
    if (direct_parent is not None):
        for type_parent in type_parents:
            for slot_name in getattr(type_parent, f'_{type_parent.__name__}__slots', ()):
                existing_attribute = getattr(direct_parent, slot_name, None)
                if (existing_attribute is not None) and isinstance(existing_attribute, MemberDescriptorType):
                    continue
                
                final_slots.add(slot_name)
    
    slots = type_attributes.get('__slots__', None)
    if (slots is not None) and slots:
        final_slots.update(slots)
    
    # Remove weakref if we already have it
    if (direct_parent is not None) and hasattr(direct_parent, '__weakref__'):
        try:
            final_slots.remove('__weakref__')
        except KeyError:
            pass
    
    return final_slots


def _process_set_slot(type_attributes, final_slots):
    """
    Processes type attributes, which implement  `__set_slot__`.
    
    Parameters
    ----------
    type_attributes : `dict<str, object>`
        The type attributes of the created type.
    
    final_slots : `set<str>`
        Slots for the created type.
    """
    slotters = []
    for attribute_item in type_attributes.items():
        attribute_value = attribute_item[1]
        
        # Ignore types.
        if isinstance(attribute_value, type):
            continue
        
        # Check the type, whether it has the correct method.
        set_slot = getattr(type(attribute_value), '__set_slot__', None)
        if set_slot is None:
            continue
        
        # Queue up for future applications.
        slotters.append(attribute_item)
        continue
    
    # Apply slotters
    while slotters:
        attribute_name, slotter = slotters.pop()
        type(slotter).__set_slot__(slotter, attribute_name, type_attributes, final_slots)


class Slotted(type):
    """
    Meta type for special slotted objects, which require `__set_slot__`.
    """
    def __new__(cls, type_name, type_parents, type_attributes):
        """
        Creates a new ``Slotted``.
        
        Parameters
        ----------
        type_name : `str`
            The created type's name.
        
        type_parents : `tuple<type>`
            The sub-types of the creates type.
        
        type_attributes : `dict<str, object>`
            The type attributes of the created type.
        """
        direct_parent = _get_direct_parent(cls, type_name, type_parents)
        final_slots = _merge_type_slots(direct_parent, type_parents, type_attributes)
        _process_set_slot(type_attributes, final_slots)
        _inherit_hash(direct_parent, type_attributes)
        
        type_attributes['__slots__'] = tuple(sorted(final_slots))
        
        return type.__new__(cls, type_name, type_parents, type_attributes)

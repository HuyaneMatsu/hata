__all__ = ('DiscordEntity', 'Slotted', )

from scarletio import RichAttributeErrorBaseType, include

from .place_holder import PlaceHolder

id_to_datetime = include('id_to_datetime')


def _get_direct_parents_and_merge_slots(class_name, class_parents, class_attributes):
    """
    Gets the direct parent of the specified class definition and it's merged slots.
    
    Parameters
    ----------
    class_name : `str`
        The created class's name.
    class_parents : `tuple` of `type`
        The superclasses of the creates type.
    class_attributes : `dict` of (`str`, `Any`) items
        The class attributes of the created type.
    
    Returns
    -------
    direct_parent : `None`, `type`
        The direct parent of the respective class.
    final_slots : `set` of `str`
        Slots for the created type.
    """
    final_slots = set()
    
    parent_count = len(class_parents)
    if parent_count > 0:
        direct_parent = class_parents[0]
    else:
        direct_parent = None
    
    for class_parent in class_parents[1:]:
        if isinstance(class_parent, DiscordEntity):
            raise RuntimeError(
                f'`{class_name}` wanted to inherit `{DiscordEntity.__name__}` not as it\'s direct '
                f'(1st) parent type.'
            )
    
    if (direct_parent is not None):
        # Subclasses might miss hash!
        if class_attributes.get('__hash__', None) is None:
            class_attributes['__hash__'] = direct_parent.__hash__
        
        # Remove weakref to avoid error
        try:
            final_slots.remove('__weakref__')
        except KeyError:
            pass
        
        index = 1
        while index < parent_count:
            class_parent = class_parents[index]
            final_slots.update(getattr(class_parent, f'_{class_parent.__name__}__slots', ()))
            index += 1
    
    slots = class_attributes.get('__slots__',)
    if (slots is not None) and slots:
        final_slots.update(slots)
    
    return direct_parent, final_slots


def _process_set_slot(class_attributes, final_slots):
    """
    Processes class attributes, which implement  `__set_slot__`.
    
    Parameters
    ----------
    class_attributes : `dict` of (`str`, `Any`) items
        The class attributes of the created type.
    final_slots : `set` of `str`
        Slots for the created type.
    """
    slotters = []
    for attribute_item in class_attributes.items():
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
        type(slotter).__set_slot__(slotter, attribute_name, class_attributes, final_slots)


class Slotted(type):
    """
    Metaclass for special slotted objects, which require `__set_slot__`.
    """
    def __new__(cls, class_name, class_parents, class_attributes):
        """
        Creates a new ``Slotted``.
        
        Parameters
        ----------
        class_name : `str`
            The created class's name.
        class_parents : `tuple` of `type`
            The superclasses of the creates type.
        class_attributes : `dict` of (`str`, `Any`) items
            The class attributes of the created type.
        """
        direct_parent, final_slots = _get_direct_parents_and_merge_slots(class_name, class_parents, class_attributes)
        _process_set_slot(class_attributes, final_slots)
        class_attributes['__slots__'] = tuple(sorted(final_slots))
        
        return type.__new__(cls, class_name, class_parents, class_attributes)


class DiscordEntityMeta(Slotted):
    """
    Metaclass of Discord entities. Use ``DiscordEntity`` as superclass instead of using this class directly as a
    metaclass.
    """
    def __new__(cls, class_name, class_parents, class_attributes, immortal=False):
        """
        Creates a Discord entity type. Subclass ``DiscordEntity`` instead of using this class directly as a metaclass.
        
        Parameters
        ----------
        class_name : `str`
            The created class's name.
        class_parents : `tuple` of `type`
            The superclasses of the creates type.
        class_attributes : `dict` of (`str`, `Any`) items
            The class attributes of the created type.
        immortal : `bool` = `False`, Optional
            Whether the created type's instances should support weakreferencing. If the inherited type supports
            weakreferencing, then the subclass will as well of course.
        
        Returns
        -------
        type : ``DiscordEntityMeta``
        
        Notes
        -----
        The created instances are always slotted.
        
        When more classes are inherited then use `__slots` at the secondary classes for adding additional member
        descriptors.
        """
        direct_parent, final_slots = _get_direct_parents_and_merge_slots(class_name, class_parents, class_attributes)
        _process_set_slot(class_attributes, final_slots)
        
        if immortal:
            for class_parent in class_parents:
                if hasattr(class_parent, '__weakref__'):
                    break
            else:
                final_slots.add('__weakref__')
        
        if (direct_parent is not None) and ('id' not in class_attributes) and (direct_parent.id is DiscordEntity.id):
            final_slots.add('id')
        
        class_attributes['__slots__'] = tuple(sorted(final_slots))
        
        return type.__new__(cls, class_name, class_parents, class_attributes)


class DiscordEntity(RichAttributeErrorBaseType, metaclass=DiscordEntityMeta):
    """
    Base class for Discord entities.
    
    Notes
    -----
    Inherit it with passing `immortal = True` to make the subclass weakreferable.
    """
    id = PlaceHolder(
        0,
        """
        Returns the discord entity's unique identifier number
        
        Returns
        -------
        id : `int`
        """
    )
    
    __slots__ = ()
    
    @property
    def created_at(self):
        """
        When the entity was created.
        
        Returns
        -------
        created_at : `datetime`
        """
        return id_to_datetime(self.id)
    
    def __hash__(self):
        """Returns the has value of the entity, what equals to it's id."""
        return self.id
    
    def __gt__(self, other):
        """Whether this entity's id is greater than the other's."""
        if type(self) is type(other):
            return self.id > other.id
        
        return NotImplemented
    
    def __ge__(self, other):
        """Whether this entity's id is greater or equal than the other's."""
        if type(self) is type(other):
            return self.id >= other.id
        
        return NotImplemented
    
    def __eq__(self, other):
        """Whether this entity's id is equal as the other's."""
        if type(self) is type(other):
            return self.id == other.id
        
        return NotImplemented
    
    def __ne__(self, other):
        """Whether this entity's id is not equal as the other's."""
        if type(self) is type(other):
            return self.id != other.id
        
        return NotImplemented
    
    def __le__(self, other):
        """Whether this entity's id is less or equal than the other's."""
        if type(self) is type(other):
            return self.id <= other.id
        
        return NotImplemented
    
    def __lt__(self, other):
        """Whether this entity's id is less than the other's."""
        if type(self) is type(other):
            return self.id < other.id
        
        return NotImplemented

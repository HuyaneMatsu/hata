﻿# -*- coding: utf-8 -*-
__all__ = ('DiscordEntity', 'ICON_TYPE_ANIMATED', 'ICON_TYPE_NONE', 'ICON_TYPE_STATIC', 'Icon', 'IconType',
    'IconSlot', 'instance_or_id_to_instance', 'instance_or_id_to_snowflake', )

import sys

from ..backend.dereaddons_local import _spaceholder

id_to_time = NotImplemented

class DiscordEntityMeta(type):
    """
    Metaclass of Discord entities. Use ``DiscordEntity`` as superclass instead of using this class directly as a
    metaclass.
    """
    def __new__(cls, class_name, class_parents, class_attributes, immortal=False):
        """
        Creates a Discord entity type. Subclass ``DiscordEntity`` instead of using this class diractly as a mtaclass.
        
        Parameters
        ----------
        class_name : `str`
            The created classe's name.
        class_parents : `tuple` of `type` instances
            The superclasses of the creates type.
        class_attributes : `dict` of (`str`, `Any`) items
            The class attributes of the created type.
        immortal : `bool`, Optional
            Whether the created type's instances should support weakreferencing. If the inherited type supports
            weakreferening, then the subclass will as well of cource. Defaults to `False`.
        
        Returns
        -------
        type : ``DiscordEntityMeta`` instance
        
        Notes
        -----
        The created instances are always slotted.
        
        When more classes are inherited then use `__slots` at the secondary classes for adding additional member
        descriptors.
        """
        final_slots = set()
        
        parent_count = len(class_parents)
        if parent_count > 0:
            parent = class_parents[0]
            final_slots.update(getattr(parent, '__slots__', ()))
            
            #Sublasses might miss hash!
            if class_attributes.get('__hash__', None) is None:
                class_attributes['__hash__'] = parent.__hash__
            
            # Remove weakref to avoid error
            try:
                final_slots.remove('__weakref__')
            except KeyError:
                pass
            
            index = 1
            while index < parent_count:
                parent = class_parents[index]
                final_slots.update(getattr(parent, f'_{parent.__name__}__slots', ()))
                index +=1
        
        slots = class_attributes.get('__slots__',)
        if (slots is not None) and slots:
            final_slots.update(slots)
        
        if immortal:
            for parent in class_parents:
                if hasattr(parent, '__weakref__'):
                    break
            else:
                final_slots.add('__weakref__')
        
        if 'id' not in class_attributes:
            final_slots.add('id')
        
        slotters = []
        for attribute_item in class_attributes.items():
            attribute_value = attribute_item[1]
            
            # Ignroe types.
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
        
        class_attributes['__slots__'] = tuple(sorted(final_slots))
        
        return type.__new__(cls, class_name, class_parents, class_attributes)

class DiscordEntity(object, metaclass = DiscordEntityMeta):
    """
    Base class for Discord entities.
    
    Notes
    -----
    Inherit it with passing `immortal = True` to make the subclass weakreferable.
    """
    @property
    def id(self):
        """
        Returns the discord entity's unique identificator number
        
        Returns
        -------
        id . `int`
        """
        return 0
    
    __slots__ = ()
    
    @property
    def created_at(self):
        """
        When the entity was created.
        
        Returns
        -------
        created_at : `datetime`
        """
        return id_to_time(self.id)
    
    def __hash__(self):
        """Returns the has value of the entity, what quals to it's id."""
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

class FlagGetDescriptor(object):
    """
    Returns the flag descriptor's owner's value at a specific byte vize position.
    
    Attributes
    ----------
    shift : `int`
        The byte vize position of the atrribute what this flag represents.
    """
    __slots__ = ('shift', )
    def __init__(self, shift):
        self.shift = shift
    
    def __get__(self, instance, type_=None):
        if instance is None:
            return self
        else:
            return (instance>>self.shift)&1
    
    def __call__(self, value):
        return (value>>self.shift)&1
    
    def __set__(self, obj, value):
        raise AttributeError('can\'t set attribute')
    
    def __delete__(self, obj):
        raise AttributeError('can\'t delete attribute')

class ReverseFlagGetDescriptor(FlagGetDescriptor):
    """
    Returns the flag descriptor's owner's reversed value at a specific byte vize position.
    
    This type is a reversed version of ``FlagGetDescriptor``, so it returns `0` when th value has `1` at the specific
    byte vize position.
    
    Attributes
    ----------
    shift : `int`
        The byte vize position of the atrribute, what this flag represents.
    """
    def __get__(self, instance, type_=None):
        if instance is None:
            return self
        else:
            return ((instance>>self.shift)&1)^1
    
    def __call__(self, value):
        return ((value>>self.shift)&1)^1

class FlagEnabler(object):
    """
    Enables a specific byte vize flag of a given value by returning a new one with the given byte vize flag enabled.
    
    This type is instanced by ``FlagEnableDescriptor`` objects, when they are accessed as instance attribute.
    
    Attributes
    ----------
    instance : ``FlagMeta`` instance's instance
        The source value, what will be modified.
    shift : `int`
        The byte vize position, what will be modified.
    
    Notes
    -----
    This type is used for disabling specific byte vize values when the source flag is a reversed flag.
    """
    __slots__ = ('instance', 'shift')
    
    def __call__(self):
        instance = self.instance
        shift = self.shift
        return int.__new__(type(instance), (instance|(1<<self.shift)))

class FlagEnableDescriptor(FlagGetDescriptor):
    """
    Descriptor for enabling a specific bytevize value of a flag. After this descriptor is accessed as an instance
    attribute, a ``FlagEnabler`` is returned, and calling that will return a new instance with it's byte vize flag
    value enabled.
    
    Attributes
    ----------
    shift : `int`
        The byte vize position of the atrribute what this flag represents.
    
    Notes
    -----
    This type is used for disabling specific byte vize values when the source flag is a reversed flag.
    """
    def __get__(self, instance, type_=None):
        if instance is None:
            return self
        else:
            result = FlagEnabler()
            result.instance = instance
            result.shift = self.shift
            return result

class FlagDisabler(object):
    """
    Disables a specific byte vize flag of a given value by returning a new one with the given byte vize flag disabled.
    
    This type is instanced by ``FlagDisableDescriptor`` objects, when they are accessed as instance attribute.
    
    Attributes
    ----------
    instance : ``FlagMeta`` instance's instance
        The source value, what will be modified.
    shift : `int`
        The byte vize position, what will be modified.
    
    Notes
    -----
    This type is used for enable specific byte vize values when the source flag is a reversed flag.
    """
    __slots__ = ('instance', 'shift')
    
    def __call__(self):
        instance = self.instance
        shift = self.shift
        if (instance>>shift)&1:
            return int.__new__(type(instance), (instance^(1<<shift)))
        else:
            return instance

class FlagDisableDescriptor(FlagGetDescriptor):
    """
    Descriptor for disabling a specific bytevize value of a flag. After this descriptor is accessed as an instance
    attribute, a ``FlagDisabler`` is returned, and calling that will return a new instance with it's byte vize flag
    value disabled.
    
    Attributes
    ----------
    shift : `int`
        The byte vize position of the atrribute what this flag represents.
    
    Notes
    -----
    This type is used for enabling specific byte vize values when the source flag is a reversed flag.
    """
    def __get__(self, instance, type_=None):
        if instance is None:
            return self
        else:
            result = FlagDisabler()
            result.instance = instance
            result.shift = self.shift
            return result

class FlagMeta(type):
    """
    Metaclass for byte vize flags.
    """
    def __new__(cls, class_name, class_parents, class_attributes, access_keyword=None, enable_keyword=None,
            disable_keyword=None, baseclass=False):
        """
        Creates a byte vize flag type.
        
        Parameters
        ----------
        class_name : `str`
            The created classe's name.
        class_parents : `tuple` of `type` instances
            The superclasses of the creates type.
        class_attributes : `dict` of (`str`, `Any`) items
            The class attributes of the created type.
        access_keyword : `str`, Optional
            The string what will go before the descriptor's name, which allow accessing their respective value. If not
            defined, the there will be no keyword before them.
        enable_keyword : `str`, Optional
            Whether enabling descriptors should be added to the created type. The passed string will be before the
            enabling descriptor's name. If not defined, then the created type will not have flag enablers.
        disable_keyword : `str`, Optional
            Whether disabling descriptors should be added to the created type. The passed string will be before the
            disabling descriptor's name. If not defined, then the created type will not have flag disablers.
        baseclass : `bool`, Optional
            Whether the created type is a base class for flags. If it is:
                - Should directly derived from `int`.
                - Should not implement `__keys__` (exceept `NotImplemented`).
                - Should implement `__getter_class__` class attribute.
                - Should implement `__enabler_class__` class attribute.
                - Should implement `__disabler_class__` class attribute.
            If not, then:
                - Should deriver directly from a ``FlagMeta`` baseclass.
                - Should implement `__keys__` as `dict` of (`str`, `int`) items, where the values are not less than
                    `0`, and not greater than `63` either.
        
        Returns
        -------
        type : ``FlagMeta`` instance
        
        Raises
        ------
        TypeError
            When any requirements are not satisfied.
        """
        if baseclass:
            if (not class_parents) or (not issubclass(class_parents[0], int)):
                raise TypeError(f'`{class_name}` is not derived directly from `int`.')
            
            class_keys = class_attributes.get('__keys__', _spaceholder)
            if class_keys is NotImplemented:
                pass
            elif class_keys is _spaceholder:
                class_attributes['__keys__'] = NotImplemented
            else:
                raise TypeError(f'`{class_name}` has `__keys__` defined and not as `NotImplemented`.')
            
            for attribute_name in ('__getter_class__', '__enabler_class__', '__disabler_class__'):
                if attribute_name not in class_attributes:
                    raise TypeError(f'`{class_name}` should implemnt a `{attribute_name}`.')
            
            # do not care about the leftover
            
            return type.__new__(cls, class_name, class_parents, class_attributes)
        
        # Python has no GOTO, so lets insert one
        while True:
            if class_parents:
                parent = class_parents[0]
                if (type(parent) is FlagMeta) and parent.__keys__ is NotImplemented:
                    break
            
            raise TypeError(f'`{class_name}` is not derived directly from a `{cls.__name__}` base instance.')
        
        # Validate keys
        try:
            keys = class_attributes['__keys__']
        except KeyError:
            raise TypeError(f'`{class_name}` did not define `__keys__` attribute.') from None
        
        if (type(keys) is not dict):
            raise TypeError(f'`__keys__` defined as non `dict`: `{keys.__class__.__name__}`.')
        
        for name, shift in keys.items():
            if (type(name) is not str):
                raise TypeError('`__keys__`\'s keys should be `str` instances, meanwhile got at least 1 non `str`: '
                    f'{name!r}.')
            
            if (type(shift) is not int):
                raise TypeError('`__keys__`\'s values should be `int` instances, meanwhile got at least 1 non `int`: '
                    f'{shift!r}.')
            
            if shift < 0 or shift > 63:
                raise TypeError(f'`__keys__`\' values must be between 0 and 63, got: {shift!r}')
        
        class_attributes.setdefault('__new__', int.__new__)
        
        getter = parent.__getter_class__
        enabler = parent.__enabler_class__
        disabler = parent.__disabler_class__
        
        # Add properties
        for name, shift in keys.items():
            if access_keyword is None:
                access_name = name
            else:
                access_name = f'{access_keyword}_{name}'
            
            class_attributes[access_name] = getter(shift)
            
            if (enable_keyword is not None):
                class_attributes[f'{enable_keyword}_{name}'] = enabler(shift)
            
            if (disable_keyword is not None):
                class_attributes[f'{disable_keyword}_{name}'] = disabler(shift)
        
        return type.__new__(cls, class_name, class_parents, class_attributes)

class FlagBase(int, metaclass = FlagMeta, baseclass=True):
    """
    Base class for byte vize flags.
    
    Class attributes
    ----------------
    __getter_class__ : ``FlagGetDescriptor``
        Flag value getter descriptor for subclasses.
    __enabler_class__ : ``FlagEnableDescriptor``
        Flag enabler descriptor for subclasses.
    __disabler_class__ : ``FlagDisableDescriptor``
        Flag disabler descriptor for subclasses.
    """
    __slots__ = ()
    __keys__ = NotImplemented
    
    __getter_class__ = FlagGetDescriptor
    __enabler_class__ = FlagEnableDescriptor
    __disabler_class__ = FlagDisableDescriptor
    
    def __new__(self, base=None):
        """You cannot subclass flag base classes."""
        raise NotImplementedError
    
    def __repr__(self):
        """Returns the reprsentation of the flag."""
        return f'{self.__class__.__name__}({int.__repr__(self)})'
    
    def __getitem__(self, key):
        """Returns whether a specific flag of the given name is enableds."""
        return (self>>self.__keys__[key])&1
    
    def keys(self):
        """
        Yields the name of the byte vize flags, which are enabled.
        
        Yields
        ------
        name : `str`
        """
        for name, shift in self.__keys__.items():
            if (self>>shift)&1:
                yield name
    
    __iter__ = keys
    
    def values(self):
        """
        Yields the shift values of the flags, under which shift value the flag is enabled.
        
        Yields
        -------
        shift : `int`
        """
        for shift in self.__keys__.values():
            if (self>>shift)&1:
                yield shift
    
    def items(self):
        """
        Yields the items of the flag.
        
        Yields
        -------
        name : `str`
            The name of the specific flag
        enabled : `int` (`0` or `1`)
            Whether the specific byte vize value is enabled.
        """
        for name, shift in self.__keys__.items():
            yield name, (self>>shift)&1
    
    def __contains__(self, key):
        """Returns whether the specific flag of the given name is enabled."""
        try:
            position = self.__keys__[key]
        except KeyError:
            return 0
        
        return (self>>position)&1
    
    def is_subset(self, other):
        """Returns whether self has the same amount or more flags disabled than other."""
        return (self&other) == self
    
    def is_superset(self, other):
        """Returns whether self has the same amount or more flags enabled than other."""
        return (self|other) == self
    
    def is_strict_subset(self, other):
        """Returns whether self has more flags disabled than other."""
        return self != other and (self&other) == self
    
    def is_strict_superset(self, other):
        """Returns whether self has more flags enabled than other."""
        return self != other and (self|other) == self
    
    __ge__ = is_superset
    __gt__ = is_strict_superset
    __lt__ = is_strict_subset
    __le__ = is_subset
    
    def update_by_keys(self, **kwargs):
        """
        Updates the source value with the given flags and returns a new one.
        
        Parameters
        ----------
        **kwargs : Keyword arguments
            `flag-name` - `bool` relations.
        
        Returns
        -------
        flag : ``FlagBase`` instance
        
        Examples
        -------
        ```
        >>> from hata import Permission
        >>> perm = Permission().update_by_keys(kick_users=True, ban_users=True)
        >>> list(perm)
        ['kick_users', 'ban_users']
        >>> perm = perm.update_by_keys(manage_roles=True, kick_users=False)
        >>> list(perm)
        ['ban_users', 'manage_roles']
        ```
        """
        new = self
        for key, value in kwargs.items():
            try:
                shift = self.__keys__[key]
            except KeyError as err:
                err.args = (f'Invalid key: {key!r}.',)
                raise
            
            if value:
                new |= (1<<shift)
            else:
                if (new>>shift)&1:
                    new ^= (1<<shift)
        
        return int.__new__(type(self), new)

class ReverseFlagBase(FlagBase, baseclass=True):
    """
    Base class for reversed byte vize flags.
    
    Class attributes
    ----------------
    __getter_class__ : ``ReverseFlagGetDescriptor``
        Flag value getter descriptor for subclasses.
    __enabler_class__ : ``FlagDisableDescriptor``
        Flag enabler descriptor for subclasses.
    __disabler_class__ : ``FlagEnableDescriptor``
        Flag disabler descriptor for subclasses.
    """
    __getter_class__ = ReverseFlagGetDescriptor
    __enabler_class__ = FlagDisableDescriptor
    __disabler_class__ = FlagEnableDescriptor
    
    def __getitem__(self, key):
        """Returns whether a specific flag of the given name is enableds."""
        return ((self>>self.__keys__[key])&1)^1
    
    def keys(self):
        """
        Yields the name of the byte vize flags, which are enabled.
        
        Yields
        ------
        name : `str`
        """
        for name, shift in self.__keys__.items():
            if ((self>>shift)&1)^1:
                yield name
    
    __iter__ = keys
    
    def values(self):
        """
        Yields the shift values of the flags, under which shift value the flag is enabled.
        
        Yields
        -------
        shift : `int`
        """
        for shift in self.__keys__.values():
            if ((self>>shift)&1)^1:
                yield shift
    
    def items(self):
        """
        Yields the items of the flag.
        
        Yields
        -------
        name : `str`
            The name of the specific flag
        enabled : `int` (`0` or `1`)
            Whether the specific byte vize value is enabled.
        """
        for name, shift in self.__keys__.items():
            yield name, ((self>>shift)&1)^1
    
    def __contains__(self, key):
        """Returns whether the specific flag of the given name is enabled."""
        try:
            position = self.__keys__[key]
        except KeyError:
            return 0
        
        return ((self>>position)&1)^1
    
    def is_subset(self, other):
        """Returns whether self has the same amount or more flags disabled than other."""
        return (self|other) == self
    
    def is_superset(self, other):
        """Returns whether self has the same amount or more flags enabled than other."""
        return (self&other) == self
    
    def is_strict_subset(self, other):
        """Returns whether self has more flags disabled than other."""
        return self != other and (self|other) == self
    
    def is_strict_superset(self, other):
        """Returns whether self has more flags enabled than other."""
        return self != other and (self&other) == self
    
    __ge__ = is_superset
    __gt__ = is_strict_superset
    __lt__ = is_strict_subset
    __le__ = is_subset
    
    def update_by_keys(self, **kwargs):
        """
        Updates the source value with the given flags and returns a new one.
        
        Parameters
        ----------
        **kwargs : Keyword arguments
            `flag-name` - `bool` relations.
        
        Returns
        -------
        flag : ``ReverseFlagBase`` instance
        
        Examples
        --------
        ```
        >>> from hata import SystemChannelFlag
        >>> flags = SystemChannelFlag()
        >>> list(flags)
        ['welcome', 'boost']
        >>> flags = flags.update_by_keys(boost=False)
        >>> list(flags)
        ['welcome']
        ```
        """
        new = self
        for key, value in kwargs.items():
            try:
                shift = self.__keys__[key]
            except KeyError as err:
                err.args = (f'Invalid key:{key!r}.',)
                raise
            
            if value:
                if (new>>shift)&1:
                    new ^= (1<<shift)
            else:
                new |= (1<<shift)
        
        return int.__new__(type(self), new)

class IconType(object):
    """
    Represents a Discord icon's type.
    
    Attributes
    ----------
    name : `str`
        The name of the icon type.
    value : `int`
        The identificator value the icon type.
        
    Class Attributes
    ----------------
    Every predefind icon type can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | name          | value |
    +=======================+===============+=======+
    | NONE                  | NONE          | 0     |
    +-----------------------+---------------+-------+
    | STATIC                | STATIC        | 1     |
    +-----------------------+---------------+-------+
    | ANIMATED              | ANIMATED      | 2     |
    +-----------------------+---------------+-------+
    """
    __slots__ = ('name', 'value', )
    
    def __init__(self, name, value):
        """
        Creates a new icon type with the given name and value.
        
        Parameters
        ----------
        name : `str`
            The icon type's name.
        value : `int`
            The icon type's identificator value.
        """
        self.name = name
        self.value = value
    
    def __str__(self):
        """Returns the name of the avatar type."""
        return self.name
    
    def __int__(self):
        """Returns the identificator value of the icon type."""
        return self.value
    
    def __bool__(self):
        """Returns whether the icon's type is set."""
        if self.value:
            boolean = True
        else:
            boolean = False
        
        return boolean
    
    def __repr__(self):
        """Returns the icon type's representation."""
        return f'{self.__class__.__name__}(name={self.name!r}, value={self.value!r})'
    
    def __hash__(self):
        """Returns the icon type's hash, what equals to it's value."""
        return self.value
    
    def __gt__(self, other):
        """Returns whether this icon type's value is greater than the other's."""
        if type(self) is type(other):
            return self.value > other.value
        
        return NotImplemented
    
    def __ge__(self, other):
        """Returns whether this icon type's value is greater or equal to the other's."""
        if type(self) is type(other):
            return self.value >= other.value
        
        return NotImplemented
    
    def __eq__(self, other):
        """Returns whether this icon type's value is equal to the other's."""
        if type(self) is type(other):
            return self.value == other.value
        
        return NotImplemented
    
    def __ne__(self, other):
        """Returns whether this icon type's value is not equal to the other's."""
        if type(self) is type(other):
            return self.value != other.value
        
        return NotImplemented
    
    def __le__(self, other):
        """Returns whether this icon type's value is less or equal to the other's."""
        if type(self) is type(other):
            return self.value <= other.value
        
        return NotImplemented
    
    def __lt__(self, other):
        """Returns whether this icon type's value is less than the other's."""
        if type(self) is type(other):
            return self.value < other.value
        
        return NotImplemented
    
    NONE = NotImplemented
    STATIC = NotImplemented
    ANIMATED = NotImplemented

IconType.NONE     = ICON_TYPE_NONE     = IconType('NONE'    , 0)
IconType.STATIC   = ICON_TYPE_STATIC   = IconType('STATIC'  , 1)
IconType.ANIMATED = ICON_TYPE_ANIMATED = IconType('ANIMATED', 2)

class Icon(object):
    """
    Represents a Discord Icon.
    
    Attributes
    ----------
    hash : `int`
        The icon's hash value.
    type : ``IconType``
        The icon's type.
    """
    __slots__ = ('type', 'hash',)
    
    def __init__(self, icon_type, icon_hash):
        """
        Creates a new ``Icon`` object with the given attributes.
        
        Parameters
        ----------
        icon_type : ``IconType``
            The icon's type.
        icon_hash : `int`
            The icon's hash value.
        """
        self.type = icon_type
        self.hash = icon_hash
        
    @property
    def as_base16_hash(self):
        """
        Returns the discord side representtaion of the icon.
        
        Returns
        -------
        icon : `str` or `None`
        """
        icon_type = self.type
        if icon_type is ICON_TYPE_NONE:
            icon = None
        else:
            icon = self.hash.__format__('0>32x')
            if icon_type is ICON_TYPE_ANIMATED:
                icon = 'a_'+icon
        
        return icon
    
    hash_info_width = sys.hash_info.width
    if hash_info_width == 32:
        def __hash__(self):
            """Returns the icon's hash."""
            icon_type = self.type
            if icon_type is ICON_TYPE_NONE:
                hash_value = 0
            else:
                icon_hash = self.hash
                hash_value = (icon_hash>>96)^((icon_hash>>64)&((1<<32)-1))^((icon_hash>>32)&((1<<32)-1))^(icon_hash&((1<<32)-1))
                if icon_type is ICON_TYPE_ANIMATED:
                    hash_value ^= ((1<<32)-1)
            
            return hash_value
    
    elif hash_info_width == 64:
        def __hash__(self):
            """Returns the icon's hash."""
            icon_type = self.type
            if icon_type is ICON_TYPE_NONE:
                hash_value = 0
            else:
                icon_hash = self.hash
                hash_value = (icon_hash>>64)^(icon_hash&((1<<64)-1))
                if icon_type is ICON_TYPE_ANIMATED:
                    hash_value ^= ((1<<64)-1)
            return hash_value
    
    else:
        def __hash__(self):
            """Returns the icon's hash."""
            icon_type = self.type
            if icon_type is ICON_TYPE_NONE:
                hash_value = 0
            else:
                hash_value = self.hash
                if icon_type is ICON_TYPE_ANIMATED:
                    hash_value ^= ((1<<128)-1)
            
            return hash_value
    
    del hash_info_width
    
    def __eq__(self, other):
        """Returns whether the two icons are equal."""
        if (type(self) is not type(other)):
            return NotImplemented
        
        icon_type = self.type
        if (icon_type is not other.type):
            return False
        
        if icon_type is ICON_TYPE_NONE:
            return True
        
        if self.hash == other.hash:
            return True
        
        return False
    
    def __repr__(self):
        """Returns the represnetation of the icon."""
        return f'{self.__class__.__name__}(icon_type=ICON_TYPE_{self.type.name}, icon_hash={self.hash})'
    
    def __iter__(self):
        """Unpacks the icon."""
        yield self.type
        yield self.hash
    
    def __len__(self):
        """Lenght hinter (for unpacking if needed)."""
        return 2
    
    def __bool__(self):
        return (self.type is not ICON_TYPE_NONE)
    
    @classmethod
    def from_base16_hash(cls, icon):
        """
        Converts a discord icon hash value to an ``Icon`` object.
        
        Parameters
        ----------
        icon : `None` or `str`
        
        Returns
        -------
        self : ``Icon``
        """
        if icon is None:
            icon_type = ICON_TYPE_NONE
            icon_hash = 0
        else:
            if icon.startswith('a_'):
                icon = icon[2:]
                icon_type = ICON_TYPE_ANIMATED
            else:
                icon_type = ICON_TYPE_STATIC
            icon_hash = int(icon, 16)
        
        self = object.__new__(cls)
        self.type = icon_type
        self.hash = icon_hash
        return self


class IconSlot(object):
    """
    Interal icon slotter to represent an icon of a discord entitiy.
    
    Attributes
    ----------
    internal_name : `str`
        The internal name of the icon.
    discord_side_name : `str`
        The discord side name of the icon.
    added_instance_atttributes : `tuple` of `str`
        The added instance attribute's name by the icon slot.
    added_class_attributes : `list` of `tuple` (`str`, `Any`)
        The added class attributes by the icon slot.
    
    Class Attributes
    ----------------
    _compile_globals : `dict` of (`str`, `Any`)
        Compile time globals for the generated functions.
    """
    __slots__ = ('internal_name', 'discord_side_name', 'added_instance_atttributes', 'added_class_attributes')
    
    _compile_globals = {
        'ICON_TYPE_NONE'     : ICON_TYPE_NONE     ,
        'ICON_TYPE_STATIC'   : ICON_TYPE_STATIC   ,
        'ICON_TYPE_ANIMATED' : ICON_TYPE_ANIMATED ,
        'Icon'               : Icon               ,
            }
    
    def __new__(cls, internal_name, discord_side_name, url_property, url_as_method, add_updater=True):
        """
        Creates an ``IconSlot`` with the given parameters.
        
        Parameters
        ----------
        internal_name : `str`
            The internal name of the icon.
        discord_side_name : `str`
            The discord side name of the icon.
        url_property : `function`
            A function what will be used as a property when accessing the icon' url.
        url_as_method : `function`
            A function what will be used a method when creating a formatted icon url.
        add_updater : `bool`, Optional
            Whether the icon slot should add updater methods to the class. Defaults to `True`.
        
        Returns
        -------
        self : ``IconSlot``
        """
        added_instance_atttribute_name_hash = internal_name+'_hash'
        added_internal_attribute_name_type  = internal_name+'_type'
        
        added_class_attributes = []
        if (url_property is not None):
            added_class_attributes.append((f'{internal_name}_url', property(url_property)))
        
        if (url_as_method is not None):
            added_class_attributes.append((f'{internal_name}_url_as', url_as_method))
        
        locals_ = {}
        func_name = f'_set_{internal_name}'
        exec(compile((
            f'def {func_name}(self, data):\n'
            f'    icon = data.get({discord_side_name!r})\n'
            f''
            f'    if icon is None:\n'
            f'        icon_type = ICON_TYPE_NONE\n'
            f'        icon_hash = 0\n'
            f'    else:\n'
            f'        if icon.startswith(\'a_\'):\n'
            f'            icon = icon[2:]\n'
            f'            icon_type = ICON_TYPE_ANIMATED\n'
            f'        else:\n'
            f'            icon_type = ICON_TYPE_STATIC\n'
            f'        icon_hash = int(icon, 16)\n'
            f''
            f'    self.{added_internal_attribute_name_type} = icon_type\n'
            f'    self.{added_instance_atttribute_name_hash} = icon_hash\n'
                ), f'<{cls.__name__}>', 'exec', optimize=2), cls._compile_globals, locals_)
        
        added_class_attributes.append((func_name, locals_[func_name]),)
        
        if add_updater:
            locals_ = {}
            func_name = f'_update_{internal_name}'
            exec(compile((
                f'def {func_name}(self, data, old_attributes):\n'
                f'    icon = data.get({discord_side_name!r})\n'
                f''
                f'    if icon is None:\n'
                f'        icon_type = ICON_TYPE_NONE\n'
                f'        icon_hash = 0\n'
                f'    else:\n'
                f'        if icon.startswith(\'a_\'):\n'
                f'            icon = icon[2:]\n'
                f'            icon_type = ICON_TYPE_ANIMATED\n'
                f'        else:\n'
                f'            icon_type = ICON_TYPE_STATIC\n'
                f'        icon_hash = int(icon, 16)\n'
                f''
                f'    self_icon_type = self.{added_internal_attribute_name_type}\n'
                f'    self_icon_hash = self.{added_instance_atttribute_name_hash}\n'
                f'    if (self_icon_type is not icon_type) or (self_icon_hash != icon_hash):\n'
                f'        old_attributes[{internal_name!r}] = Icon(self_icon_type, self_icon_hash)\n'
                f'        self.{added_internal_attribute_name_type} = icon_type\n'
                f'        self.{added_instance_atttribute_name_hash} = icon_hash\n'
                    ), f'<{cls.__name__}>', 'exec', optimize=2), cls._compile_globals, locals_)
            
            added_class_attributes.append((func_name, locals_[func_name]),)
        
        self = object.__new__(cls)
        self.internal_name = internal_name
        self.discord_side_name = discord_side_name
        self.added_instance_atttributes = (added_internal_attribute_name_type, added_instance_atttribute_name_hash)
        self.added_class_attributes = added_class_attributes
        return self
    
    def __set_slot__(self, attribute_name, class_attributes, class_slots):
        """Applies the changes of the icon slot on the classe's attributes."""
        
        # Extend the slots of the class
        class_slots.update(self.added_instance_atttributes)
        
        # Add the extra class attributes to the class
        for name, value in self.added_class_attributes:
            class_attributes[name] = value
    
    def __get__(self, obj, objtype=None):
        """Returns self if called from class, meanwhile an Icon if called from an object."""
        if obj is None:
            return self
        
        icon_type_name, icon_hash_name = self.added_instance_atttributes
        icon_type = getattr(obj, icon_type_name)
        icon_hash = getattr(obj, icon_hash_name)
        return Icon(icon_type, icon_hash)
    
    def __set__(self, obj, value):
        """Can't set attribute."""
        raise AttributeError('can\'t set attribute')
    
    def __delete__(self, obj):
        """Can't delete attribute."""
        raise AttributeError('can\'t delete attribute')
    
    def preconvert(self, kwargs, processable):
        """
        Used at proconverters to parse out from the passed kwargs the icon of the entitiy.
        
        Parameters
        ----------
        kwargs : `dict` of (`str`, `Any`) items
            Keyword arguments passed to the respective preconverter.
        processable : `list` of `tuple` (`str`, `Any`)
            A list of instance attributes which will be set when all the passed kwargs are validated.
        
        Raises
        ------
        TypeError
            If any of expected value's type is invalid.
        ValueError
            If any of the expected value's type is valid, but it's value is not.
        """
        icon_type_name, icon_hash_name = self.added_instance_atttributes
        try:
            icon = kwargs.pop(self.internal_name)
        except KeyError:
            try:
                icon_hash = kwargs.pop(icon_hash_name)
            except KeyError:
                return
            
            if type(icon_hash) is int:
                pass
            elif isinstance(icon_hash, int):
                icon_hash = int(icon_hash)
            else:
                raise TypeError(f'`{icon_hash_name}` can be passed as `int` instance, got '
                    f'{icon_hash.__class__.__name__}.')
            
            if icon_hash<0 or icon_hash>((1<<128)-1):
                raise ValueError(f'`{icon_hash_name}` cannot be negative or longer than 128 bits, got {icon_hash}.')
            
            try:
                icon_type = kwargs.pop(icon_type_name)
            except KeyError:
                if icon_hash == 0:
                    icon_type = ICON_TYPE_NONE
                else:
                    icon_type = ICON_TYPE_STATIC
            else:
                if (type(icon_type) is not IconType):
                    raise TypeError(f'`{icon_type_name}` can be passed as `{IconType.__name__}` instance, got '
                        f'{icon_type.__class__.__name__}.')
            
                if (icon_type is ICON_TYPE_NONE) and icon_hash:
                    raise ValueError(f'If `{icon_type_name}` is passed as `ICON_TYPE_NONE`, then `{icon_hash_name}` '
                        f'can be passed only as `0`, meanwhile got `{icon_hash}`.')
            
        else:
            if icon is None:
                icon_type = ICON_TYPE_NONE
                icon_hash = 0
            elif type(icon) is Icon:
                icon_type = icon.type
                icon_hash = icon.hash
            elif isinstance(icon, str):
                if icon.startswith('a_'):
                    icon = icon[2:]
                    icon_type = ICON_TYPE_ANIMATED
                else:
                    icon_type = ICON_TYPE_STATIC
                icon_hash = int(icon, 16)
            else:
                raise TypeError(f'`{self.internal_name!r}` can be passed as `None`, `{Icon.__name__}` or as `str` '
                    f'instance, got {icon.__class__.__name__}.')
        
        processable[icon_type_name] = icon_type
        processable[icon_hash_name] = icon_hash

def instance_or_id_to_instance(obj, type_, name):
    """
    Converts the given `obj` to it's `type_` representation.
    
    Parameters
    ----------
    obj : `int`, `str` or`type_` instance
        The object to convert.
    type_ : `type` or (`tuple` of `type`)
        The type to convert.
    name : `str`
        The respective name of the object.
    
    Returns
    -------
    instance : `type_`
    
    Raises
    ------
    TypeError
        If `obj` was not given neither as `type_`, `str` or `int` instance.
    ValueError
        If `obj` was given as `str` or as `int` instance, but not as a valid snowflake, so `type_` cannot be precreated
        with it.
    
    Notes
    -----
    The given `type_` must have a `.precreate` function`.
    """
    obj_type = obj.__class__
    if issubclass(obj_type, type_):
        instance = obj
    else:
        if obj_type is int:
            snowflake = obj
        elif issubclass(obj_type, str):
            if 6<len(obj)<18 and obj.isdigit():
                snowflake = int(obj)
            else:
                raise ValueError(f'`{name}` was given as `str` instance, but not as a valid snowflake, got {obj!r}.')
        
        elif issubclass(obj_type, int):
            snowflake = int(obj)
        else:
            if type(type_) is tuple:
                type_name = ', '.join(t.__name__ for t in type_)
            else:
                type_name = type_.__name__
            
            raise TypeError(f'`{name}` can be given either as {type_name} instance, or as `int` or `str` representing '
                f'a snowflake, got {obj_type.__name__}.')
        
        if snowflake < 0 or snowflake>((1<<64)-1):
            raise ValueError(f'`{name}` was given either as `int` or as `str` instance, but not as represneting a '
                f'`uint64`, got {obj!r}.')
        
        if type(type_) is tuple:
            type_ = type_[0]
        
        instance = type_.precreate(snowflake)
    
    return instance

def instance_or_id_to_snowflake(obj, type_, name):
    """
    Validates the given `obj` whether it is instance of the given `type_`, or is a valid snowflake representation.
    
    Parameters
    ----------
    obj : `int`, `str` or`type_` instance
        The object to validate.
    type_ : `type` of (`tuple` of `type`)
        Expected type.
    name : `str`
        The respective name of the object.
    
    Returns
    -------
    snowflake : `int`
    
    Raises
    ------
    TypeError
        If `obj` was not given neither as `type_`, `str` or `int` instance.
    ValueError
        If `obj` was given as `str` or as `int` instance, but not as a valid snowflake.
    
    Notes
    -----
    The given `type_`'s instances must have a `.id` attribute.
    """
    obj_type = obj.__class__
    if issubclass(obj_type, type_):
        snowflake = obj.id
    else:
        if obj_type is int:
            snowflake = obj
        elif issubclass(obj_type, str):
            if 6<len(obj)<18 and obj.isdigit():
                snowflake = int(obj)
            else:
                raise ValueError(f'`{name}` was given as `str` instance, but not as a valid snowflake, got {obj!r}.')
        
        elif issubclass(obj_type, int):
            snowflake = int(obj)
        else:
            if type(type_) is tuple:
                type_name = ', '.join(t.__name__ for t in type_)
            else:
                type_name = type_.__name__
            
            raise TypeError(f'`{name}` can be given either as {type_name} instance, or as `int` or `str` representing '
                f'a snowflake, got {obj_type.__name__}.')
        
        if snowflake < 0 or snowflake>((1<<64)-1):
            raise ValueError(f'`{name}` was given either as `int` or as `str` instance, but not as represneting a '
                f'`uint64`, got {obj!r}.')
    
    return snowflake

del sys

# -*- coding: utf-8 -*-
from ..backend.dereaddons_local import _spaceholder
from .others import id_to_time

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
        The creates instances are always slotted.
        
        When more classes are inherited then use `__slots` at the secondary classes for adding additional member
        descriptors.
        """
        final_slots = set()
        
        parent_count = len(class_parents)
        if parent_count > 0:
            parent = class_parents[0]
            final_slots.update(getattr(parent,'__slots__',()))
            
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
                final_slots.update(getattr(parent,f'_{parent.__name__}__slots',()))
                index +=1
        
        final_slots.update(class_attributes.get('__slots__',()))
        
        if immortal:
            for parent in class_parents:
                if hasattr(parent,'__weakref__'):
                    break
            else:
                final_slots.add('__weakref__')
        
        class_attributes['__slots__'] = tuple(sorted(final_slots))
        
        return type.__new__(cls, class_name, class_parents, class_attributes)

class DiscordEntity(object, metaclass = DiscordEntityMeta):
    """
    Base class for Discord entities.
    
    Attributes
    ----------
    id : `int`
        The entity's unique identificator number.
    
    Notes
    -----
    Inherit it with passing `immortal = True` to make the subclass weakreferable.
    """
    __slots__ = ('id', )
    
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
        return int.__new__(type(instance),(instance|(1<<self.shift)))

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
            return int.__new__(type(instance),(instance^(1<<shift)))
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
    def __new__(cls, class_name, class_parents, class_attributes, access_keyword=None, enable_keyword=None, disable_keyword=None,
            baseclass=False):
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
            if (not class_parents) or (not issubclass(class_parents[0],int)):
                raise TypeError(f'`{class_name}` is not derived directly from `int`.')
            
            class_keys = class_attributes.get('__keys__',_spaceholder)
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
                raise TypeError(f'`__keys__`\'s keys should be `str` instances, meanwhile got at least 1 non `str`: {name!r}.')
            
            if (type(shift) is not int):
                raise TypeError(f'`__keys__`\'s values should be `int` instances, meanwhile got at least 1 non `int`: {shift!r}.')
            
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
        return f'{self.__class__.__name__}({self!s})'
    
    def __getitem__(self,key):
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
            position=self.__keys__[key]
        except KeyError:
            return 0
        
        return (self>>position)&1
    
    def is_subset(self, other):
        """Returns whether self has the same amount or more flags disabled than other."""
        return (self&other)==self
    
    def is_superset(self, other):
        """Returns whether self has the same amount or more flags enabled than other."""
        return (self|other)==self
    
    def is_strict_subset(self, other):
        """Returns whether self has more flags disabled than other."""
        return self!=other and (self&other)==self
    
    def is_strict_superset(self, other):
        """Returns whether self has more flags enabled than other."""
        return self!=other and (self|other)==self
    
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
        >>> from hata import Permission
        >>> perm = Permission().update_by_keys(kick_users=True, ban_users=True)
        >>> list(perm)
        ['kick_users', 'ban_users']
        >>> perm = perm.update_by_keys(manage_roles=True, kick_users=False)
        >>> list(perm)
        ['ban_users', 'manage_roles']
        """
        new=self
        for key, value in kwargs.items():
            try:
                shift=self.__keys__[key]
            except KeyError as err:
                err.args=(f'Invalid key: {key!r}.',)
                raise
            
            if value:
                new|=(1<<shift)
            else:
                if (new>>shift)&1:
                    new^=(1<<shift)
        
        return int.__new__(type(self),new)

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
    
    def __contains__(self,key):
        """Returns whether the specific flag of the given name is enabled."""
        try:
            position=self.__keys__[key]
        except KeyError:
            return 0
        
        return ((self>>position)&1)^1
    
    def is_subset(self,other):
        """Returns whether self has the same amount or more flags disabled than other."""
        return (self|other)==self
    
    def is_superset(self,other):
        """Returns whether self has the same amount or more flags enabled than other."""
        return (self&other)==self
    
    def is_strict_subset(self,other):
        """Returns whether self has more flags disabled than other."""
        return self!=other and (self|other)==self
    
    def is_strict_superset(self,other):
        """Returns whether self has more flags enabled than other."""
        return self!=other and (self&other)==self
    
    __ge__ = is_superset
    __gt__ = is_strict_superset
    __lt__ = is_strict_subset
    __le__ = is_subset
    
    def update_by_keys(self,**kwargs):
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
        >>> from hata import SystemChannelFlag
        >>> flags = SystemChannelFlag()
        >>> list(flags)
        ['welcome', 'boost']
        >>> flags = flags.update_by_keys(boost=False)
        >>> list(flags)
        ['welcome']
        """
        new=self
        for key, value in kwargs.items():
            try:
                shift=self.__keys__[key]
            except KeyError as err:
                err.args=(f'Invalid key:{key!r}.',)
                raise
            
            if value:
                if (new>>shift)&1:
                    new^=(1<<shift)
            else:
                new|=(1<<shift)
        
        return int.__new__(type(self),new)

__all__ = ('FlagBase', 'ReverseFlagBase', )

class FlagGetDescriptor:
    """
    Returns the flag descriptor's owner's value at a specific bitwise position.
    
    Attributes
    ----------
    shift : `int`
        The bitwise position of the attribute what this flag represents.
    """
    __slots__ = ('shift', )
    def __init__(self, shift):
        self.shift = shift
    
    def __get__(self, instance, type_):
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
    Returns the flag descriptor's owner's reversed value at a specific bitwise position.
    
    This type is a reversed version of ``FlagGetDescriptor``, so it returns `0` when the value has `1` at the specific
    bitwise position.
    
    Attributes
    ----------
    shift : `int`
        The bitwise position of the attribute, what this flag represents.
    """
    def __get__(self, instance, type_):
        if instance is None:
            return self
        else:
            return ((instance>>self.shift)&1)^1
    
    def __call__(self, value):
        return ((value>>self.shift)&1)^1


class FlagEnabler:
    """
    Enables a specific bitwise flag of a given value by returning a new one with the given bitwise flag enabled.
    
    This type is instanced by ``FlagEnableDescriptor`` objects, when they are accessed as instance attribute.
    
    Attributes
    ----------
    instance : ``FlagMeta`` instance's instance
        The source value, what will be modified.
    shift : `int`
        The bitwise position, what will be modified.
    
    Notes
    -----
    This type is used for disabling specific bitwise values when the source flag is a reversed flag.
    """
    __slots__ = ('instance', 'shift')
    
    def __call__(self):
        instance = self.instance
        return int.__new__(type(instance), (instance|(1<<self.shift)))


class FlagEnableDescriptor(FlagGetDescriptor):
    """
    Descriptor for enabling a specific bitwise value of a flag. After this descriptor is accessed as an instance
    attribute, a ``FlagEnabler`` is returned, and calling that will return a new instance with it's bitwise flag
    value enabled.
    
    Attributes
    ----------
    shift : `int`
        The bitwise position of the attribute what this flag represents.
    
    Notes
    -----
    This type is used for disabling specific bitwise values when the source flag is a reversed flag.
    """
    def __get__(self, instance, type_):
        if instance is None:
            return self
        else:
            result = FlagEnabler()
            result.instance = instance
            result.shift = self.shift
            return result


class FlagDisabler:
    """
    Disables a specific bitwise flag of a given value by returning a new one with the given bitwise flag disabled.
    
    This type is instanced by ``FlagDisableDescriptor`` objects, when they are accessed as instance attribute.
    
    Attributes
    ----------
    instance : ``FlagMeta`` instance's instance
        The source value, what will be modified.
    shift : `int`
        The bitwise position, what will be modified.
    
    Notes
    -----
    This type is used for enable specific bitwise values when the source flag is a reversed flag.
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
    Descriptor for disabling a specific bitwise value of a flag. After this descriptor is accessed as an instance
    attribute, a ``FlagDisabler`` is returned, and calling that will return a new instance with it's bitwise flag
    value disabled.
    
    Attributes
    ----------
    shift : `int`
        The bitwise position of the attribute what this flag represents.
    
    Notes
    -----
    This type is used for enabling specific bitwise values when the source flag is a reversed flag.
    """
    def __get__(self, instance, type_):
        if instance is None:
            return self
        else:
            result = FlagDisabler()
            result.instance = instance
            result.shift = self.shift
            return result


class FlagMeta(type):
    """
    Metaclass for bitwise flags.
    """
    def __new__(cls, class_name, class_parents, class_attributes, access_keyword=None, enable_keyword=None,
            disable_keyword=None, base_class=False):
        """
        Creates a bitwise flag type.
        
        Parameters
        ----------
        class_name : `str`
            The created class's name.
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
        base_class : `bool`, Optional
            Whether the created type is a base class for flags. If it is:
                - Should directly derived from `int`.
                - Should not implement `__keys__` (except `NotImplemented`).
                - Should implement `__getter_class__` class attribute.
                - Should implement `__enabler_class__` class attribute.
                - Should implement `__disabler_class__` class attribute.
            If not, then:
                - Should derive directly from a ``FlagMeta`` base_class.
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
        if base_class:
            if (not class_parents) or (not issubclass(class_parents[0], int)):
                raise TypeError(f'`{class_name}` is not derived directly from `int`.')
            
            class_keys = class_attributes.get('__keys__', ...)
            if class_keys is NotImplemented:
                pass
            elif class_keys is ...:
                class_attributes['__keys__'] = NotImplemented
            else:
                raise TypeError(f'`{class_name}` has `__keys__` defined and not as `NotImplemented`.')
            
            for attribute_name in ('__getter_class__', '__enabler_class__', '__disabler_class__'):
                if attribute_name not in class_attributes:
                    raise TypeError(f'`{class_name}` should implement a `{attribute_name}`.')
            
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


class FlagBase(int, metaclass = FlagMeta, base_class=True):
    """
    Base class for bitwise flags.
    
    Class Attributes
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
        """Returns the representation of the flag."""
        return f'{self.__class__.__name__}({int.__repr__(self)})'
    
    def __getitem__(self, key):
        """Returns whether a specific flag of the given name is enabled."""
        return (self>>self.__keys__[key])&1
    
    def keys(self):
        """
        Yields the name of the bitwise flags, which are enabled.
        
        This method is a generator.
        
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
        
        This method is a generator.
        
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
        
        This method is a generator.
        
        Yields
        ------
        name : `str`
            The name of the specific flag
        enabled : `int` (`0` or `1`)
            Whether the specific bitwise value is enabled.
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
        **kwargs : Keyword parameters
            `flag-name` - `bool` relations.
        
        Returns
        -------
        flag : ``FlagBase`` instance
        
        Raises
        ------
        LookupError
            If a keyword is invalid.
        
        Examples
        -------
        ```py
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
            except KeyError:
                raise LookupError(f'Invalid key: {key!r}.') from None
            
            if value:
                new |= (1<<shift)
            else:
                if (new>>shift)&1:
                    new ^= (1<<shift)
        
        return int.__new__(type(self), new)

class ReverseFlagBase(FlagBase, base_class=True):
    """
    Base class for reversed bitwise flags.
    
    Class Attributes
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
        """Returns whether a specific flag of the given name is enabled."""
        return ((self>>self.__keys__[key])&1)^1
    
    def keys(self):
        """
        Yields the name of the bitwise flags, which are enabled.
        
        This method is a generator.
        
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
        
        This method is a generator.
        
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
        
        This method is a generator.
        
        Yields
        -------
        name : `str`
            The name of the specific flag
        enabled : `int` (`0` or `1`)
            Whether the specific bitwise value is enabled.
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
        **kwargs : Keyword parameters
            `flag-name` - `bool` relations.
        
        Returns
        -------
        flag : ``ReverseFlagBase`` instance
        
        Examples
        --------
        ```py
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

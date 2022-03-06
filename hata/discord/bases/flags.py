__all__ = ('FlagBase', 'ReverseFlagBase', )


def create_flag_getter(name, shift):
    """
    Creates a flag getter function.
    
    Parameters
    ----------
    name : `str`
        The flag's name.
    shift : `int`
        Bit shift value.
    
    Returns
    -------
    flag_getter : `FunctionType`
    """
    locals_ = {}
    func_name = f'_get_{name}'
    exec(compile((
        f'def {func_name}(self):\n'
        f'    return (self >> 0x{shift:x}) & 1'
    ), f'<create_flag_getter>', 'exec', optimize=2), {}, locals_)
    
    return locals_[func_name]


def create_reversed_flag_getter(name, shift):
    """
    Creates a reversed flag getter function.
    
    Parameters
    ----------
    name : `str`
        The flag's name.
    shift : `int`
        Bit shift value.
    
    Returns
    -------
    reversed_flag_getter : `FunctionType`
    """
    locals_ = {}
    func_name = f'_get_{name}'
    exec(compile((
        f'def {func_name}(self):\n'
        f'    return ((self >> 0x{shift:x}) & 1) ^ 1'
    ), f'<create_reversed_flag_getter>', 'exec', optimize=2), {}, locals_)
    
    return locals_[func_name]


def create_flag_enabler(name, shift):
    """
    Creates a flag enabler function.
    
    Parameters
    ----------
    name : `str`
        The flag's name.
    shift : `int`
        Bit shift value.
    
    Returns
    -------
    flag_enabler : `FunctionType`
    """
    locals_ = {}
    func_name = f'_enable_{name}'
    exec(compile((
        f'def {func_name}(self):\n'
        f'    return int.__new__(type(self), (self | (1 << 0x{shift:x})))'
    ), f'<create_flag_enabler>', 'exec', optimize=2), {}, locals_)
    
    return locals_[func_name]


def create_flag_disabler(name, shift):
    """
    Creates a flag disabler function.
    
    Parameters
    ----------
    name : `str`
        The flag's name.
    shift : `int`
        Bit shift value.
    
    Returns
    -------
    flag_disabler : `FunctionType`
    """
    locals_ = {}
    func_name = f'_disable_{name}'
    exec(compile((
        f'def {func_name}(self):\n'
        f'    if (self >> 0x{shift:x}) & 1:\n'
        f'        return int.__new__(type(self), (self ^ (1 << 0x{shift:x})))\n'
        f'    else:\n'
        f'        return self'
    ), f'<create_flag_enabler>', 'exec', optimize=2), {}, locals_)
    
    return locals_[func_name]


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
        class_parents : `tuple` of `type`
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
                - Should implement `__getter_factory__` class attribute.
                - Should implement `__enabler_factory__` class attribute.
                - Should implement `__disabler_factory__` class attribute.
            If not, then:
                - Should derive directly from a ``FlagMeta`` base_class.
                - Should implement `__keys__` as `dict` of (`str`, `int`) items, where the values are not less than
                    `0`, and not greater than `63` either.
        
        Returns
        -------
        type : ``FlagMeta``
        
        Raises
        ------
        TypeError
            When any requirements are not satisfied.
        """
        if base_class:
            if (not class_parents) or (not issubclass(class_parents[0], int)):
                raise TypeError(
                    f'`{class_name}` is not derived directly from `int`.'
                )
            
            class_keys = class_attributes.get('__keys__', ...)
            if class_keys is NotImplemented:
                pass
            elif class_keys is ...:
                class_attributes['__keys__'] = NotImplemented
            else:
                raise TypeError(
                    f'`{class_name}` has `__keys__` defined and not as `NotImplemented`.'
                )
            
            for attribute_name in ('__getter_factory__', '__enabler_factory__', '__disabler_factory__'):
                if attribute_name not in class_attributes:
                    raise TypeError(
                        f'`{class_name}` should implement a `{attribute_name}`.'
                    )
            
            # do not care about the leftover
            
            return type.__new__(cls, class_name, class_parents, class_attributes)
        
        # Python has no GOTO, so lets insert one
        while True:
            if class_parents:
                parent = class_parents[0]
                if (type(parent) is FlagMeta) and parent.__keys__ is NotImplemented:
                    break
            
            raise TypeError(
                f'`{class_name}` is not derived directly from a `{cls.__name__}` base instance.'
            )
        
        # Validate keys
        try:
            keys = class_attributes['__keys__']
        except KeyError:
            raise TypeError(
                f'`{class_name}` did not define `__keys__` attribute.'
            ) from None
        
        if (type(keys) is not dict):
            raise TypeError(
                f'`__keys__` defined as non `dict`: `{keys.__class__.__name__}`.'
            )
        
        for name, shift in keys.items():
            if not isinstance(name, str):
                raise TypeError(
                    f'`__keys__`\'s keys should be `str`-s, meanwhile got at least 1 non `str`: '
                    f'{name.__class__.__name__}; {name!r}.'
                )
            
            if not isinstance(shift, int):
                raise TypeError(
                    f'`__keys__`\'s values should be `int`-s, meanwhile got at least 1 non `int`: '
                    f'{shift.__class__.__name__}; {shift!r}.'
                )
            
            if shift < 0 or shift > 63:
                raise TypeError(
                    f'`__keys__`\' values must be between 0 and 63, got: {shift!r}'
                )
        
        class_attributes.setdefault('__new__', int.__new__)
        
        getter = parent.__getter_factory__
        enabler = parent.__enabler_factory__
        disabler = parent.__disabler_factory__
        
        # Add properties
        for name, shift in keys.items():
            if access_keyword is None:
                access_name = name
            else:
                access_name = f'{access_keyword}_{name}'
            
            class_attributes[access_name] = property(getter(name, shift))
            
            if (enable_keyword is not None):
                class_attributes[f'{enable_keyword}_{name}'] = enabler(name, shift)
            
            if (disable_keyword is not None):
                class_attributes[f'{disable_keyword}_{name}'] = disabler(name, shift)
        
        return type.__new__(cls, class_name, class_parents, class_attributes)


class FlagBase(int, metaclass=FlagMeta, base_class=True):
    """
    Base class for bitwise flags.
    
    Class Attributes
    ----------------
    __getter_factory__ : ``create_flag_getter``
        Flag value getter descriptor for subclasses.
    __enabler_factory__ : ``create_flag_enabler``
        Flag enabler function factory for subclasses.
    __disabler_factory__ : ``create_flag_disabler``
        Flag disabler function factory for subclasses.
    """
    __slots__ = ()
    __keys__ = NotImplemented
    
    __getter_factory__ = create_flag_getter
    __enabler_factory__ = create_flag_enabler
    __disabler_factory__ = create_flag_disabler
    
    def __new__(self, base=None):
        """You cannot subclass flag base classes."""
        raise NotImplementedError
    
    def __repr__(self):
        """Returns the representation of the flag."""
        return f'{self.__class__.__name__}({int.__repr__(self)})'
    
    def __getitem__(self, key):
        """Returns whether a specific flag of the given name is enabled."""
        return (self >> self.__keys__[key]) & 1
    
    def keys(self):
        """
        Yields the name of the bitwise flags, which are enabled.
        
        This method is a generator.
        
        Yields
        ------
        name : `str`
        """
        for name, shift in self.__keys__.items():
            if (self >> shift) & 1:
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
            if (self >> shift) & 1:
                yield shift
    
    def items(self):
        """
        Yields the items of the flag.
        
        This method is a generator.
        
        Yields
        ------
        name : `str`
            The name of the specific flag
        enabled : `int` (`0`, `1`)
            Whether the specific bitwise value is enabled.
        """
        for name, shift in self.__keys__.items():
            yield name, (self >> shift) & 1
    
    def __contains__(self, key):
        """Returns whether the specific flag of the given name is enabled."""
        try:
            position = self.__keys__[key]
        except KeyError:
            return 0
        
        return (self >> position) & 1
    
    def is_subset(self, other):
        """Returns whether self has the same amount or more flags disabled than other."""
        return (self & other) == self
    
    def is_superset(self, other):
        """Returns whether self has the same amount or more flags enabled than other."""
        return (self | other) == self
    
    def is_strict_subset(self, other):
        """Returns whether self has more flags disabled than other."""
        return self != other and (self & other) == self
    
    def is_strict_superset(self, other):
        """Returns whether self has more flags enabled than other."""
        return self != other and (self | other) == self
    
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
        flag : ``FlagBase``
        
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
                new |= (1 << shift)
            else:
                if (new >> shift) & 1:
                    new ^= (1 << shift)
        
        return int.__new__(type(self), new)


class ReverseFlagBase(FlagBase, base_class=True):
    """
    Base class for reversed bitwise flags.
    
    Class Attributes
    ----------------
    __getter_factory__ : ``create_reversed_flag_getter``
        Flag value getter descriptor for subclasses.
    __enabler_factory__ : ``create_flag_disabler``
        Flag enabler function factory for subclasses.
    __disabler_factory__ : ``create_flag_enabler``
        Flag disabler function factory for subclasses.
    """
    __getter_factory__ = create_reversed_flag_getter
    __enabler_factory__ = create_flag_disabler
    __disabler_factory__ = create_flag_enabler
    
    def __getitem__(self, key):
        """Returns whether a specific flag of the given name is enabled."""
        return ((self >> self.__keys__[key]) & 1)^1
    
    def keys(self):
        """
        Yields the name of the bitwise flags, which are enabled.
        
        This method is a generator.
        
        Yields
        ------
        name : `str`
        """
        for name, shift in self.__keys__.items():
            if ((self >> shift) & 1)^1:
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
            if ((self >> shift) & 1)^1:
                yield shift
    
    def items(self):
        """
        Yields the items of the flag.
        
        This method is a generator.
        
        Yields
        -------
        name : `str`
            The name of the specific flag
        enabled : `int` (`0`, `1`)
            Whether the specific bitwise value is enabled.
        """
        for name, shift in self.__keys__.items():
            yield name, ((self >> shift) & 1) ^ 1
    
    def __contains__(self, key):
        """Returns whether the specific flag of the given name is enabled."""
        try:
            position = self.__keys__[key]
        except KeyError:
            return 0
        
        return ((self >> position) & 1) ^ 1
    
    def is_subset(self, other):
        """Returns whether self has the same amount or more flags disabled than other."""
        return (self | other) == self
    
    def is_superset(self, other):
        """Returns whether self has the same amount or more flags enabled than other."""
        return (self & other) == self
    
    def is_strict_subset(self, other):
        """Returns whether self has more flags disabled than other."""
        return self != other and (self | other) == self
    
    def is_strict_superset(self, other):
        """Returns whether self has more flags enabled than other."""
        return self != other and (self & other) == self
    
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
        flag : ``ReverseFlagBase``
        
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
                if (new >> shift) & 1:
                    new ^= (1 << shift)
            else:
                new |= (1 << shift)
        
        return int.__new__(type(self), new)

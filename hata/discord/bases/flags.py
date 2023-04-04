__all__ = ('FlagBase', 'ReverseFlagBase', )

import warnings


def maybe_apply_deprecation(function, name, deprecation_info):
    """
    CApplies deprecation to the given getter / enabled / disabler function.
    
    Parameters
    ----------
    function : `FunctionType`
        The function to apply it to.
    name : `str`
        The flag's name.
    deprecation_info : `None`, `tuple` (`str`, `str`)
        Deprecation info for the field if deprecated.
    
    Returns
    -------
    function : `FunctionType`
    """
    if (deprecation_info is None):
        return function
    
    def deprecated_field(self):
        nonlocal deprecation_info
        nonlocal function
        nonlocal name
        
        warnings.warn(
            (
                f'{self.__class__.__name__}`\s {name} field is deprecated and will be removed in '
                f'{deprecation_info[0]}. Please use {deprecation_info[1]} instead.'
            ),
            FutureWarning,
            stacklevel = 3,
        )
        
        return function(self)
    
    return deprecated_field


def create_flag_getter(name, shift, deprecation_info):
    """
    Creates a flag getter function.
    
    Parameters
    ----------
    name : `str`
        The flag's name.
    shift : `int`
        Bit shift value.
    deprecation_info : `None`, `tuple` (`str`, `str`)
        Deprecation info for the field if deprecated.
    
    Returns
    -------
    flag_getter : `FunctionType`
    """
    def flag_getter(self):
        nonlocal shift
        return (self >> shift) & 1
    
    maybe_apply_deprecation(flag_getter, name, deprecation_info)
    function_name = f'_get_{name}'
    flag_getter.__name__ = function_name
    flag_getter.__qualname__ = function_name
    
    return flag_getter


def create_reversed_flag_getter(name, shift, deprecation_info):
    """
    Creates a reversed flag getter function.
    
    Parameters
    ----------
    name : `str`
        The flag's name.
    shift : `int`
        Bit shift value.
    deprecation_info : `None`, `tuple` (`str`, `str`)
        Deprecation info for the field if deprecated.
    
    Returns
    -------
    reversed_flag_getter : `FunctionType`
    """
    def flag_getter(self):
        nonlocal shift
        return ((self >> shift) & 1) ^ 1
    
    maybe_apply_deprecation(flag_getter, name, deprecation_info)
    function_name = f'_get_{name}'
    flag_getter.__name__ = function_name
    flag_getter.__qualname__ = function_name
    
    return flag_getter



def create_flag_enabler(name, shift, deprecation_info):
    """
    Creates a flag enabler function.
    
    Parameters
    ----------
    name : `str`
        The flag's name.
    shift : `int`
        Bit shift value.
    deprecation_info : `None`, `tuple` (`str`, `str`)
        Deprecation info for the field if deprecated.
    
    Returns
    -------
    flag_enabler : `FunctionType`
    """
    def flag_enabled(self):
        nonlocal shift
        return int.__new__(type(self), (self | (1 << shift)))
    
    maybe_apply_deprecation(flag_enabled, name, deprecation_info)
    function_name = f'_enable_{name}'
    flag_enabled.__name__ = function_name
    flag_enabled.__qualname__ = function_name
    
    return flag_enabled


def create_flag_disabler(name, shift, deprecation_info):
    """
    Creates a flag disabler function.
    
    Parameters
    ----------
    name : `str`
        The flag's name.
    shift : `int`
        Bit shift value.
    deprecation_info : `None`, `tuple` (`str`, `str`)
        Deprecation info for the field if deprecated.
    
    Returns
    -------
    flag_disabler : `FunctionType`
    """
    def flag_disabler(self):
        nonlocal shift
        if (self >> shift) & 1:
            return int.__new__(type(self), (self ^ (1 << shift)))
        
        return self
    
    maybe_apply_deprecation(flag_disabler, name, deprecation_info)
    function_name = f'_disable_{name}'
    flag_disabler.__name__ = function_name
    flag_disabler.__qualname__ = function_name
    
    return flag_disabler


def validate_shift(shift, keys_name, shift_name):
    """
    Validates a shift.
    
    shift : `int`
        The shift to validate.
    keys_name : `str`
        The name of the keys we are validating.
    shift_name : `str`
        The shift field's name.
    
    Raises
    ------
        - If `shift`'s type or value is not acceptable.
    """
    if not isinstance(shift, int):
        raise TypeError(
            f'`{keys_name}`\'s {shift_name}s should be `int`, got {shift.__class__.__name__}; {shift!r}.'
        )
    
    if shift < 0 or shift > 63:
        raise TypeError(
            f'`{keys_name}`\' {shift_name}s must be between 0 and 63, got: {shift!r}'
        )


def deprecated_value_validator(value, keys_name):
    """
    Deprecated value validator for key values.
    
    Parameters
    ----------
    value : `int`
        The value to validate.
    keys_name : `str`
        The name of the keys we are validating.
    
    Raises
    ------
        - If `value`'s type or structure is not acceptable.
    """
    if not isinstance(value, tuple) or (len(value) != 3):
        raise TypeError(
            f'`{keys_name}`\'s values can be `tuple` of length 3.'
        )
    
    shift, removed_at, use_instead = value
    validate_shift(shift, keys_name, 'shift')
    
    if not isinstance(removed_at, str):
        raise TypeError(
            f'`{keys_name}`\'s removed_at-s should be `str`, got {removed_at.__class__.__name__}; {removed_at!r}.'
        )
    
    if not isinstance(use_instead, str):
        raise TypeError(
            f'`{keys_name}`\'s use_instead-s should be `str`, got {removed_at.__class__.__name__}; {removed_at!r}.'
        )


def default_value_validator(value, keys_name):
    """
    Default validator for key values.
    
    Parameters
    ----------
    value : `int`
        The value to validate.
    keys_name : `str`
        The name of the keys we are validating.
    
    Raises
    ------
        - If `value`'s type or value is not acceptable.
    """
    validate_shift(value, keys_name, 'value')


def validate_keys(keys, keys_name, value_validator):
    """
    Validates the given flag keys.
    
    Parameters
    ----------
    keys : `dict` of (`str`, `int`) items
        Flag keys to validate.
    keys_name : `str`
        The name of the keys we are validating.
    value_validator : `FunctionType`
        Validates the item's value.
    
    Raises
    ------
        - If `keys`' type or structure is not acceptable.
    """
    if not isinstance(keys, dict):
        raise TypeError(
            f'`{keys_name}` defined as non `dict`: `{keys.__class__.__name__}`.'
        )
    
    for name, value in keys.items():
        if not isinstance(name, str):
            raise TypeError(
                f'`{keys_name}`\'s keys should be `str`-s, meanwhile got at least 1 non `str`: '
                f'{name.__class__.__name__}; {name!r}.'
            )
        
        value_validator(value, keys_name)


def iterate_keys(keys, deprecated_keys):
    """
    Iterates over the items of the given keys.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    keys : `dict` of (`str`, `int`) items
        Flag keys to iterate over.
    validate_keys : `NotImplemented`, `dict` of (`str`, `int`) items
        Deprecated flag keys to validate.
    
    Yields
    ------
    key : `str`
        Field key.
    shift : `int`
        Flag shift.
    deprecation_info : `None`, `tuple` (`str`, `str`)
        The deprecation info of the field.
    """
    for item in keys.items():
        yield (*item, None)
    
    if (deprecated_keys is not NotImplemented):
        for key, (shift, *deprecation_info) in deprecated_keys.items():
            yield key, shift, deprecation_info


class FlagMeta(type):
    """
    Metaclass for bitwise flags.
    """
    def __new__(
        cls,
        class_name,
        class_parents,
        class_attributes,
        access_keyword = None,
        enable_keyword = None,
        disable_keyword = None,
        base_class = False,
    ):
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
        
        validate_keys(keys, '__keys__', default_value_validator)
        
        deprecated_keys = class_attributes.get('__deprecated_keys__', NotImplemented)
        if (deprecated_keys is not NotImplemented):
            validate_keys(deprecated_keys, '__deprecated_keys__', deprecated_value_validator)
        
        class_attributes.setdefault('__new__', int.__new__)
        
        getter = parent.__getter_factory__
        enabler = parent.__enabler_factory__
        disabler = parent.__disabler_factory__
        
        # Add properties
        for name, shift, deprecation_info in iterate_keys(keys, deprecated_keys):
            if access_keyword is None:
                access_name = name
            else:
                access_name = f'{access_keyword}_{name}'
            
            class_attributes[access_name] = property(getter(name, shift, deprecation_info))
            
            if (enable_keyword is not None):
                class_attributes[f'{enable_keyword}_{name}'] = enabler(name, shift, deprecation_info)
            
            if (disable_keyword is not None):
                class_attributes[f'{disable_keyword}_{name}'] = disabler(name, shift, deprecation_info)
        
        return type.__new__(cls, class_name, class_parents, class_attributes)


class FlagBase(int, metaclass = FlagMeta, base_class = True):
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
    __deprecated_keys__ = NotImplemented
    
    __getter_factory__ = create_flag_getter
    __enabler_factory__ = create_flag_enabler
    __disabler_factory__ = create_flag_disabler
    
    def __new__(self, base = None):
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
    
    
    def _get_shift_of(self, key):
        """
        Gets the shift value for the given keys.
        
        Parameters
        ----------
        keys : `str`
            The key's name.
        
        Returns
        -------
        shift : `int`
        
        Raises
        ------
        LookupError
            - Invalid key given.
        """
        try:
            shift = self.__keys__[key]
        except KeyError:
            pass
        
        else:
            return shift
        
        deprecated_keys = self.__deprecated_keys__
        if (deprecated_keys is not NotImplemented):
            try:
                shift, removed_at, use_instead = deprecated_keys[key]
            except KeyError:
                pass
            else:
                warnings.warn(
                    (
                        f'`{self.__class__.__name__}`\'s {key} is deprecated and will be removed at {removed_at}. '
                        f'Please use {use_instead} instead.'
                    ),
                    FutureWarning,
                    stacklevel = 3,
                )
                
                return shift
        
        # support `_(\d+)` format
        if key.startswith('_'):
            try:
                shift = int(key[1:])
            except ValueError:
                pass
            else:
                return shift
        
        raise LookupError(f'Invalid key: {key!r}.')
    
    
    def update_by_keys(self, **keyword_parameters):
        """
        Updates the source value with the given flags and returns a new one.
        
        Parameters
        ----------
        **keyword_parameters : Keyword parameters
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
        >>> perm = Permission().update_by_keys(kick_users = True, ban_users = True)
        >>> list(perm)
        ['kick_users', 'ban_users']
        >>> perm = perm.update_by_keys(manage_roles = True, kick_users = False)
        >>> list(perm)
        ['ban_users', 'manage_roles']
        ```
        """
        new = self
        for key, value in keyword_parameters.items():
            shift = self._get_shift_of(key)
            
            if value:
                new |= (1 << shift)
            else:
                if (new >> shift) & 1:
                    new ^= (1 << shift)
        
        return int.__new__(type(self), new)


class ReverseFlagBase(FlagBase, base_class = True):
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
            if ((self >> shift) & 1) ^ 1:
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
    
    
    def update_by_keys(self, **keyword_parameters):
        """
        Updates the source value with the given flags and returns a new one.
        
        Parameters
        ----------
        **keyword_parameters : Keyword parameters
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
        for key, value in keyword_parameters.items():
            shift = self._get_shift_of(key)
            
            if value:
                if (new >> shift) & 1:
                    new ^= (1 << shift)
            else:
                new |= (1 << shift)
        
        return int.__new__(type(self), new)

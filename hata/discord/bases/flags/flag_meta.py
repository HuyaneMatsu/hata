__all__ = ()

from .flag_descriptors import (
    FlagBitDescriptor, FlagBitDescriptorDeprecated, FlagBitDescriptorReversed, FlagBitDescriptorReversedDeprecated,
    FlagDescriptor
)


NotImplementedType = type(NotImplemented)


def _ensure_int_in_type_parents(type_parents):
    """
    Ensures that parent 0 is `int` subclass.
    
    Parameters
    ----------
    type_parents : `tuple<type>`
        The type's parents to create.
    
    Returns
    -------
    type_parents : `tuple<type>`
    """
    if not type_parents:
        type_parents = (int,)
    elif not issubclass(type_parents[0], int):
        type_parents = (int, *type_parents)
    
    return type_parents


def _collect_shifts_from_type_parents(meta_type, type_parents, accumulated_shifts):
    """
    Collect the existing shifts from type parents.
    
    Parameters
    ----------
    meta_type : `type`
        The meta type to allow its children to be collected from.
    
    type_parents : `tuple<type>`
        The type's parents to create.
    
    accumulated_shifts : `set<(str, int, None | FlagDeprecation>)>`
        The accumulated shifts by their name.
    """
    for type_parent in type_parents:
        if isinstance(type_parent, meta_type):
            for name, shift in type_parent.__shifts__.items():
                accumulated_shifts.add((name, shift, None))
            
            for name, (shift, deprecation) in type_parent.__deprecated_shifts__.items():
                accumulated_shifts.add((name, shift, deprecation))


def _collect_shifts_from_type_attributes(
    type_attributes, accumulated_shifts, accumulated_flag_descriptors
):
    """
    Collects the new shifts from the type's new attributes.
    
    Parameters
    ----------
    type_attributes : `dict<str, object>`
        The type attributes of the created type.
    
    accumulated_shifts : `set<(str, int, None | FlagDeprecation)>`
        The accumulated shifts by their name.
    
    accumulated_flag_descriptors : `set<(str, FlagDescriptor)>`
        Flag descriptors.
    """
    for attribute_name, attribute_value in type_attributes.items():
        if isinstance(attribute_value, FlagDescriptor):
            accumulated_flag_descriptors.add((attribute_name, attribute_value))
            accumulated_shifts.add((attribute_name, attribute_value.shift, attribute_value.deprecation))


def _get_shift_name_overlap(accumulated_shifts):
    """
    Collects the keys that are duplicates.
    
    Parameters
    ----------
    accumulated_shifts : `set<(str, int, None | FlagDeprecation)>`
        The accumulated shifts by their name.
    
    Returns
    -------
    duplicates : `set<str>`
    """
    singles = set()
    duplicates = None
    
    # Get shifts by their name. And set them in a dictionary.
    for name, shift, deprecation in accumulated_shifts:
        if name not in singles:
            singles.add(name)
            continue
        
        # Add name to duplicates.
        if duplicates is None:
            duplicates = set()
        
        duplicates.add(name)
    
    return duplicates


def _filter_shifts_by_name(accumulated_shifts, duplicates):
    """
    Filters the shifts for the given names.
    
    Parameters
    ----------
    accumulated_shifts : `set<(str, int, None | FlagDeprecation)>`
        The accumulated shifts by their name.
    
    duplicates : `set<str>`
        Duplicated names.
    
    Returns
    -------
    shifts_by_name : `dict<str, set<int>>`
    """
    shifts_by_name = {name: set() for name in duplicates}
    
    for name, shift, deprecation in accumulated_shifts:
        try:
            shifts = shifts_by_name[name]
        except KeyError:
            continue
        
        shifts.add(shift)
    
    return shifts_by_name


def _build_duplicate_names_exception_message(shifts_by_name):
    """
    Builds exception message for the case when there are duplicate shifts for a single name.
    
    Parameters
    ----------
    shifts_by_name : `dict<str, set<int>>`
        The duplicate shifts under the same name.
    
    Returns
    -------
    exception_message : `str`
    """
    output_parts = []
    field_added = False
    
    for name, shifts in sorted(shifts_by_name.items()):
        if field_added:
            output_parts.append(' ')
        else:
            field_added = True
        
        output_parts.append('Name: `')
        output_parts.append(name)
        output_parts.append('` has duplicate shifts: ')
        
        shift_added = False
        for shift in sorted(shifts):
            if shift_added:
                output_parts.append(', ')
            else:
                shift_added = True
            
            output_parts.append(str(shift))
        
        output_parts.append('.')
    
    return ''.join(output_parts)


def _check_shifts_overlap(accumulated_shifts):
    """
    Raises an exception if there are duplicate shifts under the same name.
    
    Parameters
    ----------
    accumulated_shifts : `set<(str, int, None | FlagDeprecation)>`
        The accumulated shifts by their name.
    
    Raises
    ------
    ValueError
    """
    duplicates = _get_shift_name_overlap(accumulated_shifts)
    if duplicates is None:
        return
    
    raise ValueError(
        _build_duplicate_names_exception_message(_filter_shifts_by_name(accumulated_shifts, duplicates))
    )


def _collect_reverse_descriptors_from_type_parents(meta_type, type_parents, accumulated_reverse_descriptors):
    """
    Collects the `__reverse_descriptors__` fields from the given type parents.
    
    Parameters
    ----------
    meta_type : `type`
        The meta type to allow its children to be collected from.
    
    type_parents : `tuple<type>`
        The parent types of the type to create.
    
    accumulated_reverse_descriptors : `set<(str, int)>`
        Accumulated `__reverse_descriptors__` values.
    """
    for type_parent in type_parents:
        if isinstance(type_parent, meta_type):
            accumulated_reverse_descriptors.add((type_parent.__name__, type_parent.__reverse_descriptors__))


def _check_reverse_descriptors_type(type_name, value):
    """
    Checks whether `__reverse_descriptors__`'s type is acceptable.
    
    Parameters
    ----------
    type_name : `str`
        The type's name.
    
    value : `object`
        The value to check.
    
    Raises
    ------
    TypeError
    """
    if not isinstance(value, bool):
        raise TypeError(
            f'`{type_name}.__reverse_descriptors__` is not `bool`, got `{type(value).__name__}`; {value!r}.'
        )


def _is_reverse_descriptors_contradiction(accumulated_reverse_descriptors):
    """
    Returns whether there is a contradiction in `accumulated_reverse_descriptors` values.
    
    Parameters
    ----------
    accumulated_reverse_descriptors : `set<(str, bool)>`
        Accumulated `__reverse_descriptors__` values.
    
    Returns
    -------
    is_reverse_descriptors_contradiction : `bool`
    """
    iterator = iter(accumulated_reverse_descriptors)
    while True:
        item = next(iterator, None)
        
        # No more items left.
        if item is None:
            return False
        
        stated_value = item[1]
        # Ignore item if `-1`.
        if stated_value == -1:
            continue
        
        break
    
    for item in iterator:
        value = item[1]
        # Ignore item if `-1`.
        if value == -1:
            continue
        
        if value == stated_value:
            continue
        
        return True
    
    return False


def _build_reverse_descriptors_contradiction_exception_message(accumulated_reverse_descriptors):
    """
    Builds a `__reverse_descriptors__` contradiction error message.
    
    Parameters
    ----------
    accumulated_reverse_descriptors : `set<(str, bool)>`
        Accumulated `__reverse_descriptors__` values.
    
    Returns
    -------
    error_message : `str`
    """
    output_parts = ['There is contradiction in `__reverse_descriptors__` values: ']
    
    item_added = False
    
    for type_name, reverse_descriptors in sorted(accumulated_reverse_descriptors):
        if item_added:
            output_parts.append(', ')
        else:
            item_added = True
        
        output_parts.append(type_name)
        output_parts.append(' -> ')
        output_parts.append(repr(reverse_descriptors))
    
    output_parts.append('.')
    return ''.join(output_parts)


def _check_reverse_descriptors_contradiction(accumulated_reverse_descriptors):
    """
    Checks whether there is contradiction in `__reverse_descriptors__` values.
    
    Parameters
    ----------
    accumulated_reverse_descriptors : `set<(str, bool)>`
        Accumulated `__reverse_descriptors__` values.
    
    Raises
    ------
    ValueError
    """
    if _is_reverse_descriptors_contradiction(accumulated_reverse_descriptors):
        raise ValueError(_build_reverse_descriptors_contradiction_exception_message(accumulated_reverse_descriptors))


def _get_reverse_descriptors_value(accumulated_reverse_descriptors):
    """
    Gets what `__reverse_descriptors__` value should the created type use.
    
    Parameters
    ----------
    accumulated_reverse_descriptors : `set<(str, int)>`
        Accumulated `__reverse_descriptors__` values.
    
    Returns
    -------
    reverse_descriptors : `int`
    """
    if accumulated_reverse_descriptors:
        reverse_descriptors = next(iter(accumulated_reverse_descriptors))[1]
    else:
        reverse_descriptors = -1
    return reverse_descriptors


def _build_shifts(accumulated_shifts):
    """
    Builds a new `__shifts__` dictionary.
    
    Parameters
    ----------
    accumulated_shifts : `set<(str, int, None | FlagDeprecation)>`
        The accumulated shifts by their name.
    
    Returns
    -------
    shifts : `dict<str, int>`
    deprecated_shifts : `dict<str, (int, FlagDeprecation)>`
    """
    shifts = {}
    deprecated_shifts = {}
    
    for name, shift, deprecation in accumulated_shifts:
        if deprecation is None:
            shifts[name] = shift
        else:
            deprecated_shifts[name] = (shift, deprecation)
    
    return shifts, deprecated_shifts


def _build_flag_descriptors(type_name, reverse_descriptors, accumulated_flag_descriptors):
    """
    Builds flag descriptors.
    
    Parameters
    ----------
    type_name : `str`
        The created class's name.
    
    reverse_descriptors : `bool`
        Whether the descriptors should be reversed.
    
    accumulated_flag_descriptors : `set<(str, FlagDescriptor)>`
        Flag descriptors.
    
    Returns
    -------
    flag_descriptors : `list<FlagBitDescriptor>`
    """
    if reverse_descriptors:
        descriptor_type = FlagBitDescriptorReversed
        descriptor_type_deprecated = FlagBitDescriptorReversedDeprecated
    else:
        descriptor_type = FlagBitDescriptor
        descriptor_type_deprecated = FlagBitDescriptorDeprecated
        
    flag_descriptors = []
    
    for flag_name, flag_descriptor in accumulated_flag_descriptors:
        deprecation = flag_descriptor.deprecation
        shift = flag_descriptor.shift
        
        if deprecation is None:
            descriptor = descriptor_type(shift, type_name, flag_name)
        else:
            descriptor = descriptor_type_deprecated(shift, type_name, flag_name, deprecation)
        
        flag_descriptors.append(descriptor)
    
    return flag_descriptors


class FlagMeta(type):
    """
    Metatype for bit-flags.
    """
    def __new__(cls, type_name, type_parents, type_attributes, *, reverse_descriptors = ...):
        """
        Creates a new bitwise flag type.
        
        Parameters
        ----------
        type_name : `str`
            The created class's name.
        
        type_parents : `tuple<type>`
            The parent types of the type to create.
        
        type_attributes : `dict<str, object>`
            The type attributes of the created type.
        
        reverse_descriptors : `bool`, Optional (Keyword only)
            Whether 
        
        Returns
        -------
        type : `instance<cls>`
        
        Raises
        ------
        TypeError
            When any requirements are not satisfied.
        """
        type_parents = _ensure_int_in_type_parents(type_parents)
        
        # Assert if type not updated / incorrectly formed
        if __debug__:
            try:
                keys = type_attributes['__keys__']
            except KeyError:
                pass
            else:
                if isinstance(keys, (dict, NotImplementedType)):
                    raise AssertionError('Support for `__keys__` removed.')
        
        assert '__deprecated_keys__' not in type_attributes, 'Support for `__deprecated_keys__` removed.'
        
        # This should not be defined.
        assert '__shifts__' not in type_attributes, '`__shifts__` not allowed to be defined.'
        assert '__shifts_ordered__' not in type_attributes, '`__shifts_ordered__` not allowed to be defined.'
        assert '__deprecated_shifts__' not in type_attributes, '`__deprecated_shifts__` not allowed to be defined.'
        assert '__slots__' not in type_attributes, '`__slots__` not allowed to be defined.'
        
        # Accumulate shifts
        accumulated_shifts = set()
        accumulated_flag_descriptors = set()
        _collect_shifts_from_type_parents(cls, type_parents, accumulated_shifts)
        _collect_shifts_from_type_attributes(
            type_attributes, accumulated_shifts, accumulated_flag_descriptors
        )
        _check_shifts_overlap(accumulated_shifts)
        
        # check whether we reverse
        accumulated_reverse_descriptors = set()
        if (reverse_descriptors is ...):
            reverse_descriptors = -1
        else:
            _check_reverse_descriptors_type(type_name, reverse_descriptors)
            reverse_descriptors = 1 if reverse_descriptors else 0
        
        accumulated_reverse_descriptors.add((type_name, reverse_descriptors))
        
        _collect_reverse_descriptors_from_type_parents(cls, type_parents, accumulated_reverse_descriptors)
        _check_reverse_descriptors_contradiction(accumulated_reverse_descriptors)
        
        # Build new values
        reverse_descriptors = _get_reverse_descriptors_value(accumulated_reverse_descriptors)
        # allow -1 only if we have no descriptors.
        if (reverse_descriptors == -1) and accumulated_flag_descriptors:
            reverse_descriptors = 0
        
        shifts, deprecated_shifts = _build_shifts(accumulated_shifts)
        flag_descriptors = _build_flag_descriptors(type_name, reverse_descriptors, accumulated_flag_descriptors)
        shifts_ordered = sorted(shifts.items())
        
        # Populate attributes
        type_attributes['__reverse_descriptors__'] = reverse_descriptors
        type_attributes['__shifts__'] = shifts
        type_attributes['__shifts_ordered__'] = shifts_ordered
        type_attributes['__deprecated_shifts__'] = deprecated_shifts
        type_attributes.update((flag_descriptor.flag_name, flag_descriptor) for flag_descriptor in flag_descriptors)
        type_attributes['__slots__'] = ()
        
        return type.__new__(cls, type_name, type_parents, type_attributes)

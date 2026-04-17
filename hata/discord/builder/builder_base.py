__all__ = ()

from functools import partial as partial_func

from scarletio import RichAttributeErrorBaseType

from .conversion import ConversionMeta
from .descriptor import _conversion_descriptor_sort_key, ConversionDescriptor


def _request_type_attribute(type_name, base_types, type_attributes, attribute_name):
    """
    Allows requesting a constructed type's attribute before it was created.
    
    Parameters
    ----------
    type_name : `str`
        The to create type's name.
    base_types : `set<type>`
        Types to inherit from.
    type_attributes : `dict<str, object>`
            The type attributes of the type to be created.
    attribute_name : `str`
        The attribute's name.
    
    Returns
    -------
    attribute_value : `object`
    
    Raises
    ------
    RuntimeError
        - Missing attribute.
    """
    try:
        return type_attributes[attribute_name]
    except KeyError:
        pass
    
    for base_type in base_types:
        try:
            return getattr(base_type, attribute_name)
        except AttributeError:
            pass
    
    raise RuntimeError(
        f'{type_name!s} would not have requested attribute: {attribute_name!r}.'
    )


def _without_duplication(elements):
    """
    Returns a new list without duplication.
    
    Parameters
    ----------
    elements : `list`
        Elements to process.
    
    Returns
    -------
    output : `list`
    """
    output = []
    collected = set()
    old_length = 0
    
    for element in elements:
        collected.add(element)
        new_length = len(collected)
        if new_length == old_length:
            continue
        
        old_length = new_length
        output.append(element)
    
    return output


def _collect_meta_type_instances(meta_type, base_types):
    """
    Collects the types from the inherited ones.
    
    Parameters
    ----------
    meta_type : `type`
        Meta type to match.
    base_types : `tuple<type>`
        Types to filter from.
    
    Returns
    -------
    builder_types : `list<type>`
    """
    conversion_types = []
    
    for base_type in base_types:
        if isinstance(base_type, meta_type):
            conversion_types.append(base_type)

    return conversion_types


def _collect_assigned_conversions(builder_types, type_attributes):
    """
    Collects the assigned conversions.
    
    Parameters
    ----------
    builder_types : `list<type>`
        Inherited builder types to collect from.
    type_attributes : `dict<str, object>`
        The type attributes of the type to be created.
    
    Returns
    -------
    assigned_conversions : `dict<str, Conversion>`
    """
    assigned_conversions = {}
    for conversion_type in builder_types:
        # Remove anything that is already assigned
        to_remove = None
        for key in assigned_conversions.keys():
            if not hasattr(conversion_type, key):
                continue
            
            if to_remove is None:
                to_remove = []
            to_remove.append(key)
        
        if (to_remove is not None):
            for key in to_remove:
                del assigned_conversions[key]
        
        # Extend with new conversions 
        assigned_conversions.update(conversion_type.CONVERSIONS_ASSIGNED)
    
    # Remove from type attributes.
    to_remove = None
    for key in assigned_conversions.keys():
        if key not in type_attributes:
            continue
        
        if to_remove is None:
            to_remove = []
        to_remove.append(key)
    
    if (to_remove is not None):
        for key in to_remove:
            del assigned_conversions[key]
    
    # Extend with new conversions
    for attribute_name, attribute_value in type_attributes.items():
        if isinstance(type(attribute_value), ConversionMeta):
            assigned_conversions[attribute_name] = attribute_value
    
    return assigned_conversions


def _collect_default_conversions(builder_types, type_attributes):
    """
    Collects the default conversions.
    
    Parameters
    ----------
    builder_types : `list<type>`
        Inherited builder types to collect from.
    type_attributes : `dict<str, object>`
        The type attributes of the type to be created.
    
    Returns
    -------
    default_conversions : `list<Conversion>`
    """
    default_conversions = []
    
    for conversion_type in builder_types:
        added_conversions = getattr(conversion_type, 'CONVERSIONS_DEFAULT', None)
        if (added_conversions is not None):
            default_conversions.extend(added_conversions)
    
    added_conversions = type_attributes.pop('__conversions_default__', None)
    if (added_conversions is not None):
        default_conversions.extend(added_conversions)
    
    return _without_duplication(default_conversions)


def _create_conversion_descriptors(type_name, base_types, type_attributes, default_conversions, assigned_conversions):
    """
    Creates the conversion descriptors.
    
    Parameters
    ----------
    type_name : `str`
        The created type's name.
    base_types : `tuple<type>`
        The parent types.
    type_attributes : `dict<str, object>`
        The type attributes of the type to be created.
    default_conversions : `list<Conversion>`
        Default conversions to create descriptors for.
    assigned_conversions : `dict<str, Conversion>`
        Assigned descriptors to create descriptors for.
    
    Returns
    -------
    descriptors : `list<ConversionDescriptor>`
    """
    attribute_requester = partial_func(_request_type_attribute, type_name, base_types, type_attributes)
    descriptors = []
    
    for conversion in default_conversions:
        descriptor = ConversionDescriptor(None, conversion, attribute_requester)
        descriptors.append(descriptor)
    
    for attribute_name, conversion in assigned_conversions.items():
        descriptor = ConversionDescriptor(attribute_name, conversion, attribute_requester)
        type_attributes[attribute_name] = descriptor
        descriptors.append(descriptor)
    
    return descriptors


def _filter_descriptors_typed(conversion_descriptors):
    """
    Creates a type to descriptor relation for fast typed validation.
    
    Parameters
    ----------
    conversion_descriptors : `list<ConversionDescriptor>`
        Descriptors to filter from.
    
    Returns
    -------
    descriptors_typed : `dict<type, ConversionDescriptor>`
    descriptors_typed_ordered : `list<ConversionDescriptor>`
    """
    descriptors_typed_ordered = []
    for conversion_descriptor in conversion_descriptors:
        if conversion_descriptor.conversion.set_type is not None:
            descriptors_typed_ordered.append(conversion_descriptor)
    
    descriptors_typed_ordered.sort(key = _conversion_descriptor_sort_key)
    descriptors_typed = {
        conversion_descriptor.conversion.set_type: conversion_descriptor
        for conversion_descriptor in descriptors_typed_ordered
    }
    return descriptors_typed, descriptors_typed_ordered


def _filter_descriptors_positional(conversion_descriptors):
    """
    Creates the descriptor listing for positional parameter input validation.
    
    Parameters
    ----------
    conversion_descriptors : `list<ConversionDescriptor>`
        Descriptors to filter from.
    
    Returns
    -------
    descriptors_positional : `list<ConversionDescriptor>`
    """
    descriptors_positional = []
    for conversion_descriptor in conversion_descriptors:
        if conversion_descriptor.conversion.set_identifier is not None:
            descriptors_positional.append(conversion_descriptor)
    
    descriptors_positional.sort(key = _conversion_descriptor_sort_key)
    return descriptors_positional


def _filter_descriptors_listing(conversion_descriptors):
    """
    Creates the descriptor listing for listing parameter input validation.
    
    Parameters
    ----------
    conversion_descriptors : `list<ConversionDescriptor>`
        Descriptors to filter from.
    
    Returns
    -------
    descriptors_listing : `list<ConversionDescriptor>`
    """
    descriptors_listing = []
    for conversion_descriptor in conversion_descriptors:
        if conversion_descriptor.conversion.set_listing_identifier is not None:
            descriptors_listing.append(conversion_descriptor)
    
    descriptors_listing.sort(key = _conversion_descriptor_sort_key)
    return descriptors_listing


def _filter_descriptors_keyword(conversion_descriptors):
    """
    Creates a descriptor mapping for keyword parameter input validation.
    
    Parameters
    ----------
    conversion_descriptors : `list<ConversionDescriptor>`
        Descriptors to filter from.
    
    Returns
    -------
    descriptors_keyword : `dict<str, ConversionDescriptor>`
    """
    descriptors_keyword = {}
    for conversion_descriptor in conversion_descriptors:
        if conversion_descriptor.conversion.set_validator is not None:
            for name in conversion_descriptor.conversion.iter_names():
                descriptors_keyword[name] = conversion_descriptor
    
    return descriptors_keyword


class BuilderMeta(type):
    """
    Builder metatype.
    """
    def __new__(cls, type_name, base_types, type_attributes):
        """
        Creates a new builder type.
        
        Parameters
        ----------
        type_name : `str`
            The created type's name.
        base_types : `tuple<type>`
            The parent types.
        type_attributes : `dict<str, object>`
            The type attributes of the type to be created.
        """
        builder_types = _collect_meta_type_instances(cls, base_types)
        
        # Collect CONVERSIONS_DEFAULT
        default_conversions = _collect_default_conversions(builder_types, type_attributes)
        
        # Collect CONVERSIONS_ASSIGNED
        assigned_conversions = _collect_assigned_conversions(builder_types, type_attributes)
        
        # create conversion_descriptors
        conversion_descriptors = _create_conversion_descriptors(
            type_name, base_types, type_attributes, default_conversions, assigned_conversions
        )
        
        # filter DESCRIPTORS_POSITIONAL
        descriptors_positional = _filter_descriptors_positional(conversion_descriptors)
        
        # filter DESCRIPTORS_KEYWORD
        descriptors_keyword = _filter_descriptors_keyword(conversion_descriptors)
        
        # filter DESCRIPTORS_TYPED, DESCRIPTORS_TYPED_ORDERED
        descriptors_typed, descriptors_typed_ordered = _filter_descriptors_typed(conversion_descriptors)
        
        # filter DESCRIPTORS_LISTING
        descriptors_listing = _filter_descriptors_listing(conversion_descriptors)
        
        # set
        type_attributes['CONVERSIONS_ASSIGNED'] = assigned_conversions
        type_attributes['CONVERSIONS_DEFAULT'] = default_conversions
        type_attributes['DESCRIPTORS_POSITIONAL'] = descriptors_positional
        type_attributes['DESCRIPTORS_KEYWORD'] = descriptors_keyword
        type_attributes['DESCRIPTORS_TYPED'] = descriptors_typed
        type_attributes['DESCRIPTORS_TYPED_ORDERED'] = descriptors_typed_ordered
        type_attributes['DESCRIPTORS_LISTING'] = descriptors_listing
        
        # create type
        
        return type.__new__(cls, type_name, base_types, type_attributes)


class BuilderBase(RichAttributeErrorBaseType, metaclass = BuilderMeta):
    """
    Base builder defining default functionality.
    """
    __slots__ = ()
    
    __conversions_default__ = None
    
    def __new__(cls):
        """
        Creates a new message builder.
        """
        self = object.__new__(cls)
        return self
    
    
    def __eq__(self, other):
        """Returns whether the two builders are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        for conversion in {*self._iter_conversions(), *other._iter_conversions()}:
            if self._getter_field(conversion) != other._getter_field(conversion):
                return False
        
        return True
    
    
    def __hash__(self):
        """Returns the hash value of the builder."""
        hash_value = 0
        
        for conversion, value in self._iter_fields():
            if not value:
                continue
            
            hash_value ^= hash(conversion) & hash(value)
        
        return hash_value
    
    
    def __repr__(self):
        """Returns the builder's representation."""
        repr_parts = ['<', type(self).__name__]
        
        field_added = False
        
        for conversion, value in self._iter_fields():
            if not value:
                continue
            
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' ')
            repr_parts.append(conversion.name)
            repr_parts.append(' = ')
            repr_parts.append(repr(value))
            
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def _setter_none(self, conversion, value):
        """
        Sets nothing.
        
        Parameters
        ----------
        conversion : ``Conversion``
            Conversion we are setting.
        value : `object`
            The value to set.
        
        Returns
        -------
        field_set : `bool`
        """
        return True
    
    
    def _setter_field(self, conversion, value):
        """
        Sets the given field value.
        
        Parameters
        ----------
        conversion : ``Conversion``
            Conversion we are setting.
        value : `object`
            The value to set.
        
        Returns
        -------
        field_set : `bool`
        """
        set_merger = conversion.set_merger
        if (set_merger is not None):
            for old_value in self._try_pull_field_value(conversion):
                value = set_merger(old_value, value)
        
        self._store_field_value(conversion, value)
        return True
    
    
    def _store_field_value(self, conversion, value):
        """
        Stores the given field value.
        
        This method is method is an iterable generator.
        
        Parameters
        ----------
        conversion : ``Conversion``
            Conversion we are setting.
        value : `object`
            The value to set.    
        """
        raise NotImplemented
    
    
    def _try_pull_field_value(self, conversion):
        """
        Tries to get the field of the given conversion.
        
        This method is an iterable generator that should yield the matched `field` value once and not yield anything if
        not.
        
        Yields
        ------
        value : `object`
        """
        raise NotImplemented
        yield
    
    
    def _setter_positional(self, conversion, value):
        """
        Sets the given positional field values.
        
        Parameters
        ----------
        conversion : ``Conversion``
            Conversion we are setting.
        value : `object`
            The value to set.
        
        Returns
        -------
        field_set : `bool`
        """
        self._with_positional_parameters(value)
        return True
    
    
    def _setter_keyword(self, conversion, value):
        """
        Sets the given keyword field values.
        
        Parameters
        ----------
        conversion : ``Conversion``
            Conversion we are setting.
        value : `object`
            The value to set.
        
        Returns
        -------
        field_set : `bool`
        """
        self._with_keyword_parameters(value)
        return True
    
    
    def _setter_instance(self, conversion, value):
        """
        Sets the given builder instance's fields into self.
        
        Parameters
        ----------
        conversion : ``Conversion``
            Conversion we are setting.
        value : `instance<type<self>>`
            The value to set.
        
        Returns
        -------
        field_set : `bool`
        """
        for field_conversion, field_value in value._iter_fields():
            self._setter_field(field_conversion, field_value)
        return True
    
    
    def _with_positional_parameter_unknown(self, value):
        """
        Handles an unknown positional parameter adding. Called by ``._with_positional_parameters``.
        
        Parameters
        ----------
        value : `object`
            The value to add.
        
        Returns
        -------
        added : `bool`
        """
        return True
    
    
    def _try_match_as_typed(self, value):
        """
        Tries to match the given value based on type and then sets it.
        
        Parameters
        ----------
        value : `object`
            Value to match.
        
        Returns
        -------
        matched : `bool`
        """
        try:
            descriptor = self.DESCRIPTORS_TYPED[type(value)]
        except KeyError:
            return False
        
        set_type_processor = descriptor.conversion.set_type_processor
        if set_type_processor is None:
            processed_value = value
        else:
            processed_value = set_type_processor(value)
        
        descriptor.setter(self, descriptor.output_conversion, processed_value)
        return True
    
    
    def _try_match_as_listing(self, value):
        """
        Tries to match the given value if its a listing and then sets it.
        
        Parameters
        ----------
        value : `object`
            Value to match.
        
        Returns
        -------
        matched : `bool`
        """
        if not isinstance(value, list) or not value:
            return False
        
        for descriptor in self.DESCRIPTORS_LISTING:
            for processed_value in descriptor.conversion.set_listing_identifier(value):
                descriptor.setter(self, descriptor.output_conversion, processed_value)
                return True
        
        return False
    
    
    def _try_match_as_sub_type(self, value):
        """
        Tries to match the given value based on type and then sets it.
        Checks for inheritance and if matched updates the match table.
        
        Parameters
        ----------
        value : `object`
            Value to match.
        
        Returns
        -------
        matched : `bool`
        """
        value_type = type(value)
        for descriptor in self.DESCRIPTORS_TYPED_ORDERED:
            if issubclass(value_type, descriptor.conversion.set_type):
                self.DESCRIPTORS_TYPED[value_type] = descriptor
                break
        else:
            return False
                
        set_type_processor = descriptor.conversion.set_type_processor
        if set_type_processor is None:
            processed_value = value
        else:
            processed_value = set_type_processor(value)
        
        descriptor.setter(self, descriptor.output_conversion, processed_value)
        return True
    
    
    def _try_match_as_identified(self, value):
        """
        Tries to match the given value based on identifiers and then sets it.
        
        Parameters
        ----------
        value : `object`
            Value to match.
        
        Returns
        -------
        matched : `bool`
        """
        for descriptor in self.DESCRIPTORS_POSITIONAL:
            for processed_value in descriptor.conversion.set_identifier(value):
                descriptor.setter(self, descriptor.output_conversion, processed_value)
                return True
        
        return False
    
    
    def _with_positional_parameters(self, positional_parameters):
        """
        Extends the builder with the given positional parameters.
        
        Parameters
        ----------
        positional_parameters : `iterable<object>`
            Positional parameters to extend self with.
        
        Raises
        ------
        TypeError
            - Value of invalid type given.
            - Unrecognised value.
        """
        for value in positional_parameters:
            if self._try_match_as_typed(value):
                continue
            
            if self._try_match_as_listing(value):
                continue
            
            if self._try_match_as_sub_type(value):
                continue
            
            if self._try_match_as_identified(value):
                continue
            
            self._with_positional_parameter_unknown(value)
    
    
    def _with_keyword_parameter_unknown(self, key, value):
        """
        Handles an unknown keyword parameter adding. Called by ``._with_keyword_parameters``.
        
        Parameters
        ----------
        key : `str`
            They key to add for.
        
        value : `object`
            The value to add.
        
        Returns
        -------
        added : `bool`
        """
        return True
    
    
    def _with_keyword_parameters(self, keyword_parameters):
        """
        Extends the builder with the given keyword parameters.
        
        Parameters
        ----------
        keyword_parameters : `dict<str, object>`
            Keyword parameters to extend self with.
        
        Raises
        ------
        TypeError
            - Value of invalid type given.
            - Unrecognised value.
        """
        descriptors_keyword = self.DESCRIPTORS_KEYWORD
        
        for key, value in keyword_parameters.items():
            try:
                descriptor = descriptors_keyword[key]
            except KeyError:
                pass
            else:
                for processed_value in descriptor.conversion.set_validator(value):
                    descriptor.setter(self, descriptor.output_conversion, processed_value)
                    break
                
                else:
                    return descriptor.raise_type_error(key, value)
                
                continue
            
            self._with_keyword_parameter_unknown(key, value)
            continue
    
    
    def _getter_none(self, conversion):
        """
        Default value getter. Rejects getting.
        
        Parameters
        ----------
        conversion : ``Conversion``
            Conversion we are getting.
        
        Returns
        -------
        value : `object`
        
        Raises
        ------
        RuntimeError
            - Field is not gettable.
        """
        raise RuntimeError(
            f'Field {conversion.name} is not gettable.'
        )
    
    
    def _getter_field(self, conversion):
        """
        Gets the field value for the given conversion.
        
        Parameters
        ----------
        conversion : ``Conversion``
            Conversion to pull the value for.
        
        Returns
        -------
        field_value : `object`
        """
        for value in self._try_pull_field_value(conversion):
            break
        else:
            return conversion.get_default
        
        get_processor = conversion.get_processor
        if (get_processor is not None):
            value = get_processor(value)
        
        return value
    
    
    def _iter_conversions(self):
        """
        Iterates over the set conversions of the builder.
        
        This method is an iterable generator.
        
        Yields
        ------
        conversion : ``Conversion``
        """
        return
        yield
    
    
    def _iter_fields(self):
        """
        Iterates over the set fields of the builder.
        
        This method is an iterable generator.
        
        Yields
        ------
        conversion : ``Conversion``
        value : `object`
        """
        return
        yield
    

    def serialise(self, serialization_configuration):
        """
        Serialises the builder.
        
        Parameters
        ----------
        serialization_configuration : ``SerializationConfiguration``
            Configuration for serialization.
        
        Returns
        -------
        data : `dict<str, object> | FormData>`
        """
        data = {}
        defaults = serialization_configuration.defaults
        for conversion in serialization_configuration.conversions:
            for value in self._try_pull_field_value(conversion):
                data = conversion.serializer_putter(data, defaults, value)
        
        return data

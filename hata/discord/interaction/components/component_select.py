__all__ = ('ComponentSelect',)

import reprlib

from scarletio import copy_docs, include

from .component_base import ComponentBase
from .component_select_option import ComponentSelectOption
from .debug import (
    _debug_component_custom_id, _debug_component_enabled, _debug_component_max_values, _debug_component_min_values,
    _debug_component_options, _debug_component_placeholder
)
from .preinstanced import ComponentType


create_auto_custom_id = include('create_auto_custom_id')


class ComponentSelect(ComponentBase):
    """
    Select component.
    
    Attributes
    ----------
    custom_id : `str`
        Custom identifier to detect which component was used by the user.
    enabled : `bool`
        Whether the component is enabled.
    options : `None`, `tuple` of ``ComponentSelectOption``
        Options of the select.
    placeholder : `str`
        Placeholder text of the select.
    max_values : `int
        The maximal amount of options to select. Can be in range [1:25]. Defaults to `1`.
    min_values : `int`
        The minimal amount of options to select. Can be in range [1:15]. Defaults to `1`.
    
    Class Attributes
    ----------------
    type : ``ComponentType`` = `ComponentType.select`
        The component's type.
    """
    type = ComponentType.select
    
    __slots__ = ('custom_id', 'enabled', 'options', 'placeholder', 'max_values', 'min_values', )
    
    def __new__(cls, options, custom_id=None, *, enabled=True, placeholder=None, max_values=1, min_values=1):
        """
        Creates a new ``ComponentSelect`` with the given parameters.
        
        Parameters
        ----------
        options : `None` or (`list`, `tuple`) of ``ComponentSelectOption``
            Options of the select.
        custom_id : `None`, `str` = `None`, Optional
            Custom identifier to detect which component was used by the user.
        enabled : `bool` = `True`, Optional (Keyword only)
            Whether the button is enabled. Defaults to `True`.
        placeholder : `None`, `str` = `None`, Optional (Keyword only)
            Placeholder text of the select.
        max_values : `int` = `1`, Optional (Keyword only)
            The maximal amount of options to select. Can be in range [1:25].
        min_values : `int` = `1`, Optional (Keyword only)
            The minimal amount of options to select. Can be in range [1:15].
        
        Raises
        ------
        AssertionError
            - If `custom_id` is not given as `None`, `str`.
            - If `custom_id`'s length is out of range [0:100].
            - If `options` length is out from the expected range [1:25].
            - If `options` is neither `None` or (`list`, `tuple`) of ``ComponentSelectOption`` elements.
            - If `min_values` is not `int`.
            - If `min_values` is out of range [1:15].
            - If `max_values` is not `int`.
            - If `max_values` is out of range [1:25].
            - If `enabled` was not given as `bool`.
        """
        if __debug__:
            _debug_component_custom_id(custom_id)
            _debug_component_enabled(enabled)
            _debug_component_options(options)
            _debug_component_placeholder(placeholder)
            _debug_component_min_values(min_values)
            _debug_component_max_values(max_values)
        
        # custom_id
        if (custom_id is None) or (not custom_id):
            custom_id = create_auto_custom_id()
        
        # enabled
        # No additional checks
        
        # options
        if (options is not None):
            options = tuple(options)
            if (not options):
                options = None
        
        # placeholder
        if (placeholder is not None) and (not placeholder):
            placeholder = None
        
        # max_values
        # No additional checks
        
        # min_values
        # No additional checks
        
        self = object.__new__(cls)
        self.custom_id = custom_id
        self.enabled = enabled
        self.options = options
        self.placeholder = placeholder
        self.max_values = max_values
        self.min_values = min_values
        return self
    
    
    @classmethod
    @copy_docs(ComponentBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        
        # custom_id
        self.custom_id = data['custom_id']
        
        # enabled
        self.enabled = not data.get('disabled', False)
        
        # options
        option_datas = data['options']
        if option_datas:
            options = tuple(ComponentSelectOption.from_data(option_data) for option_data in option_datas)
        else:
            options = None
        self.options = options
        
        # placeholder
        placeholder = data.get('placeholder', None)
        if (placeholder is not None) and (not placeholder):
            placeholder = None
        self.placeholder = placeholder
        
        # max_values
        self.max_values = data.get('max_values', 1)
        
        # min_values
        self.min_values = data.get('min_values', 1)
        
        return self
    
    
    @copy_docs(ComponentBase.to_data)
    def to_data(self):
        # type & custom_id
        data = {
            'type': self.type.value,
            'custom_id': self.custom_id,
        }
        
        # enabled
        if (not self.enabled):
            data['disabled'] = True
        
        # options
        options = self.options
        if options is None:
            options_value = []
        else:
            options_value = [option.to_data() for option in options]
        data['options'] = options_value
        
        # placeholder
        placeholder = self.placeholder
        if (placeholder is not None):
            data['placeholder'] = placeholder
        
        # max_values
        max_values = self.max_values
        if max_values != 1:
            data['max_values'] = max_values
        
        # min_values
        min_values = self.min_values
        if min_values != 1:
            data['min_values'] = min_values
        
        return data
    
    
    @copy_docs(ComponentBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # Descriptive fields : type
        
        # type
        type_ = self.type
        repr_parts.append(' type=')
        repr_parts.append(type_.name)
        repr_parts.append(' (')
        repr_parts.append(repr(type_.value))
        repr_parts.append(')')
        
        # System fields : custom_id & options
        
        # custom_id
        repr_parts.append(', custom_id=')
        repr_parts.append(reprlib.repr(self.custom_id))
        
        # options
        repr_parts.append(', options=')
        options = self.options
        if (options is None):
            repr_parts.append('[]')
        else:
            repr_parts.append('[')
            
            index = 0
            limit = len(options)
            
            while True:
                option = options[index]
                index += 1
                
                repr_parts.append(repr(option))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        repr_parts.append('>')
        
        # Text fields : placeholder
        
        # placeholder
        placeholder = self.placeholder
        if (placeholder is not None):
            repr_parts.append(', placeholder=')
            repr_parts.append(repr(placeholder))
        
        # Optional descriptive fields: min_values & max_values & enabled
        
        # min_values
        min_values = self.min_values
        if min_values != 1:
            repr_parts.append(', min_values=')
            repr_parts.append(repr(min_values))
        
        # max_values
        max_values = self.max_values
        if max_values != 1:
            repr_parts.append(', max_values=')
            repr_parts.append(repr(max_values))
        
        # enabled
        enabled = self.enabled
        if (not enabled):
            repr_parts.append(', enabled=')
            repr_parts.append(repr(enabled))
        
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        # custom_id
        new.custom_id = self.custom_id
        
        # enabled
        new.enabled = self.enabled
        
        # options
        options = self.options
        if (options is not None):
            options = tuple(option.copy() for option in options)
        new.options = options
        
        # placeholder
        new.placeholder = self.placeholder
        
        # max_values
        new.max_values = self.max_values
        
        # min_values
        new.min_values = self.min_values
        
        return new
    
    
    def copy_with(self, **kwargs):
        """
        Copies the component and modifies the created one with the given parameters.
        
        Parameters
        ----------
        **kwargs : Keyword parameters
            Keyword parameters referencing attributes.
        
        Other Parameters
        ----------------
        custom_id : `None`, `str`, Optional (Keyword only)
            Custom identifier to detect which component was used by the user.
        
        enabled : `bool`, Optional (Keyword only)
            Whether the button is enabled. Defaults to `True`.
        
        options : `None` or (`list`, `tuple`) of ``ComponentSelectOption``, Optional (Keyword only)
            Options of the select.
        
        placeholder : `str`, Optional (Keyword only)
            Placeholder text of the select.
        
        max_values : `int`, Optional (Keyword only)
            The maximal amount of options to select. Can be in range [1:25]. Defaults to `1`.
        
        min_values : `int`, Optional (Keyword only)
            The minimal amount of options to select. Can be in range [1:15]. Defaults to `1`.
        
        Returns
        -------
        new : ``ComponentSelect``
        """
        # custom_id
        try:
            custom_id = kwargs.pop('custom_id')
        except KeyError:
            custom_id = self.custom_id
        else:
            if __debug__:
                _debug_component_custom_id(custom_id)
            
            if custom_id is None:
                custom_id = self.custom_id
        
        # enabled
        try:
            enabled = kwargs.pop('enabled')
        except KeyError:
            enabled = self.enabled
        else:
            if __debug__:
                _debug_component_enabled(enabled)
        
        # options
        try:
            options = kwargs.pop('options')
        except KeyError:
            options = self.options
            if (options is not None):
                options = tuple(option.copy() for option in options)
        else:
            if __debug__:
                _debug_component_options(options)
            
            if (options is not None):
                options = tuple(options)
                if (not options):
                    options = None
        
        # placeholder
        try:
            placeholder = kwargs.pop('placeholder')
        except KeyError:
            placeholder = self.placeholder
        else:
            if __debug__:
                _debug_component_placeholder(placeholder)
            
            if (placeholder is not None) and (not placeholder):
                placeholder = None
        
        # max_values
        try:
            max_values = kwargs.pop('max_values')
        except KeyError:
            max_values = self.max_values
        else:
            if __debug__:
                _debug_component_max_values(max_values)
        
        # min_values
        try:
            min_values = kwargs.pop('min_values')
        except KeyError:
            min_values = self.min_values
        else:
            if __debug__:
                _debug_component_min_values(min_values)
        
        if kwargs:
            raise TypeError(f'Unused or unsettable attributes: {kwargs!r}.')
        
        new = object.__new__(type(self))
        new.custom_id = custom_id
        new.enabled = enabled
        new.options = options
        new.placeholder = placeholder
        new.max_values = max_values
        new.min_values = min_values
        return new
    
    
    @copy_docs(ComponentBase.__eq__)
    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented
        
        # custom_id
        if self.custom_id != other.custom_id:
            return False
        
        # enabled
        if self.enabled != other.enabled:
            return False
        
        # options
        if self.options != other.options:
            return False
        
        # placeholder
        if self.placeholder != other.placeholder:
            return False
        
        # max_values
        if self.max_values != other.max_values:
            return False
        
        # min_values
        if self.min_values != other.min_values:
            return False
        
        return True
    
    
    @copy_docs(ComponentBase.__hash__)
    def __hash__(self):
        hash_value = self.type.value
        
        # custom_id
        hash_value ^= hash(self.custom_id)
        
        # enabled
        if self.enabled:
            hash_value ^= 1 << 8
        
        # options
        options = self.options
        if (options is not None):
            hash_value ^= len(options) << 12
            for option in options:
                hash_value ^= hash(option)
        
        # placeholder
        placeholder = self.placeholder
        if (placeholder is not None):
            hash_value ^= hash(placeholder)
        
        # max_values
        max_values = self.max_values
        if (max_values != 1):
            hash_value ^= (max_values << 18)
        
        # min_values
        min_values = self.min_values
        if (min_values != 1):
            min_values ^= (min_values << 22)
        
        return hash_value
    
    
    @copy_docs(ComponentBase._iter_components)
    def _iter_components(self):
        yield self
        
        options = self.options
        if (options is not None):
            for option in options:
                yield from option._iter_components()
    
    
    @copy_docs(ComponentBase._replace_direct_sub_components)
    def _replace_direct_sub_components(self, relation):
        options = self.options
        if (options is not None):
            self.options = tuple(relation.get(option, option) for option in options)
    
    
    @copy_docs(ComponentBase._iter_direct_sub_components)
    def _iter_direct_sub_components(self):
        options = self.options
        if (options is not None):
            yield from options

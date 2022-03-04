__all__ = ('FormSubmitInteraction', 'FormSubmitInteractionOption',)

import reprlib

from scarletio import copy_docs

from ..components import ComponentType

from .interaction_field_base import InteractionFieldBase


class FormSubmitInteraction(InteractionFieldBase):
    """
    Represents a response to a ``InteractionForm``.
    
    Attributes
    ----------
    custom_id : `None`, `str`
        The forms's custom identifier.
    options : `None`, `tuple` of ``FormSubmitInteractionOption``
        Submitted component values.
    """
    __slots__ = ('custom_id', 'options', )
    
    @copy_docs(InteractionFieldBase.__new__)
    def __new__(cls, data, interaction_event):
        # custom_id
        custom_id = data.get('custom_id', None)
        if (custom_id is not None) and (not custom_id):
            custom_id = None
        
        # options
        option_datas = data.get('components', None)
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = tuple(FormSubmitInteractionOption(option_data) for option_data in option_datas)
        
        
        self = object.__new__(cls)
        
        self.custom_id = custom_id
        self.options = options
        
        return self


    @copy_docs(InteractionFieldBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__,]
        
        repr_parts.append(' custom_id=')
        repr_parts.append(reprlib.repr(self.custom_id))
        
        options = self.options
        if (options is not None):
            repr_parts.append(', options=[')
            
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
        return ''.join(repr_parts)
    
    
    @copy_docs(InteractionFieldBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            hash_value ^= hash(custom_id)
        
        # options
        options = self.options
        if (options is not None):
            hash_value ^= (len(options) << 8)
            
            for option in options:
                hash_value ^= hash(option)
            
        return hash_value
    
    
    @copy_docs(InteractionFieldBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # custom_id
        if self.custom_id != other.custom_id:
            return False
        
        # options
        if self.options != other.options:
            return False
        
        return True
    
    
    def iter_custom_ids_and_values(self):
        """
        Iterates over all the `custom_id`-s and values of the form submit interaction.
        
        This method is an iterable generator.
        
        Yields
        ------
        custom_id : `str`
            The `custom_id` of a represented component.
        value : `str`
            The `value` passed by the user.
        """
        options = self.options
        if (options is not None):
            for option in options:
                yield from option.iter_custom_ids_and_values()
    
    
    def get_custom_id_value_relation(self):
        """
        Returns a dictionary with `custom_id` to `value` relation.
        
        Returns
        -------
        custom_id_value_relation : `dict` of (`str`, `str`) items
        """
        custom_id_value_relation = {}
        
        for custom_id, value in self.iter_custom_ids_and_values():
            if (value is not None):
                custom_id_value_relation[custom_id] = value
        
        return custom_id_value_relation
    
    
    def get_value_for(self, custom_id_to_match):
        """
        Returns the value for the given `custom_id`.
        
        Parameters
        ----------
        custom_id_to_match : `str`
            A respective components `custom_id` to match.
        
        Returns
        -------
        value : `None`, `str`
            The value if any.
        """
        for custom_id, value in self.iter_custom_ids_and_values():
            if (custom_id == custom_id_to_match):
                return value
    
    
    def get_match_and_value(self, matcher):
        """
        Gets a `custom_id`'s value matching the given `matcher`.
        
        Parameters
        ----------
        matcher : `callable`
            Matcher to call on a `custom_id`
            
            Should accept the following parameters:
            
            +-----------+-----------+
            | Name      | Type      |
            +===========+===========+
            | custom_id | `str`     |
            +-----------+-----------+
            
            Should return non-`None` on success.
        
        Returns
        -------
        match : `None`, `Any`
            The returned value by the ``matcher``
        value : `None`, `str`
            The matched `custom_id`'s value.
        """
        for custom_id, value in self.iter_custom_ids_and_values():
            match = matcher(custom_id)
            if (match is not None):
                return match, value
        
        return None, None
    
    
    def iter_matches_and_values(self, matcher):
        """
        Gets a `custom_id`'s value matching the given `matcher`.
        
        This method is an iterable generator.
        
        Parameters
        ----------
        matcher : `callable`
            Matcher to call on a `custom_id`
            
            Should accept the following parameters:
            
            +-----------+-----------+
            | Name      | Type      |
            +===========+===========+
            | custom_id | `str`     |
            +-----------+-----------+
            
            Should return non-`None` on success.
        
        Yields
        -------
        match : `None`, `Any`
            The returned value by the ``matcher``
        value : `None`, `str`
            The matched `custom_id`'s value.
        """
        for custom_id, value in self.iter_custom_ids_and_values():
            match = matcher(custom_id)
            if (match is not None):
                yield match, value


class FormSubmitInteractionOption:
    """
    Attributes
    ----------
    custom_id : `None`, `str`
        The option's respective component's type.
        
    options : `None`, `tuple` of ``FormSubmitInteractionOption``
        Mutually exclusive with the `value` field.
    
    type : ``ComponentType``
        The option respective component's type.
        
    value : `None`, `str`
        Mutually exclusive with the `options` field.
    """
    __slots__ = ('custom_id', 'options', 'type', 'value')
    
    def __new__(cls, data):
        """
        Creates a new ``FormSubmitInteractionOption`` from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            The received form submit interaction option data.
        """
        # custom_id
        custom_id = data.get('custom_id', None)
        if (custom_id is not None) and (not custom_id):
            custom_id = None
        
        # options
        option_datas = data.get('components', None)
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = tuple(FormSubmitInteractionOption(option_data) for option_data in option_datas)
        
        # type
        type_ = ComponentType.get(data.get('type', 0))
        
        # value
        value = data.get('value', None)
        if (value is not None) and (not value):
            value = None
        
        self = object.__new__(cls)
        
        self.custom_id = custom_id
        self.options = options
        self.type = type_
        self.value = value
        
        return self
        
    def __repr__(self):
        """Returns the application command interaction option's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # Descriptive fields : type
        
        # type
        type_ = self.type
        if type_ is not ComponentType.none:
            repr_parts.append(' type=')
            repr_parts.append(type_.name)
            repr_parts.append(' (')
            repr_parts.append(repr(type_.value))
            repr_parts.append(')')
            
            field_added = True
        
        else:
            field_added = False
        
        # System fields : custom_id
        
        # custom_id
        
        if field_added:
            repr_parts.append(',')
        repr_parts.append(' custom_id=')
        repr_parts.append(reprlib.repr(self.custom_id))
        
        # Extra descriptive fields : options | value
        # options
        options = self.options
        if (options is not None):
            repr_parts.append(', options=[')
            
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
        
        # value
        value = self.value
        if (value is not None):
            repr_parts.append(', value=')
            repr_parts.append(repr(value))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)


    def __hash__(self):
        """Returns the form submit interaction's option hash value."""
        hash_value = 0
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            hash_value ^= hash(custom_id)
        
        # options
        options = self.options
        if (options is not None):
            hash_value ^= (len(options) << 8)
            
            for option in options:
                hash_value ^= hash(option)
        
        # type
        hash_value ^= self.type.value
        
        # value
        value = self.value
        if (value is not None):
            hash_value ^= hash(value)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two submit interaction options are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # custom_id
        if self.custom_id != other.custom_id:
            return False
        
        # options
        if self.options != other.options:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        # value
        if self.value != other.value:
            return False
        
        return True
    
    
    def iter_custom_ids_and_values(self):
        """
        Iterates over all the `custom_id`-s and values of the form submit interaction option.
        
        This method is an iterable generator.
        
        Yields
        ------
        custom_id : `str`
            The `custom_id` of a represented component.
        value : `str`
            The `value` passed by the user.
        """
        custom_id = self.custom_id
        if (custom_id is not None):
            yield custom_id, self.value
        
        options = self.options
        if (options is not None):
            for option in options:
                yield from option.iter_custom_ids_and_values()

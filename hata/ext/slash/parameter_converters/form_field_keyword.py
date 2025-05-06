__all__ = ()

from scarletio import copy_docs

from .base import ParameterConverterBase

try:
    # CPython
    from re import Pattern
except ImportError:
    # ChadPython (PyPy)
    from re import _pattern_type as Pattern


class ParameterConverterFormFieldKeyword(ParameterConverterBase):
    """
    Regex and string matcher and `custom_id` matching parameter parser for forms.
    
    Attributes
    ----------
    annotation : `str | re.Pattern`
        Annotation defaulting to the parameter's name if required.
    
    default : `object`
        Default value of the parameter.
    
    parameter_name : `str`
        The parameter's name.
    
    matcher : `FunctionType`
        Matches interaction options based on their `custom_id`.
    """
    __slots__ = ('annotation', 'default', 'matcher')
    
    def __new__(cls, parameter):
        """
        Creates a new parameter converter used by form submit fields.
        
        Parameters
        ----------
        parameter : ``Parameter``
            The parameter to create converter from.
        """
        # Default annotation to parameter name
        annotation = parameter.annotation
        if (annotation is None) or (not isinstance(annotation, (str, Pattern))):
            annotation = parameter.name
        
        if isinstance(annotation, str):
            matcher = cls._converter_string
        
        else:
            group_count = annotation.groups
            group_dict = annotation.groupindex
            group_dict_length = len(group_dict)
            
            if group_dict_length and (group_dict_length != group_count):
                raise ValueError(
                    f'Regex patterns with mixed dict groups and non-dict groups are disallowed, got '
                    f'{annotation!r}.'
                )
            
            if not group_count:
                matcher = cls._converter_regex
            
            elif group_dict_length:
                matcher = cls._converter_regex_group_dict
            
            else:
                matcher = cls._converter_regex_group_tuple
        
        self = object.__new__(cls)
        self.parameter_name = parameter.name
        self.annotation = annotation
        self.default = parameter.default
        self.matcher = matcher
        return self
    
    
    @copy_docs(ParameterConverterBase.__call__)
    async def __call__(self, client, interaction_event, value):
        return self.matcher(self, interaction_event)
    
    
    @copy_docs(ParameterConverterBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        # annotation
        repr_parts.append(', annotation = ')
        repr_parts.append(repr(self.annotation))
        
        # default
        repr_parts.append(', default = ')
        repr_parts.append(repr(self.default))
    
    
    @staticmethod
    def _converter_string(converter, interaction_event):
        """
        String form submit interaction option value matcher.
        
        Parameters
        ----------
        converter : ``ParameterConverterFormFieldKeyword``
            The parent converter instance using this function.
        
        interaction_event : ``InteractionEvent``
            A received interaction event.
        
        Returns
        -------
        value : `object`
            The matched value or the converter's default value.
        """
        value = interaction_event.get_value_for(converter.annotation)
        if (value is None):
            value = converter.default
        
        return value
    
    
    @staticmethod
    def _converter_regex(converter, interaction_event):
        """
        Regex form submit interaction option value matcher.
        
        Parameters
        ----------
        converter : ``ParameterConverterFormFieldKeyword``
            The parent converter instance using this function.
        
        interaction_event : ``InteractionEvent``
            A received interaction event.
        
        Returns
        -------
        value : `object`
            The matched value or the converter's default value.
        """
        match, value = interaction_event.get_match_and_value(converter.annotation.fullmatch)
        if (value is None):
            value = converter.default
        
        return value
    
    
    @staticmethod
    def _converter_regex_group_dict(converter, interaction_event):
        """
        Regex form submit interaction option value matcher returning the matched group dictionary as well.
        
        Parameters
        ----------
        converter : ``ParameterConverterFormFieldKeyword``
            The parent converter instance using this function.
        
        interaction_event : ``InteractionEvent``
            A received interaction event.
        
        Returns
        -------
        groups : `None | dict<<str, str>`
            The matched values by the regex pattern.
        
        value : `object`
            The matched value or the converter's default value.
        """
        match, value = interaction_event.get_match_and_value(converter.annotation.fullmatch)
        if (value is None):
            value = converter.default
        
        if match is None:
            groups = None
        else:
            groups = match.groupdict()
        
        return groups, value
    
    
    @staticmethod
    def _converter_regex_group_tuple(converter, interaction_event):
        """
        Regex form submit interaction option value matcher returning the matched group tuple as well.
        
        Parameters
        ----------
        converter : ``ParameterConverterFormFieldKeyword``
            The parent converter instance using this function.
        
        interaction_event : ``InteractionEvent``
            A received interaction event.
        
        Returns
        -------
        groups : `None | tuple<str>`
            The matched values by the regex pattern.
        
        value : `object`
            The matched value or the converter's default value.
        """
        match, value = interaction_event.get_match_and_value(converter.annotation.fullmatch)
        if (value is None):
            value = converter.default
        
        if match is None:
            groups = None
        else:
            groups = match.groups()
        
        return groups, value

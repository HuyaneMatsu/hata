__all__ = ()

from .form_field_keyword import ParameterConverterFormFieldKeyword


class ParameterConverterFormFieldMulti(ParameterConverterFormFieldKeyword):
    """
    Regex and string matcher and `custom_id` matching multi parameter parser for forms.
    
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
    __slots__ = ()
    
    @staticmethod
    def _converter_string(converter, interaction_event):
        """
        String form submit interaction option multi value matcher.
        
        Parameters
        ----------
        converter : ``ParameterConverterFormFieldKeyword``
            The parent converter instance using this function.
        
        interaction_event : ``InteractionEvent``
            A received interaction event.
        
        Returns
        -------
        values : `None | list<<object>`
            The matched values.
        """
        value = interaction_event.get_value_for(converter.annotation)
        
        if (value is None):
            values = None
        else:
            values = [value]
        
        return values
    
    
    @staticmethod
    def _converter_regex(converter, interaction_event):
        """
        Regex form submit interaction option multi value matcher.
        
        Parameters
        ----------
        converter : ``ParameterConverterFormFieldKeyword``
            The parent converter instance using this function.
        
        interaction_event : ``InteractionEvent``
            A received interaction event.
        
        Returns
        -------
        values : `None`, `list<object>`
            The matched values.
        """
        values = None
        
        for match, value in interaction_event.iter_matches_and_values(converter.annotation.fullmatch):
            if (value is not None):
                if (values is None):
                    values = []
                
                values.append(value)
        
        return values
    
    
    @staticmethod
    def _converter_regex_group_dict(converter, interaction_event):
        """
        Regex form submit interaction option multi value matcher returning the matched group dictionaries as well.
        
        Parameters
        ----------
        converter : ``ParameterConverterFormFieldKeyword``
            The parent converter instance using this function.
        
        interaction_event : ``InteractionEvent``
            A received interaction event.
        
        Returns
        -------
        groups_and_values : `None | list<dict<str, str>, object)>`
            The matched values from the field's `custom_id` and their values.
        """
        values = None
        
        for match, value in interaction_event.iter_matches_and_values(converter.annotation.fullmatch):
            
            groups = match.groupdict()
            
            if (values is None):
                values = []
            
            values.append((groups, value))
       
        return values
    
    
    @staticmethod
    def _converter_regex_group_tuple(converter, interaction_event):
        """
        Regex form submit interaction option multi value matcher returning the matched group tuples as well.
        
        Parameters
        ----------
        converter : ``ParameterConverterFormFieldKeyword``
            The parent converter instance using this function.
        
        interaction_event : ``InteractionEvent``
            A received interaction event.
        
        Returns
        -------
        groups_and_values : `None | list<(tuple<str>`, object)>`
            The matched values from the field's `custom_id` and their values.
        """
        values = None
        
        for match, value in interaction_event.iter_matches_and_values(converter.annotation.fullmatch):
            groups = match.groups()
            
            if (values is None):
                values = []
            
            values.append((groups, value))
       
        return values

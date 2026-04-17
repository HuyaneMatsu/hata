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
    
    matcher : `FunctionType`ParameterConverterFormFieldMulti
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
        values : `None | list<object>`
            The matched values.
        """
        component_type, value_or_values = interaction_event.get_value_for(converter.annotation)
        
        iter_resolve = component_type.iter_resolve
        if (iter_resolve is None):
            values = None
        
        else:
            values = [*iter_resolve(interaction_event.resolved, value_or_values)]
            if not values:
                values = None
        
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
        values = []
        
        for match, component_type, value_or_values in interaction_event.iter_matches_and_values(
            converter.annotation.fullmatch
        ):
            iter_resolve = component_type.iter_resolve
            if (iter_resolve is None):
                continue
            
            values.extend(iter_resolve(interaction_event.resolved, value_or_values))
            continue
        
        if not values:
            values = None
        
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
        groups_and_values = None
        
        for match, component_type, value_or_values in interaction_event.iter_matches_and_values(
            converter.annotation.fullmatch
        ):
            resolve = component_type.resolve
            if (resolve is None):
                continue
            
            if groups_and_values is None:
                groups_and_values = []
            
            groups_and_values.append((match.groupdict(), resolve(interaction_event.resolved, value_or_values)))
        
        return groups_and_values
    
    
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
        groups_and_values = None
        
        for match, component_type, value_or_values in interaction_event.iter_matches_and_values(
            converter.annotation.fullmatch
        ):
            resolve = component_type.resolve
            if (resolve is None):
                continue
            
            if (groups_and_values is None):
                groups_and_values = []
            
            groups_and_values.append((match.groups(), resolve(interaction_event.resolved, value_or_values)))
        
        return groups_and_values

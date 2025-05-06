__all__ = ()

from scarletio import copy_docs

from .base import ParameterConverterBase


class ParameterConverterRegex(ParameterConverterBase):
    """
    Regex parameter parsing for component `custom_id`.
    
    Attributes
    ----------
    default : `object`
        Default value of the parameter.
    
    index : `int`
        the index of the regex pattern to take.
    
    parameter_name : `str`
        The parameter's name.
    
    required : `bool`
        Whether the parameter is required.
    """
    __slots__ = ('default', 'index', 'required')
    
    def __new__(cls, parameter, index):
        """
        Creates a new parameter converter from the given parameter.
        
        Parameters
        ----------
        parameter : ``Parameter``
            The parameter to create converter from.
        
        index : `int`
            The parameter's index.
        """
        self = object.__new__(cls)
        self.default = parameter.default
        self.index = index
        self.parameter_name = parameter.name
        self.required = not parameter.has_default
        return self
    
    
    @copy_docs(ParameterConverterBase.__call__)
    async def __call__(self, client, interaction_event, value):
        if value is None:
            converted_value = self.default
        
        else:
            groups = value.groups
            if value.group_dict:
                parameter_name = self.parameter_name
                try:
                    converted_value = groups[parameter_name]
                except KeyError:
                    converted_value = self.default
            else:
                index = self.index
                if index < len(groups):
                    converted_value = groups[index]
                else:
                    converted_value = self.default
        
        return converted_value
    
    
    @copy_docs(ParameterConverterBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        # index
        repr_parts.append(', index = ')
        repr_parts.append(repr(self.index))
        
        # required
        if not self.required:
            repr_parts.append(', default = ')
            repr_parts.append(repr(self.default))

__all__ = ()

from scarletio import copy_docs

from .base import ParameterConverterBase


class ParameterConverterMessageComponentKeyword(ParameterConverterBase):
    """
    Parameter converter for retrieving component value.
    
    Attributes
    ----------
    default : `object`
        Default value of the parameter.
    
    parameter_name : `str`
        The parameter's name.
    """
    __slots__ = ('annotation', 'default')
    
    def __new__(cls, parameter):
        """
        Creates a new parameter converter used by message component fields.
        
        Parameters
        ----------
        parameter : ``Parameter``
            The parameter to create converter from.
        """
        self = object.__new__(cls)
        self.parameter_name = parameter.name
        self.default = parameter.default
        return self
    
    
    @copy_docs(ParameterConverterBase.__call__)
    async def __call__(self, client, interaction_event, value):
        for custom_id, component_type, value_or_values in interaction_event.iter_custom_ids_and_values():
            resolve = component_type.resolve
            if (resolve is not None):
                value_or_values = resolve(interaction_event.resolved, value_or_values)
            break
        
        else:
            value_or_values = None
        
        if value_or_values is None:
            value_or_values = self.default
        
        return value_or_values
    
    
    @copy_docs(ParameterConverterBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        # annotation
        repr_parts.append(', annotation = ')
        repr_parts.append(repr(self.annotation))
        
        # default
        repr_parts.append(', default = ')
        repr_parts.append(repr(self.default))

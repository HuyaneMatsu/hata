__all__ = ()

from scarletio import copy_docs

from ..converter_constants import ANNOTATION_TYPE_TO_STR_ANNOTATION

from .base import ParameterConverterBase


class ParameterConverterInternal(ParameterConverterBase):
    """
    Internal parameter converter.
    
    Attributes
    ----------
    converter : `CoroutineFunctionType`
        The converter to use to convert a value to it's desired type.
    
    parameter_name : `str`
        The parameter's name.
    
    type : `int`
        Internal identifier of the converter.
    """
    __slots__ = ('converter', 'type')
    
    def __new__(cls, parameter_name, converter_type, converter):
        """
        Creates a new ``ParameterConverterInternal`` with the given parameters.
        
        Parameters
        ----------
        parameter_name : `str`
            The parameter's name.
        
        converter_type : `int`
            Internal identifier of the converter.
        
        converter : `CoroutineFunctionType`
            The converter to use to convert a value to it's desired type.
        """
        self = object.__new__(cls)
        self.parameter_name = parameter_name
        self.type = converter_type
        self.converter = converter
        return self
    
    
    @copy_docs(ParameterConverterBase.__call__)
    async def __call__(self, client, interaction_event, value):
        return await self.converter(client, interaction_event)
    
    
    @copy_docs(ParameterConverterBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        # type
        repr_parts.append(', type = ')
        repr_parts.append(ANNOTATION_TYPE_TO_STR_ANNOTATION[self.type])

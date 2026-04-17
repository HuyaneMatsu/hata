__all__ = ()

from scarletio import RichAttributeErrorBaseType


class ParameterConverterBase(RichAttributeErrorBaseType):
    """
    Base class for parameter converters.
    
    Attributes
    ----------
    parameter_name : `str`
        The parameter's name.
    """
    __slots__ = ('parameter_name',)
    
    def __new__(cls, parameter_name):
        """
        Creates a new parameter converter from the given parameter.
        
        Parameters
        ----------
        parameter_name : `str`
            The parameter's name.
        """
        self = object.__new__(cls)
        self.parameter_name = parameter_name
        return self
    
    
    async def __call__(self, client, interaction_event, value):
        """
        Calls the parameter converter to convert the given `value` to it's desired state.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective ``InteractionEvent``.
        
        interaction_event : ``InteractionEvent``
            The received application command interaction.
        
        value : `object`
            Value to convert.
        
        Returns
        -------
        converted_value : `None | object`
            If conversion fails always returns `None`.
        
        Raises
        ------
        SlashCommandParameterConversionError
            The parameter cannot be parsed.
        """
    
    
    def __repr__(self):
        """Returns the parameter converter's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # parameter_name
        repr_parts.append(' parameter_name = ')
        repr_parts.append(repr(self.parameter_name))
        
        self._put_repr_parts_into(repr_parts)
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def _put_repr_parts_into(self, repr_parts):
        """
        Helper function for sub-types to extend the created representation.
        
        Parameters
        ----------
        repr_parts : `list<str>`
            Representation parts to extended.
        """
    
    
    def as_option(self):
        """
        Converts the parameter to an application command option if applicable.
        
        Returns
        -------
        option : `None | ApplicationCommandOption`
        """
    
    
    def bind_parent(self, parent):
        """
        Binds the parent command to self.
        
        This method might be called for a few types of command functions to bind themselves to a few interactive
        parameters.
        
        Parameters
        ----------
        parent : `None | SlashCommandFunction`
            The slasher application command function to bind to self.
        """

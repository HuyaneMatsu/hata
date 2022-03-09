__all__ = ('ApplicationCommandOptionChoice',)

from scarletio import RichAttributeErrorBaseType

from .constants import (
    APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MAX, APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MIN,
    APPLICATION_COMMAND_CHOICE_VALUE_LENGTH_MAX, APPLICATION_COMMAND_CHOICE_VALUE_LENGTH_MIN
)


class ApplicationCommandOptionChoice(RichAttributeErrorBaseType):
    """
    A choice of a ``ApplicationCommandOption``.
    
    Attributes
    ----------
    name : `str`
        The choice's name. It's length can be in range [1:100].
    value : `str`, `int`, `float`
        The choice's value.
    """
    __slots__ = ('name', 'value')
    
    def __new__(cls, name, value):
        """
        Creates a new ``ApplicationCommandOptionChoice`` with the given parameters.
        
        Parameters
        ----------
        name : `str`
            The choice's name. It's length can be in range [1:100].
        value : `str`, `int`, `float`
            The choice's value.
        
        Raises
        ------
        AssertionError
            - If `name` is not `str`.
            - If `name`'s length is out of range [1:100].
            - If `value` is neither `str`, `int` nor `float`.
            - If `value` is `str` and it's length is out of range [0:100].
        """
        # name
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(
                    f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                )
            
            name_length = len(name)
            if (
                name_length < APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MIN or
                name_length > APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MAX
            ):
                raise AssertionError(
                    f'`name` length can be in range '
                    f'[{APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MIN}:{APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MAX}], '
                    f'got {name_length!r}; {name!r}.'
                )
        
        # value
        if __debug__:
            if isinstance(value, int):
                pass
            
            elif isinstance(value, str):
                value_length = len(value)
                if (
                    value_length < APPLICATION_COMMAND_CHOICE_VALUE_LENGTH_MIN or
                    value_length > APPLICATION_COMMAND_CHOICE_VALUE_LENGTH_MAX
                ):
                    raise AssertionError(
                        f'`value` length` can be in range '
                        f'[{APPLICATION_COMMAND_CHOICE_VALUE_LENGTH_MIN}:{APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MAX}]'
                        f'got {value_length!r}; {value!r}.'
                    )
            
            elif isinstance(value, float):
                pass
            
            else:
                raise AssertionError(f'`value` type can be either `str`, `int`, `float`, '
                    f'got {value.__class__.__name__}; {value!r}.')
        
        self = object.__new__(cls)
        self.name = name
        self.value = value
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new ``ApplicationCommandOptionChoice`` from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            The received application command option choice data.
        
        Returns
        -------
        self : ``ApplicationCommandOptionChoice``
            The created choice.
        """
        # name
        name = data['name']
        
        # value
        value = data['value']
        
        self = object.__new__(cls)
        self.name = name
        self.value = value
        return self
    
    
    def to_data(self):
        """
        Converts the application command option choice to a json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        
        # name
        data['name'] = self.name
        
        # value
        data['value'] = self.value
        
        return data
    
    
    def __repr__(self):
        """Returns the application command option choice's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # name
        repr_parts.append(' name=')
        repr_parts.append(repr(self.name))
        
        # value
        repr_parts.append(', value=')
        repr_parts.append(repr(self.value))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two choices are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # name
        if self.name != other.name:
            return False
        
        # value
        if self.value != other.value:
            return False
        
        return True
    
    
    def __len__(self):
        """Returns the application command choice's length."""
        length = 0
        
        # name
        length += len(self.name)
        
        # value
        value = self.value
        if isinstance(value, str):
            length += len(value)
        
        return length


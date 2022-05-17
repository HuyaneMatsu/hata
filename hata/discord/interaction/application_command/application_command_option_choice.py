__all__ = ('ApplicationCommandOptionChoice',)

from enum import Enum

from scarletio import RichAttributeErrorBaseType

from ...localizations.helpers import localized_dictionary_builder
from ...localizations.utils import build_locale_dictionary, destroy_locale_dictionary

from .constants import (
    APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MAX, APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MIN,
    APPLICATION_COMMAND_CHOICE_VALUE_LENGTH_MAX, APPLICATION_COMMAND_CHOICE_VALUE_LENGTH_MIN
)
from .helpers import apply_translation_into


class ApplicationCommandOptionChoice(RichAttributeErrorBaseType):
    """
    A choice of a ``ApplicationCommandOption``.
    
    Attributes
    ----------
    name : `str`
        The choice's name. It's length can be in range [1:100].
    name_localizations : `None`, `dict` of (``Locale``, `str`) items
        Localized names of the choice.
    value : `str`, `int`, `float`
        The choice's value.
    """
    __slots__ = ('name', 'name_localizations', 'value')
    
    def __new__(cls, name, value=None, *, name_localizations=None):
        """
        Creates a new ``ApplicationCommandOptionChoice`` with the given parameters.
        
        Parameters
        ----------
        name : `str`, `Enum`
            The choice's name. It's length can be in range [1:100].
        value : `None`, `str`, `int`, `float`, `Enum` = `None`, Optional
            The choice's value.
            
            Defaults to `name` parameter if not given.
        
        name_localizations : `None`, `dict` of ((`str`, ``Locale``), `str`) items,
                (`list`, `set`, `tuple`) of `tuple` ((`str`, ``Locale``), `str`) = `None`, Optional (Keyword only)
            Localized names of the choice.
        
        Raises
        ------
        TypeError
            - If `name_localizations`'s or any of it's item's type is incorrect.
            - If `name`'s type is incorrect.
            - If `value`'s type is incorrect.
        ValueError
            - If `name_localizations` has an item with incorrect structure.
        AssertionError
            - If `name`'s length is out of range [1:100].
            - If `value` is `str` and it's length is out of range [0:100].
        """
        if isinstance(name, str):
            choice_name = name
        
        elif isinstance(name, Enum):
            if value is None:
                choice_name = name.name
                
                if not isinstance(choice_name, str):
                    raise TypeError(
                        f'`{Enum.__name__}` choice\'s `.name` should be `str`, '
                        f'got {choice_name.__class__.__name__}; {choice_name!r}; name={name!r}; value={value!r}..'
                    )
                    
                value = name.value
            else:
                choice_name = name.value
                
                if not isinstance(choice_name, str):
                    raise TypeError(
                        f'`{Enum.__name__}` choice\'s `.value` should be `str`, '
                        f'got {choice_name.__class__.__name__}; {choice_name!r}; name={name!r}; value={value!r}.'
                    )
        
        else:
            raise TypeError(
                f'`name` can be `str`, `{Enum.__name__}`, got {name.__class__.__name__}; {name!r}.'
            )
        
        
        if __debug__:
            name_length = len(choice_name)
            if (
                name_length < APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MIN or
                name_length > APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MAX
            ):
                raise AssertionError(
                    f'`name` length can be in range '
                    f'[{APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MIN}:{APPLICATION_COMMAND_CHOICE_NAME_LENGTH_MAX}], '
                    f'got {name_length!r}; {choice_name!r}.'
                )
        
        # name_localizations
        name_localizations = localized_dictionary_builder(name_localizations, 'name_localizations')
        
        # value
        if value is None:
            choice_value = choice_name
        
        elif isinstance(value, (str, int, float)):
            choice_value = value
        
        elif isinstance(value, Enum):
            choice_value = value
            
            if not isinstance(choice_value, (str, int, float)):
                raise TypeError(
                    f'`{Enum.__name__}` choice\'s `.value` can be `str`, `int`, `float`, '
                    f'got {choice_value.__class__.__name__}; {choice_value!r}; value={value!r}.'
                )
            
        else:
            raise TypeError(
                f'`value` type can be `str`, `int`, `float`, `{Enum.__name__}`, '
                f'got {value.__class__.__name__}; {value!r}.'
            )
        
        if isinstance(choice_value, str):
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
        
        self = object.__new__(cls)
        self.name = choice_name
        self.name_localizations = name_localizations
        self.value = choice_value
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
        
        # name_localizations
        name_localizations = build_locale_dictionary(data.get('name_localizations', None))
        
        # value
        value = data['value']
        
        self = object.__new__(cls)
        self.name = name
        self.name_localizations = name_localizations
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
        
        # name_localizations
        data['name_localizations'] = destroy_locale_dictionary(self.name_localizations)
        
        # value
        data['value'] = self.value
        
        return data
    
    
    def copy(self):
        """
        Copies the ``ApplicationCommandOptionChoice``.
        
        Returns
        -------
        new : ``ApplicationCommandOptionChoice``
        """
        new = object.__new__(type(self))
        
        # name
        new.name = self.name
        
        # name_localizations
        name_localizations = self.name_localizations
        if (name_localizations is not None):
            name_localizations = name_localizations.copy()
        new.name_localizations = name_localizations
        
        # value
        new.value = self.value
        
        return new
    
    
    def __repr__(self):
        """Returns the application command option choice's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # name
        repr_parts.append(' name=')
        repr_parts.append(repr(self.name))
        
        # value
        repr_parts.append(', value=')
        repr_parts.append(repr(self.value))
        
        # Extra fields: `.name_localizations`
        
        # name_localizations
        name_localizations = self.name_localizations
        if (name_localizations is not None):
            repr_parts.append(', name_localizations=')
            repr_parts.append(repr(name_localizations))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two choices are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # name
        if self.name != other.name:
            return False
        
        # name_localizations
        if self.name_localizations != other.name_localizations:
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
        
        # name_localizations
        name_localizations = self.name_localizations
        if (name_localizations is not None):
            for value in name_localizations.values():
                length += len(value)
        
        # value
        value = self.value
        if isinstance(value, str):
            length += len(value)
        
        return length
    
    
    def apply_translation(self, translation_table, replace=False):
        """
        Applies translation from the given nested dictionary to the application command option choice.
        
        Parameters
        ----------
        translation_table : `None`, `dict` of ((``Locale``, `str`),
                (`None`, `dict` (`str`, (`None`, `str`)) items)) items
            Translation table to pull localizations from.
        replace : `bool` = `False`, Optional
            Whether actual translation should be replaced.
        """
        if translation_table is None:
            return
        
        # name
        self.name_localizations = apply_translation_into(
            self.name,
            self.name_localizations,
            translation_table,
            replace,
        )

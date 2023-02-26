__all__ = ('ApplicationCommandOptionChoice',)

import warnings

from scarletio import RichAttributeErrorBaseType

from ...localization.helpers import get_localized_length
from ...localization.utils import hash_locale_dictionary

from ..helpers import with_translation

from .fields import (
    parse_name, parse_name_localizations, parse_value, put_name_into, put_name_localizations_into, put_value_into,
    validate_name, validate_name_localizations, validate_value
)


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
    
    def __new__(cls, name, value = ..., *, name_localizations = ...):
        """
        Creates a new application command option choice with the given parameters.
        
        Parameters
        ----------
        name : `str`, `Enum`
            The choice's name. It's length can be in range [1:100].
        
        value : `None`, `str`, `int`, `float`, `Enum`, Optional
            The choice's value.
            
            Defaults to `name` parameter if not given.
        
        name_localizations : `None`, `dict` of ((`str`, ``Locale``), `str`) items,
                (`list`, `set`, `tuple`) of `tuple` ((`str`, ``Locale``), `str`), Optional (Keyword only)
            Localized names of the choice.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's length is incorrect.
        """
        if value is ...:
            value = name
        
        name = validate_name(name)
        value = validate_value(value)
        
        if name_localizations is ...:
            name_localizations = None
        else:
            name_localizations = validate_name_localizations(name_localizations)
        
        self = object.__new__(cls)
        self.name = name
        self.name_localizations = name_localizations
        self.value = value
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new application command option choice from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            The received application command option choice data.
        
        Returns
        -------
        self : `instance<cls>`
            The created choice.
        """
        self = object.__new__(cls)
        self.name = parse_name(data)
        self.name_localizations = parse_name_localizations(data)
        self.value = parse_value(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the application command option choice to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_name_into(self.name, data, defaults)
        put_name_localizations_into(self.name_localizations, data, defaults)
        put_value_into(self.value, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the application command option choice's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # name
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        # value
        repr_parts.append(', value = ')
        repr_parts.append(repr(self.value))
        
        # Extra fields: `.name_localizations`
        
        # name_localizations
        name_localizations = self.name_localizations
        if (name_localizations is not None):
            repr_parts.append(', name_localizations = ')
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
        """Returns the application command option choice's length."""
        length = 0
        
        # name & name_localizations
        length += get_localized_length(self.name, self.name_localizations)
        
        # value
        value = self.value
        if isinstance(value, str):
            length += len(value)
        
        return length
    
    
    def __hash__(self):
        """Returns the application command option choice's representation."""
        hash_value = 0
        
        # name
        hash_value ^= hash(self.name)
        
        # name_localizations
        name_localizations = self.name_localizations
        if (name_localizations is not None):
            hash_value ^= hash_locale_dictionary(name_localizations)
        
        # value
        # Do not hash `.value` of equals to `.name`
        value = self.value
        if (not isinstance(value, str)) or (value != self.name):
            hash_value ^= hash(value)
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the application command option choice.
        
        Returns
        -------
        new : `instance<type<self>>`
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
    
    
    def copy_with(self, *, name = ..., value = ..., name_localizations = ...):
        """
        Copies the application command option choice with the given fields.
        
        > Not like ``.__new__``, ``.copy_with`` will not default `value` to `name` if `value` is not provided.
        
        Parameters
        ----------
        name : `str`, `Enum`, Optional (Keyword only)
            The choice's name. It's length can be in range [1:100].
        
        name_localizations : `None`, `dict` of ((`str`, ``Locale``), `str`) items,
                (`list`, `set`, `tuple`) of `tuple` ((`str`, ``Locale``), `str`), Optional (Keyword only)
            Localized names of the choice.
        
        value : `None`, `str`, `int`, `float`, `Enum`, Optional (Keyword only)
            The choice's value.
            
            Defaults to `name` parameter if not given.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's length is incorrect.
        """
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # name_localizations
        if name_localizations is ...:
            name_localizations = self.name_localizations
            if (name_localizations is not None):
                name_localizations = name_localizations.copy()
        else:
            name_localizations = validate_name_localizations(name_localizations)
        
        # value
        if value is ...:
            value = self.value
        else:
            value = validate_value(value)
        new = object.__new__(type(self))
        
        # Construct
        new.name = name
        new.name_localizations = name_localizations
        new.value = value
        return new

    
    def apply_translation(self, translation_table, replace = False):
        """
        Applies translation from the given nested dictionary to the application command option choice.
        
        Parameters
        ----------
        translation_table : `None`, `dict` of ((``Locale``, `str`),
                (`None`, `dict` (`str`, (`None`, `str`)) items)) items
            Translation table to pull localization. from.
        replace : `bool` = `False`, Optional
            Whether actual translation should be replaced.
        """
        warnings.warn(
            (
                f'{self.__class__.__name__} is deprecated and will be removed in 2023 Jun.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        if translation_table is None:
            return
        
        # name
        self.name_localizations = with_translation(
            self.name,
            self.name_localizations,
            translation_table,
            replace,
        )
    
    
    def with_translation(self, translation_table, replace = False):
        """
        Returns a new application command option choice with the given translation table applied.
        
        Parameters
        ----------
        translation_table : `None`, `dict` of ((``Locale``, `str`), \
                (`None`, `dict` (`str`, (`None`, `str`)) items)) items
            Translation table to pull localization. from.
        replace : `bool` = `False`, Optional
            Whether actual translation should be replaced.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        if translation_table is None:
            return self
        
        new = self.copy()
        
        # name_localizations
        new.name_localizations = with_translation(
            new.name,
            new.name_localizations,
            translation_table,
            replace,
        )
        
        return new

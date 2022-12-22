__all__ = ('VerificationScreen', )

import warnings

from scarletio import RichAttributeErrorBaseType

from .fields import (
    parse_description, parse_edited_at, parse_steps, put_description_into, put_edited_at_into, put_steps_into,
    validate_description, validate_edited_at, validate_steps
)


class VerificationScreen(RichAttributeErrorBaseType):
    """
    Represents a guild's verification screen.
    
    Attributes
    ----------
    description  : `None`, `str`
        The guild's description shown in the verification screen.
    edited_at : `None`, `datetime`
        When the last version of the screen was created.
    steps : `None`, `tuple` of ``VerificationScreenStep``
        The step in the verification screen.
    """
    __slots__ = ('edited_at', 'description', 'steps')
    
    def __new__(cls, *, edited_at = ..., description = ..., steps = ...):
        """
        Creates a new verification screen instance.
        
        Parameters
        ----------
        description  : `None`, `str`, Optional (Keyword only)
            The guild's description shown in the verification screen.
        edited_at : `None`, `datetime`, Optional (Keyword only)
            When the last version of the screen was created.
        steps : `None`, `tuple` of ``VerificationScreenStep``, Optional (Keyword only)
            The step in the verification screen.
        
        Raises
        ------
        TypeError
            - If a parameter's type is invalid.
        ValueError
            - If a parameter's value is invalid.
        """
        # edited_at
        if edited_at is ...:
            edited_at = None
        else:
            edited_at = validate_edited_at(edited_at)
        
        # description
        if description is ...:
            description = None
        else:
            description = validate_description(description)
        
        # steps
        if steps is ...:
            steps = None
        else:
            steps = validate_steps(steps)
        
        # Construct
        self = object.__new__(cls)
        self.edited_at = edited_at
        self.description = description
        self.steps = steps
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new verification screen from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Verification screen data.
        """
        self = object.__new__(cls)
        self.edited_at = parse_edited_at(data)
        self.description = parse_description(data)
        self.steps = parse_steps(data)
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the verification screen to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        
        put_description_into(self.description, data, defaults)
        put_steps_into(self.steps, data, defaults)
        
        if include_internals:
            put_edited_at_into(self.edited_at, data, defaults)
        
        return data
    
    
    def __repr__(self):
        """Returns the verification screen's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        field_added = False
        
        # description
        description = self.description
        if (description is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' description = ')
            repr_parts.append(repr(description))
        
        # steps
        steps = self.steps
        if (steps is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' steps = [')
            
            index = 0
            limit = len(steps)
            
            while True:
                step = steps[index]
                
                repr_parts.append(repr(step))
                
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        # edited_at
        edited_at = self.edited_at
        if (edited_at is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' edited_at = ')
            repr_parts.append(repr(edited_at))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the verification screen's hash value."""
        hash_value = 0
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= hash(description)
        
        # edited_at
        # Internal field, skip
        
        # steps
        steps = self.steps
        if (steps is not None):
            hash_value ^= len(steps)
            
            for step in steps:
                hash_value ^= hash(step)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two verification screens are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # description
        if self.description != other.description:
            return False
        
        # steps
        if self.steps != other.steps:
            return False
        
        return True
    
    @property
    def created_at(self):
        """
        ``.created_at`` is deprecated and will be removed in 2023 April. Please use ``.edited_at`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.created_at` is deprecated and will be removed in 2023 April. '
                f'Please use `.edited_at` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return self.edited_at
    
    
    def copy(self):
        """
        Copies the verification screen.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.edited_at = self.edited_at
        new.description = self.description
        steps = self.steps
        if (steps is not None):
            steps = tuple(step.copy() for step in steps)
        new.steps = steps
        return new
    
    
    def copy_with(self, edited_at = ..., description = ..., steps = ...):
        """
        Copies the verification screen with the given fields.
        
        Parameters
        ----------
        description  : `None`, `str`, Optional (Keyword only)
            The guild's description shown in the verification screen.
        edited_at : `None`, `datetime`, Optional (Keyword only)
            When the last version of the screen was created.
        steps : `None`, `tuple` of ``VerificationScreenStep``, Optional (Keyword only)
            The step in the verification screen.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is invalid.
        ValueError
            - If a parameter's value is invalid.
        """
        # edited_at
        if edited_at is ...:
            edited_at = self.edited_at
        else:
            edited_at = validate_edited_at(edited_at)
        
        # description
        if description is ...:
            description = self.description
        else:
            description = validate_description(description)
        
        # steps
        if steps is ...:
            steps = self.steps
            if (steps is not None):
                steps = tuple(step.copy() for step in steps)
        else:
            steps = validate_steps(steps)
        
        # Construct
        new = object.__new__(type(self))
        new.edited_at = edited_at
        new.description = description
        new.steps = steps
        return new
    
    
    def iter_steps(self):
        """
        Iterates over the steps of the verification screen.
        
        This method is an iterable generator.
        
        Yields
        ------
        step : ``VerificationScreenStep``
        """
        steps = self.steps
        if (steps is not None):
            yield from steps

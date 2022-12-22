__all__ = ('VerificationScreenStep', )

import warnings

from scarletio import BaseMethodDescriptor, RichAttributeErrorBaseType

from .fields import (
    parse_required, parse_title, parse_type, parse_values, put_required_into, put_title_into, put_type_into,
    put_values_into, validate_required, validate_title, validate_type, validate_values
)
from .preinstanced import VerificationScreenStepType


class VerificationScreenStep(RichAttributeErrorBaseType):
    """
    Represents a step of a ``VerificationScreen``.
    
    Attributes
    ----------
    required : `bool`
        Whether the user must accept this step to continue.
    title : `str`
        The step's title.
    type : ``VerificationScreenStepType``
        The type of the step.
    values : `None`, `tuple` of `str`
        The values of the step.
    """
    __slots__ = ('required', 'title', 'type', 'values')
    
    
    def __new__(cls, *, required = ..., step_type = ..., title = ..., values= ...):
        """
        Creates a new verification screen step.
        
        Parameters
        ----------
        required : `bool`, Optional (Keyword only)
            Whether the user must accept this step to continue.
        step_type : ``VerificationScreenStepType``, Optional (Keyword only)
            The type of the step.
        title : `str`, Optional (Keyword only)
            The step's title.
        values : `None`, `iterable` of `str`, Optional (Keyword only)
            The values of the step.
        
        Raises
        ------
        TypeError
            - If a parameter's type is invalid.
        ValueError
            - If a parameter's value is invalid.
        """
        # required
        if required is ...:
            required = False
        else:
            required = validate_required(required)
        
        # title
        if title is ...:
            title = ''
        else:
            title = validate_title(title)
        
        # step_type
        if step_type is ...:
            step_type = VerificationScreenStepType.rules
        else:
            step_type = validate_type(step_type)
        
        # values
        if values is ...:
            values = None
        else:
            values = validate_values(values)
        
        # Construct
        self = object.__new__(cls)
        self.required = required
        self.title = title
        self.type = step_type
        self.values = values
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new verification screen step from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Verification screen step data.
        """
        self = object.__new__(cls)
        self.required = parse_required(data)
        self.title = parse_title(data)
        self.type = parse_type(data)
        self.values = parse_values(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the verification screen step to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`)
        """
        data = {}
        put_required_into(self.required, data, defaults)
        put_title_into(self.title, data, defaults)
        put_type_into(self.type, data, defaults)
        put_values_into(self.values, data, defaults)
        return data
    
    
    @BaseMethodDescriptor
    def custom(cls, base, *, type = ..., step_type = ..., **keyword_parameters):
        """
        Deprecated and will be removed in 2023 April. Please use ``.__new__`` or ``.copy_with`` respectively.
        """
        warnings.warn(
            (
                f'`{cls.__name__}.custom` is deprecated and will be removed in 2023 April. '
                f'Please use `.__new__` or `.copy_with` respectively.'
            ),
            FutureWarning,
            stacklevel = 3,
        )
        
        if type is not ...:
            warnings.warn(
                (
                    f'`{cls.__name__}.custom`\'s `type` parameters is deprecated. Please use `step_type` instead.'
                ),
                FutureWarning,
                stacklevel = 3,
            )
            step_type = type
        
        if base is None:
            return cls.__new__(cls, step_type = step_type, **keyword_parameters)
        
        return base.copy_with(step_type = step_type, **keyword_parameters)
    
    
    def __repr__(self):
        """Returns the verification screen step's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' title = ')
        repr_parts.append(repr(self.title))
        
        step_type = self.type
        repr_parts.append(', type = ')
        repr_parts.append(step_type.name)
        
        required = self.required
        if required:
            repr_parts.append(', required = ')
            repr_parts.append(repr(required))
        
        values = self.values
        if (values is not None):
            repr_parts.append(', values = [')
            
            index = 0
            limit = len(values)
            
            while True:
                value = values[index]
                
                repr_parts.append(repr(value))
                
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the verification screen step's hash value."""
        hash_value = 0
        
        # required
        hash_value ^= self.required << 14
        
        # title
        hash_value ^= hash(self.title)
        
        # type
        hash_value ^= hash(self.type)
        
        # values
        values = self.values
        if (values is not None):
            hash_value ^= len(values)
            
            for value in values:
                hash_value ^= hash(value)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two verification screen steps are equal"""
        if type(self) is not type(other):
            return NotImplemented
        
        # required
        if self.required != other.required:
            return False
        
        # title
        if self.title != other.title:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        # values
        if self.values != other.values:
            return False
        
        return True
    
    
    def copy(self):
        """
        Copies the verification screen step.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.required = self.required
        new.title = self.title
        new.type = self.type
        values = self.values
        if (values is not None):
            values = (*values,)
        new.values = values
        return new
    
    
    def copy_with(self, *, required = ..., step_type = ..., title = ..., values= ...):
        """
        Copies the verification step with the given fields.
        
        Parameters
        ----------
        required : `bool`, Optional (Keyword only)
            Whether the user must accept this step to continue.
        step_type : ``VerificationScreenStepType``, Optional (Keyword only)
            The type of the step.
        title : `str`, Optional (Keyword only)
            The step's title.
        values : `None`, `iterable` of `str`, Optional (Keyword only)
            The values of the step.
        
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
        # required
        if required is ...:
            required = self.required
        else:
            required = validate_required(required)
        
        # title
        if title is ...:
            title = self.title
        else:
            title = validate_title(title)
        
        # step_type
        if step_type is ...:
            step_type = self.type
        else:
            step_type = validate_type(step_type)
        
        # values
        if values is ...:
            values = self.values
            if (values is not None):
                values = (*values,)
        else:
            values = validate_values(values)
        
        # Construct
        new = object.__new__(type(self))
        new.required = required
        new.title = title
        new.type = step_type
        new.values = values
        return new
    
    
    def iter_values(self):
        """
        Iterates over the values of the verification screen.
        
        This method is an iterable generator.
        
        Yields
        ------
        value : `str`
        """
        values = self.values
        if (values is not None):
            yield from values

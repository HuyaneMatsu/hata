__all__ = ('VerificationScreenStep', 'VerificationScreen', )

import reprlib

from ...backend.utils import BaseMethodDescriptor

from ..utils import DATETIME_FORMAT_CODE, timestamp_to_datetime, datetime_to_timestamp
from ..preconverters import preconvert_preinstanced_type
from .preinstanced import VerificationScreenStepType


class VerificationScreen:
    """
    Represents a guild's verification screen.
    
    Attributes
    ----------
    created_at : `datetime`
        When the last version of the screen was created.
    description  : `None` or `str`
        The guild's description shown in the verification screen.
    steps : `tuple` of ``VerificationScreenStep``
        The step in the verification screen.
    """
    __slots__ = ('created_at', 'description', 'steps')
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new verification screen from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Verification screen data.
        """
        self = object.__new__(cls)
        self.created_at = timestamp_to_datetime(data['version'])
        self.description = data.get('description', None)
        self.steps = tuple(VerificationScreenStep.from_data(field_data) for field_data in data['form_fields'])
        return self
    
    def to_data(self):
        """
        Converts the verification screen to a json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`)
        """
        return {
            'version' : datetime_to_timestamp(self.created_at),
            'description' : self.description,
            'form_fields' : [step.to_data() for step in self.steps],
        }
    
    def __repr__(self):
        """Returns the verification screen's representation."""
        return (f'<{self.__class__.__name__} created_at={self.created_at:{DATETIME_FORMAT_CODE}}, '
            f'description={reprlib.repr(self.description)}, steps length={len(self.steps)!r}>')
    
    def __hash__(self):
        """Returns the verification screen's hash value."""
        return hash(self.description) ^ hash(self.steps)
    
    def __eq__(self, other):
        """Returns whether the two verification screens are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.description != other.description:
            return False
        
        if self.steps != other.steps:
            return False
        
        return True


class VerificationScreenStep:
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
    values : `None` or `list` of `str`
        The values of the step. Sets as `None` if would be set as an empty list.
    """
    __slots__ = ('required', 'title', 'type', 'values')
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new verification screen step from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Verification screen step data.
        """
        values = data.get('values', None)
        if (values is not None) and (not values):
            values = None
        
        self = object.__new__(cls)
        self.required = data['required']
        self.title = data['label']
        self.type = VerificationScreenStepType.get(data['field_type'])
        self.values = values
        return self
    
    def to_data(self):
        """
        Converts the verification screen step to a json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`)
        """
        values = self.values
        if values is None:
            values = []
        
        return {
            'required' : self.required,
            'label' : self.title,
            'field_type': self.type.value,
            'values' : values
        }
    
    @BaseMethodDescriptor
    def custom(cls, base, **kwargs):
        """
        Creates a custom ``VerificationScreenStep`` with the given parameters.
        
        Parameters
        ----------
        **kwargs : keyword parameters
            Additional attributes of the verification screen step.
        
        Other Parameters
        ----------------
        title : `str`, Optional
            The title of the step.
        values : `None` or (`tuple` or `list`) of `str`
            The values of the step.
            
            Defaults to `None` if called as a classmethod.
        required : `bool`, Optional
            Whether the user must accept this step to continue.
            
            Defaults to `True` if called as classmethod.
        type_ : ``VerificationScreenStepType`` or `str`, Optional
            The type of the step.
            
            Defaults to ``VerificationScreenStepType`` `.rules` if called as classmethod.
        
        Returns
        -------
        self : ``VerificationScreenStep``
        
        Raises
        ------
        TypeError
            - If `type_` was not given neither as ``VerificationScreenStepType`` nor as `str` instance.
            - If `title` was not given as `str` instance.
            - If `values` is not given neither as `None`, or `tuple` or `list` instance.
            - If `values` contains not only `str` instances.
            - If `required` was not given as `bool` instance.
        ValueError
            - If `type_` was given as `str` instance, ubt not any of the precreated ones.
            - If `title` was given as an empty string.
            - If `values` contains an empty string.
        """
        try:
            title = kwargs.pop('title')
        except KeyError:
            if base is None:
                raise TypeError(f'`title` is a required parameter if `{cls.__name__}.custom` is called as a '
                    f'classmethod.') from None
            
            title = base.title
        else:
            if not isinstance(title, str):
                raise TypeError(f'`title` can be given as `str` instance, got {title.__class__.__name__}.')
            
            if not title:
                raise ValueError(f'`title` cannot be given as empty string.')
        
        try:
            values = kwargs.pop('values')
        except KeyError:
            if base is None:
                values = None
            else:
                values = base.values
        
        else:
            if (values is not None):
                if not isinstance(values, (list, tuple)):
                    raise TypeError(f'`values` can be given as `tuple` or `list` instance, got '
                        f'{values.__class__.__name__}.')
                
                for index, value in enumerate(values):
                    if not isinstance(value, str):
                        raise TypeError(f'`values` index `{index}` is not `str` instance expected, but got '
                            f'{value.__class__.__name__}; {value!r}.')
                    
                    if not value:
                        raise ValueError(f'`values` index `{index}` is an empty string.')
                    
                if values:
                    values = tuple(values)
                else:
                    values = None
        
        try:
            required = kwargs.pop('required')
        except KeyError:
            if base is None:
                required = True
            else:
                required = base.required
        else:
            if not isinstance(required, bool):
                raise TypeError(f'`required` can be given as `bool` instance, got {required.__class__.__name__}.')
        
        try:
            type_ = kwargs.pop('type')
        except KeyError:
            if base is None:
                type_ = VerificationScreenStepType.rules
            else:
                type_ = base.type
        else:
            type_ = preconvert_preinstanced_type(type_, 'type_', VerificationScreenStepType)
        
        if kwargs:
            raise TypeError(f'Unused parameters: {", ".join(list(kwargs))}')
        
        self = object.__new__(cls)
        self.title = title
        self.values = values
        self.required = required
        self.type = type_
        return self
    
    def __repr__(self):
        """Returns the verification screen step's representation."""
        return (f'<{self.__class__.__name__} title={self.title!r}, type={self.type.value}, required={self.required!r}, '
            f'values length={len(self.values)!r}>')
    
    def __hash__(self):
        """Returns the verification screen step's hash value."""
        return hash(self.title) ^ hash(self.values) ^ ((self.required)<<16) ^ hash(self.type)

    def __eq__(self, other):
        """Returns whether the two verification screen steps are equal"""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.type is not other.type:
            return False
        
        if self.required != other.required:
            return False
        
        if self.title != other.title:
            return False
        
        if self.values != other.values:
            return False
        
        return True

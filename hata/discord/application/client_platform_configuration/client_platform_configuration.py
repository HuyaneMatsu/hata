__all__ = ('ClientPlatformConfiguration',)

from scarletio import RichAttributeErrorBaseType

from ...utils import DATETIME_FORMAT_CODE

from .fields import (
    parse_label_type, parse_labelled_until, parse_release_phase, put_label_type_into, put_labelled_until_into,
    put_release_phase_into, validate_label_type, validate_labelled_until, validate_release_phase
)
from .preinstanced import LabelType, ReleasePhase


class ClientPlatformConfiguration(RichAttributeErrorBaseType):
    """
    Represents an embedded activity's configuration on a client's platform.
    
    Attributes
    ----------
    label_type : ``LabelType``
        The label's type on the client's platform.
    labelled_until : `None | DateTime`
        Till when is the label shown.
    release_phase : ``ReleasePhase``
        What release phase is the embedded activity is on the client's platform.
    """
    __slots__ = ('label_type', 'labelled_until', 'release_phase', )
    
    def __new__(cls, *, label_type = ..., labelled_until = ..., release_phase = ...):
        """
        Creates a new client platform configuration.
        
        Parameters
        ----------
        label_type : `LabelType | int`, Optional (Keyword only)
            The label's type on the client's platform.
        labelled_until : `None | DateTime`, Optional (Keyword only)
            Till when is the label shown.
        release_phase : `ReleasePhase | str`, Optional (Keyword only)
            What release phase is the embedded activity is on the client's platform.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        """
        # label_type
        if label_type is ...:
            label_type = LabelType.none
        else:
            label_type = validate_label_type(label_type)
        
        # labelled_until
        if labelled_until is ...:
            labelled_until = None
        else:
            labelled_until = validate_labelled_until(labelled_until)
        
        # release_phase
        if release_phase is ...:
            release_phase = ReleasePhase.global_launch
        else:
            release_phase = validate_release_phase(release_phase)
        
        # Construct
        self = object.__new__(cls)
        self.label_type = label_type
        self.labelled_until = labelled_until
        self.release_phase = release_phase
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a client platform configuration from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Client platform configuration data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.label_type = parse_label_type(data)
        self.labelled_until = parse_labelled_until(data)
        self.release_phase = parse_release_phase(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serializes the client platform configuration.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields of their default value should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_label_type_into(self.label_type, data, defaults)
        put_labelled_until_into(self.labelled_until, data, defaults)
        put_release_phase_into(self.release_phase, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the client platform configuration's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        label_type = self.label_type
        repr_parts.append(' label_type = ')
        repr_parts.append(label_type.name)
        repr_parts.append(' ~ ')
        repr_parts.append(repr(label_type.value))
        
        
        labelled_until = self.labelled_until
        repr_parts.append(', labelled_until = ')
        if labelled_until is None:
            repr_parts.append('None')
        else:
            repr_parts.append(format(labelled_until, DATETIME_FORMAT_CODE))
        
        release_phase = self.release_phase
        repr_parts.append(', release_phase = ')
        repr_parts.append(release_phase.name)
        repr_parts.append(' ~ ')
        repr_parts.append(repr(release_phase.value))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two client platform configurations are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.label_type is not other.label_type:
            return False
        
        if self.labelled_until != other.labelled_until:
            return False
        
        if self.release_phase is not other.release_phase:
            return False
        
        return True
    

    def __hash__(self):
        """Returns the client platform configuration's hash value."""
        hash_value = 0
        
        hash_value ^= hash(self.label_type)
        
        labelled_until = self.labelled_until
        if (labelled_until is not None):
            hash_value ^= hash(labelled_until)
        
        hash_value ^= hash(self.release_phase) << 4
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the client platform configuration.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.label_type = self.label_type
        new.labelled_until = self.labelled_until
        new.release_phase = self.release_phase
        return new
    
    
    def copy_with(self, *, label_type = ..., labelled_until = ..., release_phase = ...):
        """
        Copies the client platform configuration with the given fields.
        
        Parameters
        ----------
        label_type : `LabelType | int`, Optional (Keyword only)
            The label's type on the client's platform.
        labelled_until : `None | DateTime`, Optional (Keyword only)
            Till when is the label shown.
        release_phase : `ReleasePhase | str`, Optional (Keyword only)
            What release phase is the embedded activity is on the client's platform.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        """
        # label_type
        if label_type is ...:
            label_type = self.label_type
        else:
            label_type = validate_label_type(label_type)
        
        # labelled_until
        if labelled_until is ...:
            labelled_until = self.labelled_until
        else:
            labelled_until = validate_labelled_until(labelled_until)
        
        # release_phase
        if release_phase is ...:
            release_phase = self.release_phase
        else:
            release_phase = validate_release_phase(release_phase)
        
        # Construct
        new = object.__new__(type(self))
        new.label_type = label_type
        new.labelled_until = labelled_until
        new.release_phase = release_phase
        return new

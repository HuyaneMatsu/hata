__all__ = ('AutoModerationAction',)

from scarletio import RichAttributeErrorBaseType, copy_docs

from ..action_metadata import AutoModerationActionMetadataBase

from .fields import parse_metadata, parse_type, put_metadata_into, put_type_into, validate_type
from .helpers import guess_action_type_from_keyword_parameters
from .preinstanced import AutoModerationActionType


class AutoModerationAction(RichAttributeErrorBaseType):
    """
    An action that is executed when a rule is triggered.
    
    Attributes
    ----------
    metadata : ``AutoModerationActionMetadataBase``
        Characterises the action
    type : ``AutoModerationActionType``
        The action's type.
    """
    __slots__ = ('metadata', 'type')
    
    def __new__(cls, action_type = None, **keyword_parameters):
        """
        Creates a new auto moderation action from the given parameters.
        
        Parameters
        ----------
        action_type : ``AutoModerationActionType``, `int`, Optional
            The moderation action's type.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters to pass
        
        Other Parameters
        ----------------
        channel_id : `None`, ``Channel``, `int`, Optional (Keyword only)
            The channel where the alert messages should be sent.
            
            > Mutually exclusive with the `duration` parameter.
        
        duration : `None`, `int`, `float`, Optional (Keyword only)
            The timeout's duration applied on trigger.
            
            > Mutually exclusive with the `channel` parameter.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
            - Parameter mismatch.
        """
        action_type = validate_type(action_type)
        action_type = guess_action_type_from_keyword_parameters(action_type, keyword_parameters)
        metadata = action_type.metadata_type(**keyword_parameters)
        
        self = object.__new__(cls)
        self.type = action_type
        self.metadata = metadata
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new ``AutoModerationAction`` from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received auto moderation action data.
        
        Returns
        -------
        self : ``AutoModerationAction``
            The created auto moderation rule.
        """
        action_type = parse_type(data)
        metadata = parse_metadata(data, action_type)
        
        self = object.__new__(cls)
        self.type = action_type
        self.metadata = metadata
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the auto moderation action to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        put_type_into(self.type, data, defaults)
        put_metadata_into(self.metadata, data, defaults)
        return data
    
    
    def __eq__(self, other):
        """Returns whether the two auto moderation actions are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.type is not other.type:
            return False
        
        if self.metadata != other.metadata:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the auto moderation action's hash value."""
        hash_value = 0
        
        hash_value ^= self.type.value
        
        metadata = self.metadata
        if (metadata is not None):
            hash_value ^= hash(metadata)
        
        return hash_value
    
    
    def __repr__(self):
        """Returns the auto moderation action's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # type
        type_ = self.type
        
        repr_parts.append(' type = ')
        repr_parts.append(repr(type_.name))
        repr_parts.append('~')
        repr_parts.append(repr(type_.value))
        
        # metadata
        metadata = self.metadata
        if (metadata is not None):
            repr_parts.append(', metadata = ')
            repr_parts.append(repr(metadata))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def copy(self):
        """
        Copies the auto moderation action.
        
        Returns
        -------
        new : ``AutoModerationAction``
        """
        new = object.__new__(type(self))
        
        # metadata
        new.metadata = self.metadata.copy()
        
        # type
        new.type = self.type
        
        return new

    
    def copy_with(self, *, action_type = ..., **keyword_parameters):
        """
        Copies the auto moderation action with the given attributes replaced.
        
        Parameters
        ----------
        action_type : ``AutoModerationActionType``, `int`, Optional (Keyword only)
            The moderation action's type.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters to pass
        
        Other Parameters
        ----------------
        channel_id : `None`, ``Channel``, `int`, Optional (Keyword only)
            The channel where the alert messages should be sent.
            
            > Mutually exclusive with the `duration` parameter.
        
        duration : `None`, `int`, `float`, Optional (Keyword only)
            The timeout's duration applied on trigger.
            
            > Mutually exclusive with the `channel` parameter.
        
        Returns
        -------
        self : ``AutoModerationAction``
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        """
        if action_type is ...:
            if keyword_parameters:
                action_type = guess_action_type_from_keyword_parameters(AutoModerationActionType.none, keyword_parameters)
            else:
                action_type = self.type
        else:
            action_type = validate_type(action_type)
        
        if action_type is self.type:
            metadata = self.metadata.copy_with(**keyword_parameters)
        else:
            metadata = action_type.metadata_type(**keyword_parameters)
        
        new = object.__new__(type(self))
        new.type = action_type
        new.metadata = metadata
        return new
    
    
    # ---- Field proxies ----
    
    @property
    @copy_docs(AutoModerationActionMetadataBase.channel_id)
    def channel_id(self):
        return self.metadata.channel_id
    
    
    @property
    @copy_docs(AutoModerationActionMetadataBase.duration)
    def duration(self):
        return self.metadata.duration
    
    # ---- Utility proxies ----
    
    @property
    @copy_docs(AutoModerationActionMetadataBase.channel)
    def channel(self):
        return self.metadata.channel

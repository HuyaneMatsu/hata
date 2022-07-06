__all__ = ('AutoModerationAction',)

from scarletio import RichAttributeErrorBaseType

from ..preconverters import preconvert_preinstanced_type

from .preinstanced import AutoModerationActionType


def _validate_action_type_with_metadata_options(action_type, channel, duration):
    """
    Validates the given `action_type` with the `channel`, `duration` options. If any option is given, the
    `action_type` will default towards it. On any mismatch exception is raised.
    
    Parameters
    ----------
    action_type : `Ellipsis`, `int`, ``AutoModerationActionType``
        Auto moderation action type.
    
    channel : `Ellipsis`, `None`, ``Channel``, `int`
        The channel where the alert messages should be sent.

    duration : `Ellipsis`, `None`, `int`, `float`
        The timeout's duration applied on trigger.
    
    Returns
    -------
    action_metadata : `None`, ``AutoModerationActionMetadata``
        Action type specific metadata if applicable.
    action_type : ``AutoModerationActionType``
        The final processed action type.
    
    Raises
    ------
    TypeError
        - If a parameter's type is incorrect.
        - If there are multiple mutually exclusive options.
        - If action type not detectable.
        - If multiple action types detected.
    ValueError
        - If a parameter's value is incorrect.
    """
    if (action_type is not ...):
        action_type = preconvert_preinstanced_type(action_type, 'action_type', AutoModerationActionType)
    
    if (channel is not ...) + (duration is not ...) > 1:
        raise TypeError(
            f'`channel` and `duration` parameters are mutually exclusive, got '
            f'channel={channel!r}; duration={duration!r}.'
        )
    
    if (channel is not ...):
        probable_action_type = AutoModerationActionType.send_alert_message
        metadata_parameter = channel
    
    elif (duration is not ...):
        probable_action_type = AutoModerationActionType.timeout
        metadata_parameter = duration
    
    else:
        probable_action_type = None
        metadata_parameter = None
    
    if (action_type is ...):
        if (probable_action_type is None):
            raise TypeError(
                f'`action_type` is not given or is given as `None`, and cannot be detected from `channel` '
                'or from `duration` parameters.'
            )
        
        action_type = probable_action_type
    
    else:
        if (probable_action_type is not None):
            if (action_type is not probable_action_type):
                if (channel is not ...):
                    received_parameter_name = 'channel'
                    received_parameter_value = channel
                    
                else:
                    received_parameter_name = 'duration'
                    received_parameter_value = duration
                
                raise TypeError(
                    f'Both `action_type` and `{received_parameter_name}` parameters refer to a different '
                    f'action type, got action_type={action_type!r}, '
                    f'{received_parameter_name}={received_parameter_value!r}.'
                )
    
    action_metadata_type = action_type.metadata_type
    if (action_metadata_type is None):
        action_metadata = None
    
    else:
        action_metadata = action_metadata_type(metadata_parameter)
    
    return action_metadata, action_type


class AutoModerationAction(RichAttributeErrorBaseType):
    """
    An action that is executed when a rule is triggered.
    
    Attributes
    ----------
    metadata : `None`, ``AutoModerationActionMetadata``
        Characterises the action
    type : ``AutoModerationActionType``
        The action's type.
    """
    __slots__ = ('metadata', 'type')
    
    def __new__(cls, action_type=..., *, channel=..., duration=...):
        """
        Creates a new auto moderation action from the given parameters.
        
        Parameters
        ----------
        action_type : ``AutoModerationActionType``, `int`, Optional
            The moderation action's type.
        
        channel : `None`, ``Channel``, `int`, Optional (Keyword only)
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
        # type & channel & duration
        metadata, type_ = _validate_action_type_with_metadata_options(action_type, channel, duration)
        
        self = object.__new__(cls)
        self.type = type_
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
        # type_
        type_ = AutoModerationActionType.get(data['type'])
        
        metadata_type = type_.metadata_type
        if (metadata_type is None):
            metadata = None
        
        else:
            metadata = metadata_type.from_data(data['metadata'])
        
        self = object.__new__(cls)
        self.type = type_
        self.metadata = metadata
        return self
    
    
    def to_data(self):
        """
        Converts the auto moderation action to a json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        
        # type
        data['type'] = self.type.value
        
        # metadata
        metadata = self.metadata
        if metadata is None:
            metadata_data = {}
        else:
            metadata_data = metadata.to_data()
        
        data['metadata'] = metadata_data
        
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
        
        repr_parts.append(' type=')
        repr_parts.append(repr(type_.name))
        repr_parts.append('~')
        repr_parts.append(repr(type_.value))
        
        # metadata
        metadata = self.metadata
        if (metadata is not None):
            repr_parts.append(', metadata=')
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
        metadata = self.metadata
        if (metadata is not None):
            metadata = metadata.copy()
        new.metadata = metadata
        
        # type
        new.type = self.type
        
        return new

    
    def copy_with(self, **keyword_parameters):
        """
        Copies the auto moderation action with the given attributes replaced.
        
        Parameters
        ----------
        action_type : ``AutoModerationActionType``, `int`, Optional (Keyword only)
            The moderation action's type.
        
        channel : `None`, ``Channel``, `int`, Optional (Keyword only)
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
            - Parameter mismatch.
        """
        # trigger_metadata & trigger_type
        action_type = keyword_parameters.pop('action_type', ...)
        channel = keyword_parameters.pop('channel', ...)
        duration = keyword_parameters.pop('duration', ...)
        
        if (action_type is ...) and (channel is ...) and (duration is ...):
            metadata = self.metadata
            if (metadata is not None):
                metadata = metadata.copy()
            
            type_ = self.type
            
        else:
            metadata, type_ = _validate_action_type_with_metadata_options(
                action_type, channel, duration
            )
            
        self = object.__new__(type(self))
        self.type = type_
        self.metadata = metadata
        return self

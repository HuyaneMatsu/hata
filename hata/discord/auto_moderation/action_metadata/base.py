__all__ = ('AutoModerationActionMetadataBase',)

from scarletio import RichAttributeErrorBaseType

from ...bases import PlaceHolder
from ...channel import ChannelType, create_partial_channel_from_id


class AutoModerationActionMetadataBase(RichAttributeErrorBaseType):
    """
    Base class for ``AutoModerationAction``'s action metadata.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new action metadata instance.
        """
        return object.__new__(cls)
    
    
    def __repr__(self):
        """Returns the action metadata's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new auto moderation action metadata instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
           Auto moderation action metadata payload.
        
        Returns
        -------
        self : `instance<cls>`
        """
        return object.__new__(cls)
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the action metadata to json serializable object.
        
        Parameters
        ----------
        defaults : `bool`
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        return {}
    
    
    def __eq__(self, other):
        """Returns whether the two action metadatas are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return True
    
    
    def __hash__(self):
        """Returns the action metadata's hash value."""
        return 0
    
    
    def copy(self):
        """
        Copies the action metadata.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        return object.__new__(type(self))
    
    
    def copy_with(self):
        """
        Copies the action metadata and modifies it's attributes by the given values.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        return self.copy()
    
    # ---- Place holders ----
    
    channel_id = PlaceHolder(
        0,
        """
        The channel's identifier where the alert messages are sent.
        
        Returns
        -------
        channel_id : `int`
        """
    )
    
    duration = PlaceHolder(
        0,
        """
        The timeout's duration applied on trigger.
        
        Returns
        -------
        duration : `int`
        """
    )
    
    custom_message = PlaceHolder(
        None,
        """
        A custom message that can be used as an explanation if a message is blocked.
        
        Returns
        -------
        custom_message : `None`, `str`
        """
    )
    
    # ---- Additional utility ---
    
    @property
    def channel(self):
        """
        Returns the channels where the alert messages are sent.
        
        Returns
        -------
        channel : `None`, ``Channel``
        """
        channel_id = self.channel_id
        if channel_id:
            return create_partial_channel_from_id(channel_id, ChannelType.unknown, 0)

__all__ = ('ActivityCustom',)

from ...backend.export import include
from ..utils import DISCORD_EPOCH_START, unix_time_to_datetime, datetime_to_unix_time

from .activity_base import ActivityBase
from . import activity_types as ACTIVITY_TYPES

create_partial_emoji_from_data = include('create_partial_emoji_from_data')

class ActivityCustom(ActivityBase):
    """
    Represents a Discord custom activity.
    
    Attributes
    ----------
    created : `int`
        When the status was created as Unix time in milliseconds. Defaults to `0`.
    emoji : `None` or ``Emoji``
        The emoji of the activity. If it has no emoji, then set as `None`.
    state : `None` or `str`
        The activity's text under it's emoji. Defaults to `None`.
    
    Class Attributes
    ----------------
    id : `int` = `0`
        The activity's id.
    type : `int` = `4`
        The activity's type value.
    """
    __slots__ = ('created_at', 'emoji', 'state', )
    
    type = ACTIVITY_TYPES.custom
    
    @classmethod
    def from_data(cls, activity_data):
        """
        Creates a new ``ActivityCustom`` instance from the given activity data.
        
        Parameters
        ----------
        activity_data : `dict` of (`str`, `Any`) items
            Received activity data.
        
        Returns
        -------
        self : ``ActivityCustom``
        """
        self = object.__new__(cls)
        self._update_attributes(activity_data)
        return self
    
    def __hash__(self):
        """Returns the activity's hash value."""
        state = self.state
        emoji = self.emoji
        if (state is None):
            if (emoji is None):
                hash_ = 0
            else:
                hash_ = emoji.id
        else:
            hash_ = hash(state)
            if (emoji is not None):
                hash_ ^=emoji.id
        
        return hash_
    
    @property
    def name(self):
        """
        Returns the activity's display text.
        
        Returns
        -------
        name : `str`
        """
        state = self.state
        emoji = self.emoji
        if (state is None):
            if (emoji is None):
                name = ''
            else:
                name = emoji.as_emoji
        else:
            if (emoji is None):
                name = state
            else:
                name = f'{emoji.as_emoji} {state}'
        
        return name
    
    def _update_attributes(self, activity_data):
        """
        Updates the activity by overwriting it's old attributes.
        
        Parameters
        ----------
        activity_data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        """
        self.state = activity_data.get('state', None)
        
        emoji_data = activity_data.get('emoji', None)
        if emoji_data is None:
            emoji = None
        else:
            emoji = create_partial_emoji_from_data(emoji_data)
        self.emoji = emoji
        
        created_at = activity_data.get('created_at', None)
        if created_at is None:
            created_at = DISCORD_EPOCH_START
        else:
            created_at = unix_time_to_datetime(created_at)
        self.created_at = created_at
    
    def _difference_update_attributes(self, activity_data):
        """
        Updates the activity and returns the changes in a `dict` of (`attribute-name`, `old-value`) items.
        
        Parameters
        ----------
        activity_data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        
        Returns
        -------
        changes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
            The returned items might be the following:
            
            +---------------+-----------------------+
            | key           | value                 |
            +===============+=======================+
            | created_at    | `datetime`            |
            +---------------+-----------------------+
            | emoji         | `None` or ``Emoji``   |
            +---------------+-----------------------+
            | state         | `None` or `str`       |
            +---------------+-----------------------+
        """
        old_attributes = {}
        
        state = activity_data.get('state', None)
        if self.state != state:
            old_attributes['state'] = self.state
            self.state = state
        
        emoji_data = activity_data.get('emoji', None)
        if emoji_data is None:
            emoji = None
        else:
            emoji = create_partial_emoji_from_data(emoji_data)
        
        if self.emoji != emoji:
            old_attributes['emoji'] = self.emoji
            self.emoji = emoji
        
        created_at = activity_data.get('created_at', None)
        if created_at is None:
            created_at = DISCORD_EPOCH_START
        else:
            created_at = unix_time_to_datetime(created_at)
        if self.created_at != created_at:
            old_attributes['created_at'] = self.created_at
            self.created_at = created_at
        
        return old_attributes
    
    def full_dict(self):
        """
        Converts the whole activity to a dictionary.
        
        Returns
        -------
        activity_data : `dict` of (`str`, `Any`) items
        """
        activity_data = {
            'name': 'Custom Status',
            'id': 'custom',
        }
        
        emoji = self.emoji
        if (emoji is not None):
            emoji_data = {}
            if emoji.is_custom_emoji():
                emoji_data['name'] = emoji.name
                emoji_data['id'] = emoji.id
                if emoji.animated:
                    emoji_data['animated'] = True
            else:
                emoji_data['name'] = emoji.unicode
            
            activity_data['emoji']=emoji_data
        
        state = self.state
        if (state is not None):
            activity_data['state'] = state
        
        created_at = self.created_at
        if created_at != DISCORD_EPOCH_START:
            activity_data['created_at'] = datetime_to_unix_time(created_at)
        
        return activity_data

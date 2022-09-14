__all__ = ('ActivityMetadataCustom',)


from scarletio import copy_docs, include

from ...utils import DATETIME_FORMAT_CODE, DISCORD_EPOCH_START, datetime_to_millisecond_unix_time, millisecond_unix_time_to_datetime

from .base import ActivityMetadataBase


create_partial_emoji_data = include('create_partial_emoji_data')
create_partial_emoji_from_data = include('create_partial_emoji_from_data')


class ActivityMetadataCustom(ActivityMetadataBase):
    """
    Represents a Discord custom activity.
    
    Attributes
    ----------
    created_at : `None`, `datetime`
        When the status was created.
    emoji : `None`, ``Emoji``
        The emoji of the activity. If it has no emoji, then set as `None`.
    state : `None`, `str`
        The activity's text under it's emoji. Defaults to `None`.
    """
    __slots__ = ('created_at', 'emoji', 'state', )
    
    @copy_docs(ActivityMetadataBase.__new__)
    def __new__(cls, keyword_parameters):
        self = object.__new__(cls)
        self.created_at = None
        self.emoji = None
        self.state = None
        return self
    
    
    @copy_docs(ActivityMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # created_at
        created_at = self.created_at
        if (created_at is not None):
            repr_parts.append(' created_at=')
            repr_parts.append(format(created_at, DATETIME_FORMAT_CODE))
            
            field_added = True
        else:
            field_added = False
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' emoji=')
            repr_parts.append(repr(emoji))
        
        # state
        state = self.state
        if (state is not None):
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' state=')
            repr_parts.append(repr(state))
        
        return ''.join(repr_parts)
    
    
    @copy_docs(ActivityMetadataBase.__hash__)
    def __hash__(self):
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
    
    
    @copy_docs(ActivityMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # created_at
        if self.created_at != other.created_at:
            return False
        
        # emoji
        if self.emoji != other.emoji:
            return False
        
        # state
        if self.state != other.state:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ActivityMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self._update_attributes(data)
        return self
    
    
    @copy_docs(ActivityMetadataBase.to_data)
    def to_data(self, *, include_internals=False, user=False):
        data = {}
        
        if include_internals:
            data['name'] = 'Custom Status'
            
            # created_at
            created_at = self.created_at
            if (created_at is not None):
                data['created_at'] = datetime_to_millisecond_unix_time(created_at)
            
            # emoji
            emoji = self.emoji
            if (emoji is not None):
                data['emoji'] = create_partial_emoji_data(emoji)
            
            # state
            state = self.state
            if (state is not None):
                data['state'] = state
        
        return data
    
    
    @copy_docs(ActivityMetadataBase._update_attributes)
    def _update_attributes(self, data):
        self.state = data.get('state', None)
        
        emoji_data = data.get('emoji', None)
        if emoji_data is None:
            emoji = None
        else:
            emoji = create_partial_emoji_from_data(emoji_data)
        self.emoji = emoji
        
        created_at = data.get('created_at', None)
        if (created_at is not None):
            created_at = millisecond_unix_time_to_datetime(created_at)
        self.created_at = created_at
    
    
    @copy_docs(ActivityMetadataBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = {}
        
        state = data.get('state', None)
        if self.state != state:
            old_attributes['state'] = self.state
            self.state = state
        
        emoji_data = data.get('emoji', None)
        if emoji_data is None:
            emoji = None
        else:
            emoji = create_partial_emoji_from_data(emoji_data)
        
        if self.emoji != emoji:
            old_attributes['emoji'] = self.emoji
            self.emoji = emoji
        
        created_at = data.get('created_at', None)
        if created_at is None:
            created_at = DISCORD_EPOCH_START
        else:
            created_at = millisecond_unix_time_to_datetime(created_at)
        if self.created_at != created_at:
            old_attributes['created_at'] = self.created_at
            self.created_at = created_at
        
        return old_attributes
    
    
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

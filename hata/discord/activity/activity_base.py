__all__ = ('ActivityAssets', 'ActivityBase', 'ActivityParty', 'ActivitySecrets', 'ActivityTimestamps',
    'ACTIVITY_TYPES',)

from datetime import datetime

from ..utils import DISCORD_EPOCH_START
from ..color import Color

from . import activity_types as ACTIVITY_TYPES

DEFAULT_CUSTOM_ID = 'UNKNOWN'

CUSTOM_IDS = {
    ACTIVITY_TYPES.spotify: 'spotify:1',
    ACTIVITY_TYPES.custom: 'custom',
}

ACTIVITY_TYPE_NAMES = {
    ACTIVITY_TYPES.game: 'game',
    ACTIVITY_TYPES.stream: 'stream',
    ACTIVITY_TYPES.spotify: 'spotify',
    ACTIVITY_TYPES.watching: 'watching',
    ACTIVITY_TYPES.custom: 'custom',
    ACTIVITY_TYPES.competing: 'competing',
}


class ActivityTimestamps:
    """
    Represents an activity's timestamp field.
    
    Attributes
    ----------
    end : `int`
        The time when the activity ends as Unix time in milliseconds. Defaults to `0`.
    start : `int`
        The time when the activity starts as Unix time in milliseconds. Defaults to `0`.
    """
    __slots__ = ('end', 'start',)
    
    def __init__(self, timestamps_data):
        """
        Creates a new activity timestamp object from the given data.
        
        Parameters
        ----------
        timestamps_data : `dict` of (`str`, `Any`) items
            Activity timestamp data.
        """
        self.start = timestamps_data.get('start', 0)
        self.end = timestamps_data.get('end', 0)
    
    
    def __repr__(self):
        """Returns the activity timestamp's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        start = self.start
        if start:
            repr_parts.append(' start=')
            repr_parts.append(repr(start))
            field_added = True
        else:
            field_added = False
        
        end = self.end
        if end:
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' end=')
            repr_parts.append(repr(start))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two activity timestamps are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.start != other.start:
            return False
        
        if self.end != other.end:
            return False
        
        return True
    
    
    def to_data(self):
        """
        Serializes the activity timestamp.
        
        Returns
        -------
        timestamps_data : `dict` of (`str`, `Any`) items
        """
        timestamps_data = {}
        
        start = self.start
        if start:
            timestamps_data['start'] = start
        
        end = self.end
        if end:
            timestamps_data['end'] = end
        
        return timestamps_data


class ActivityAssets:
    """
    Represents a discord activity asset.
    
    Attributes
    ----------
    image_large : `None` or `str`
        The id of the activity's large asset to display. Defaults to `None`.
    image_small : `None` or `str`
        The id of the activity's small asset to display. Defaults to `None`.
    text_large : `None` or `str`
        The hover text of the large asset. Defaults to `None`.
    text_small : `None` or `str`
        The hover text of the small asset. Defaults to `None`.
    """
    __slots__ = ('image_large', 'image_small', 'text_large', 'text_small',)
    def __init__(self, assets_data):
        """
        Creates a new activity asset object from the given data.
        
        Parameters
        ----------
        assets_data : `dict` of (`str`, `Any`) items
            Activity asset data.
        """
        self.image_large = assets_data.get('large_image', None)
        self.image_small = assets_data.get('small_image', None)
        self.text_large = assets_data.get('large_text', None)
        self.text_small = assets_data.get('small_text', None)
    
    
    def __repr__(self):
        """Returns the activity asset's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        image_large = self.image_large
        if (image_large is not None):
            repr_parts.append(' image_large=')
            repr_parts.append(repr(image_large))
            field_added = True
        else:
            field_added = False
        
        image_small = self.image_small
        if (image_small is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            repr_parts.append(' image_small=')
            repr_parts.append(repr(image_small))
        
        text_large = self.text_large
        if (text_large is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            repr_parts.append(' text_large=')
            repr_parts.append(repr(text_large))
        
        text_small = self.text_small
        if (text_small is not None):
            if field_added:
                repr_parts.append(',')
            repr_parts.append(' text_small=')
            repr_parts.append(repr(text_small))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two activity assets are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.image_large != other.image_large:
            return False
        
        if self.image_small != other.image_small:
            return False
        
        if self.text_large != other.text_large:
            return False
        
        if self.text_small != other.text_small:
            return False
        
        return True
    
    
    def to_data(self):
        """
        Serializes the activity asset.
        
        Returns
        -------
        timestamp_data : `dict` of (`str`, `Any`) items
        """
        assets_data = {}
        
        image_large = self.image_large
        if (image_large is not None):
            assets_data['large_image'] = image_large
        
        image_small = self.image_small
        if (image_small is not None):
            assets_data['small_image'] = image_small
        
        text_large = self.text_large
        if (text_large is not None):
            assets_data['large_text'] = text_large
        
        text_small = self.text_small
        if (text_small is not None):
            assets_data['small_text'] = text_small
        
        return assets_data


class ActivityParty:
    """
    Represents a discord activity party.
    
    Attributes
    ----------
    id : `None` or `str`
        The party's id, which in the player is. Defaults to `None`.
    size : `int`
        The party's maximal size, which in the player is. Defaults to `0`.
    max : `int`
        The party's actual size, which in the player is. Defaults to `0`.
    """
    __slots__ = ('id', 'size', 'max',)
    def __init__(self, party_data):
        """
        Creates a new activity party object from the given data.
        
        Parameters
        ----------
        party_data : `dict` of (`str`, `Any`) items
            Activity party data.
        """
        self.id = party_data.get('id', None)
        
        try:
            size, max_ = party_data['size']
        except KeyError:
            size = 0
            max_ = 0
        
        self.size = size
        self.max = max_
    
    def __repr__(self):
        """Returns the activity party's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        id_ = self.id
        if (id is not None):
            repr_parts.append(' id_=')
            repr_parts.append(repr(id_))
            field_added = True
        else:
            field_added = False
        
        size = self.size
        max_ = self.max
        if size or max_:
            if field_added:
                repr_parts.append(',')
            repr_parts.append(' size=')
            repr_parts.append(repr(size))
            repr_parts.append(', max=')
            repr_parts.append(repr(max_))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    def __eq__(self, other):
        """Returns whether the two activity parties are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.id != other.id:
            return False
        
        if self.size != other.size:
            return False
        
        if self.max != other.max:
            return False
        
        return True
    
    def to_data(self):
        """
        Serializes the activity party.
        
        Returns
        -------
        timestamp_data : `dict` of (`str`, `Any`) items
        """
        party_data = {}
        
        id_ = self.id
        if (id_ is not None):
            party_data['id'] = id_
        
        size = self.size
        max_ = self.max
        if size or max_:
            party_data['size'] = [size, max_]
        
        return party_data


class ActivitySecrets:
    """
    Represents and activity secret.
    
    Attributes
    ----------
    join : `None` or `str`
        Unique hash given for the match context. Defaults to `None`.
    match : `None` or `str`
        Unique hash for spectate button. Defaults to `None`.
    spectate : `None` or `str`
        Unique hash for chat invites and ask to join. Defaults to `None`.
    """
    __slots__ = ('join', 'match', 'spectate', )
    def __init__(self, secrets_data):
        """
        Creates a new activity secret object from the given data.
        
        Parameters
        ----------
        secrets_data : `dict` of (`str`, `Any`) items
            Activity secret data.
        """
        self.join = secrets_data.get('join', None)
        self.spectate = secrets_data.get('spectate', None)
        self.match = secrets_data.get('match', None)
    
    def __repr__(self):
        """Returns the activity secret's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        join = self.join
        if (join is not None):
            repr_parts.append(' join=')
            repr_parts.append(repr(join))
            field_added = True
        else:
            field_added = False
        
        spectate = self.spectate
        if (spectate is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            repr_parts.append(' spectate=')
            repr_parts.append(repr(spectate))
        
        match = self.match
        if (match is not None):
            if field_added:
                repr_parts.append(',')
            repr_parts.append(' match=')
            repr_parts.append(repr(match))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    def __eq__(self, other):
        """Returns whether the two activity secrets are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.join != other.join:
            return False
        
        if self.spectate != other.spectate:
            return False
        
        if self.match != other.match:
            return False
        
        return True
    
    def to_data(self):
        """
        Serializes the activity secret.
        
        Returns
        -------
        timestamp_data : `dict` of (`str`, `Any`) items
        """
        secrets_data = {}
        
        join = self.join
        if (join is not None):
            secrets_data['join'] = join
        
        spectate = self.spectate
        if (spectate is not None):
            secrets_data['spectate'] = spectate
        
        match = self.match
        if (match is not None):
            secrets_data['match'] = match
        
        return secrets_data


class ActivityBase:
    """
    Base class for activities.
    
    Class Attributes
    ----------------
    created : `int` = `0`
        When the activity was created as Unix time in milliseconds.
    name : `str` = `'Unknown'`
        The activity's name. Subclasses might overwrite it as member descriptor.
    id : `int` = `0`
        The activity's id. Subclasses might overwrite it as member descriptor.
    type : `int` = `127`
        The activity's type value.
    """
    name = 'Unknown'
    id = 0
    type = 127
    created = 0
    
    __slots__ = ()
    def __new__(cls, data):
        """
        Creates a new activity. Neither ``ActivityBase`` or it's subclass: ``ActivityUnknown`` cannot be instanced and
        raises `RuntimeError`.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Activity data received from Discord.
        
        Raises
        ------
        RuntimeError
        """
        raise RuntimeError(f'{cls.__name__} cannot be instanced.')
    
    def __str__(self):
        """Returns the activity's name."""
        return self.name
    
    def __repr__(self):
        """Returns the activity's representation."""
        return f'<{self.__class__.__name__} name={self.name!r}>'
    
    def __hash__(self):
        """Returns the activity's hash value."""
        return self.id
    
    def __eq__(self, other):
        """
        Returns whether the two activities are equal.
        
        Subclasses should overwrite it.
        """
        return NotImplemented
    
    @property
    def color(self):
        """
        Returns the activity's color.
        
        Subclasses should overwrite it.
        
        Returns
        -------
        color : ``Color``
        """
        return Color()
    
    
    @property
    def discord_side_id(self):
        """
        Returns the activity's Discord side id. If the activity implements id returns that, else returns it's
        `CUSTOM_ID` class attribute.
        
        Returns
        -------
        activity_id : `str`
        """
        id_ = self.id
        if id_:
            activity_id = self.id.__format__('x')
        else:
            activity_id = CUSTOM_IDS.get(self.type, DEFAULT_CUSTOM_ID)
        
        return activity_id
    
    @property
    def created_at(self):
        """
        When the activity was created. If the creation time was not included, then returns the discord's epoch's start.
        
        Returns
        -------
        created_at : `datetime`
        """
        created = self.created
        if created == 0:
            return DISCORD_EPOCH_START
        
        return datetime.utcfromtimestamp(created/1000.)
    
    @classmethod
    def from_data(cls, activity_data):
        """
        Creates a new activity instance from the given activity data.
        
        Subclasses should overwrite this method.
        
        Parameters
        ----------
        activity_data : `dict` of (`str`, `Any`) items
            Received activity data.
        
        Returns
        -------
        activity : `None`
        """
        return None
    
    def _update(self, data):
        """
        Updates the activity and returns the changes in a `dict` of (`attribute-name`, `old-value`) items.
        
        Subclasses should overwrite this method.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        
        Returns
        -------
        old_attributes : `dict`
            Always empty.
        """
        return {}
    
    def _update_no_return(self, data):
        """
        Updates the activity by overwriting it's old attributes.
        
        Subclasses should overwrite this method.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        """
        pass
    
    def bot_dict(self):
        """
        Converts the activity to json serializable dictionary, which can be sent with bot account to change activity.
        
        Subclasses, which implement it, should overwrite.
        
        Returns
        -------
        activity_data : `dict` of (`str`, `Any`) items
        """
        return {}
    
    def user_dict(self):
        """
        Converts the activity to json serializable dictionary, which can (?) be sent with user account to change
        activity.
        
        Subclasses, which implement it, should overwrite.
        
        Returns
        -------
        activity_data : `dict` of (`str`, `Any`) items
        """
        return {}
    
    def full_dict(self):
        """
        Converts the whole activity to a dictionary.
        
        Subclasses, which implement it, should overwrite.
        
        Returns
        -------
        activity_data : `dict` of (`str`, `Any`) items
        """
        return {}

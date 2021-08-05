__all__ = ('ActivityAssets', 'ActivityBase', 'ActivityParty', 'ActivitySecrets', 'ActivityTimestamps',
    'ACTIVITY_TYPES',)

from datetime import datetime

from ..utils import DISCORD_EPOCH_START, DATETIME_FORMAT_CODE, unix_time_to_datetime, datetime_to_unix_time
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
    end : `None` or `datetime`
        When the activity. Defaults to `None`.
    start : `None` or `datetime`
       When the activity starts. Defaults to `None`.
    """
    __slots__ = ('end', 'start',)
    
    def __new__(cls, *, start=None, end=None):
        """
        Creates a new activity timestamp with the given parameters.
        
        Parameters
        ----------
        end : `None` or `datetime`, Optional (Keyword only)
            When the activity. Defaults to `None`.
        start : `None` or `datetime`, Optional (Keyword only)
           When the activity starts. Defaults to `None`.
        
        Raises
        ------
        AssertionError
            - If `start` is nether `None` nor `datetime`.
            - If `end` is neither `None` nor `datetime`.
        """
        if __debug__:
            if (start is not None) and (not isinstance(start, datetime)):
                raise AssertionError(f'`start` can be either `None` or `datetime`, got {start.__class__.__name__}.')

            if (end is not None) and (not isinstance(end, datetime)):
                raise AssertionError(f'`end` can be either `None` or `datetime`, got {end.__class__.__name__}.')
        
        self = object.__new__(cls)
        self.start = start
        self.end = end
        return self
    
    
    @classmethod
    def from_data(cls, timestamps_data):
        """
        Creates a new activity timestamp object from the given data.
        
        Parameters
        ----------
        timestamps_data : `dict` of (`str`, `Any`) items
            Activity timestamp data.
        """
        start = timestamps_data.get('start', None)
        if (start is not None):
            start = unix_time_to_datetime(start)
        
        end = timestamps_data.get('end', None)
        if (end is not None):
            end = unix_time_to_datetime(end)
        
        self = object.__new__(cls)
        self.start = start
        self.end = end
        return self
    
    
    def __repr__(self):
        """Returns the activity timestamp's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        start = self.start
        if (start is not None):
            repr_parts.append(' start=')
            repr_parts.append(start.__format__(DATETIME_FORMAT_CODE))
            field_added = True
        else:
            field_added = False
        
        end = self.end
        if (end is not None):
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' end=')
            repr_parts.append(start.__format__(DATETIME_FORMAT_CODE))
        
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
        if (start is not None):
            timestamps_data['start'] = datetime_to_unix_time(start)
        
        end = self.end
        if (end is not None):
            timestamps_data['end'] = datetime_to_unix_time(end)
        
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
    
    def __new__(cls, *, image_large=None, image_small=None, text_large=None, text_small=None):
        """
        Creates a new ``ActivityAssets`` instance from the given parameters.
        
        Parameters
        ----------
        image_large : `None` or `str`, Optional (Keyword only)
            The id of the activity's large asset to display. Defaults to `None`.
        image_small : `None` or `str`, Optional (Keyword only)
            The id of the activity's small asset to display. Defaults to `None`.
        text_large : `None` or `str`, Optional (Keyword only)
            The hover text of the large asset. Defaults to `None`.
        text_small : `None` or `str`, Optional (Keyword only)
            The hover text of the small asset. Defaults to `None`.
        
        Raises
        ------
        AssertionError
            - If `image_large` is neither `None` nor `str`.
            - If `image_small` is neither `None` nor `str`.
            - If `text_large` is neither `None` nor `str`.
            - If `text_small` is neither `None` nor `str`.
        """
        if (image_large is not None):
            if __debug__:
                if (not isinstance(image_large, str)):
                    raise AssertionError(f'`image_large` can be either `None` or `str`, got '
                        f'{image_large.__class__.__name__}.')
            
            if (not image_large):
                image_large = None
            
            
        if (image_small is not None):
            if __debug__:
                if (not isinstance(image_small, str)):
                    raise AssertionError(f'`image_small` can be either `None` or `str`, got '
                        f'{image_small.__class__.__name__}.')
            
            if (not image_small):
                image_small = None
            
        
        if (text_large is not None):
            if __debug__:
                if (not isinstance(text_large, str)):
                    raise AssertionError(f'`text_large` can be either `None` or `str`, got '
                        f'{text_large.__class__.__name__}.')
            
            if (not text_large):
                text_large = None
        
        if (text_small is not None):
            if __debug__:
                if (not isinstance(text_small, str)):
                    raise AssertionError(f'`image_large` can be either `None` or `str`, got '
                        f'{text_small.__class__.__name__}.')
            
            if (not text_small):
                text_small = None
        
        self = object.__new__(cls)
        self.image_large = image_large
        self.image_small = image_small
        self.text_large = text_large
        self.text_small = text_small
        return self
    
    @classmethod
    def from_data(cls, assets_data):
        """
        Creates a new activity asset object from the given data.
        
        Parameters
        ----------
        assets_data : `dict` of (`str`, `Any`) items
            Activity asset data.
        """
        self = object.__new__(cls)
        self.image_large = assets_data.get('large_image', None)
        self.image_small = assets_data.get('small_image', None)
        self.text_large = assets_data.get('large_text', None)
        self.text_small = assets_data.get('small_text', None)
        return self
    
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
    
    def __new__(cls, *, id_=None, size=0, max_=0):
        """
        Creates a new activity party instance form the given parameters.
        
        Parameters
        ----------
        id_ : `None` or `str`, Optional (Keyword only)
            The party's id, which in the player is. Defaults to `None`.
        size : `int`, Optional (Keyword only)
            The party's maximal size, which in the player is. Defaults to `0`.
        max_ : `int`, Optional (Keyword only)
            The party's actual size, which in the player is. Defaults to `0`.
        
        Raises
        ------
        AssertionError
            - If `id_` is neither `None` nor `str` instance.
            - if `size` is not `int` instance.
            - If `max_` is not `int` instance.
            - If `size` is negative`.
            - If `max_` is negative.
        """
        if (id_ is not None):
            if __debug__:
                if (not isinstance(id_, int)):
                    raise AssertionError(f'`id_` can be either `None` or `str`, got {id_.__class__.__name__}.')
            
            if (not id_):
                id_ = None
        
        if __debug__:
            if (not isinstance(size, int)):
                raise AssertionError(f'`size` can be `int` instance, got {size.__class__.__name__}.')
            
            if (not isinstance(max_, int)):
                raise AssertionError(f'`max_` can be `int` instance, got {max_.__class__.__name__}.')
            
            if (size < 0):
                raise AssertionError(f'`size` cannot be negative, got {size!r}.')
            
            if (max_ < 0):
                raise AssertionError(f'`max_` cannot be negative, got {max_!r}.')
        
        self = object.__new__(cls)
        self.id = id_
        self.size = size
        self.max = max_
        return self
    
    
    @classmethod
    def from_data(cls, party_data):
        """
        Creates a new activity party object from the given data.
        
        Parameters
        ----------
        party_data : `dict` of (`str`, `Any`) items
            Activity party data.
        """
        
        self = object.__new__(cls)
        self.id = party_data.get('id', None)
        
        try:
            size, max_ = party_data['size']
        except KeyError:
            size = 0
            max_ = 0
        
        self.size = size
        self.max = max_
        return self
    
    def __repr__(self):
        """Returns the activity party's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        id_ = self.id
        if (id_ is not None):
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
    
    def __new__(cls, *, join=None, match=None, spectate=None):
        """
        Creates a new activity secret from the given parameters.
        
        Parameters
        ----------
        join : `None` or `str`, Optional (Keyword only)
            Unique hash given for the match context. Defaults to `None`.
        match : `None` or `str`, Optional (Keyword only)
            Unique hash for spectate button. Defaults to `None`.
        spectate : `None` or `str`, Optional (Keyword only)
            Unique hash for chat invites and ask to join. Defaults to `None`.
        """
        if (join is not None):
            if __debug__:
                if (not isinstance(join, str)):
                    raise AssertionError(f'`join` can be either `None` or `str`, got {join.__class__.__name__}.')
            
            if (not join):
                join = None
            
            
        if (match is not None):
            if __debug__:
                if (not isinstance(match, str)):
                    raise AssertionError(f'`match` can be either `None` or `str`, got {match.__class__.__name__}.')
            
            if (not match):
                match = None
            
        
        if (spectate is not None):
            if __debug__:
                if (not isinstance(spectate, str)):
                    raise AssertionError(f'`spectate` can be either `None` or `str`, got {spectate.__class__.__name__}.')
            
            if (not spectate):
                spectate = None
        
        self = object.__new__(cls)
        self.join = join
        self.match = match
        self.spectate = spectate
        return self
    
    @classmethod
    def from_data(cls, secrets_data):
        """
        Creates a new activity secret object from the given data.
        
        Parameters
        ----------
        secrets_data : `dict` of (`str`, `Any`) items
            Activity secret data.
        """
        self = object.__new__(cls)
        self.join = secrets_data.get('join', None)
        self.spectate = secrets_data.get('spectate', None)
        self.match = secrets_data.get('match', None)
        return self
    
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
    created_at : `datetime`
        When the activity was created. Defaults to Discord epoch.
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
    created_at = DISCORD_EPOCH_START
    
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
        return DISCORD_EPOCH_START
    
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
    
    def _difference_update_attributes(self, data):
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
    
    def _update_attributes(self, data):
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

__all__ = (
    'ActivityAssets', 'ActivityBase', 'ActivityParty', 'ActivitySecrets', 'ActivityTimestamps', 'ACTIVITY_TYPES'
)

from datetime import datetime

from scarletio import RichAttributeErrorBaseType, copy_docs

from ..color import Color
from ..utils import DATETIME_FORMAT_CODE, DISCORD_EPOCH_START, datetime_to_unix_time, unix_time_to_datetime

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


ACTIVITY_TYPE_NAME_UNKNOWN = 'unknown'

def get_activity_type_name(type_value):
    """
    Returns the activity'sn ame for the given type value.
    
    Parameters
    ----------
    type_value : `int`
        The activity's type's value.
    
    Returns
    -------
    activity_type_name : `str`
    """
    return ACTIVITY_TYPE_NAMES.get(type_value, ACTIVITY_TYPE_NAME_UNKNOWN)


class ActivityFieldBase(RichAttributeErrorBaseType):
    """
    Base class for activity fields.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new activity field.
        """
        return object.__new__(cls)
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new activity field from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Activity field data.
        """
        return object.__new__(cls)
    
    
    def to_data(self):
        """
        Serializes the activity field.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        return {}
    
    
    def __repr__(self):
        """Returns the activity field's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    def __eq__(self, other):
        """Returns whether the two activity fields are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return True
    
    
    def __hash__(self):
        """Returns the activity field's hash value."""
        return 0
    
    
    def __bool__(self):
        """Returns whether the activity field has any non-default attribute set."""
        return False


class ActivityTimestamps(ActivityFieldBase):
    """
    Represents an activity's timestamp field.
    
    Attributes
    ----------
    end : `None`, `datetime`
        When the activity. Defaults to `None`.
    start : `None`, `datetime`
       When the activity starts. Defaults to `None`.
    """
    __slots__ = ('end', 'start',)
    
    def __new__(cls, *, start=None, end=None):
        """
        Creates a new activity timestamp with the given parameters.
        
        Parameters
        ----------
        end : `None`, `datetime` = `None`, Optional (Keyword only)
            When the activity. Defaults to `None`.
        start : `None`, `datetime` = `None`, Optional (Keyword only)
           When the activity starts. Defaults to `None`.
        
        Raises
        ------
        AssertionError
            - If `start` is nether `None` nor `datetime`.
            - If `end` is neither `None` nor `datetime`.
        """
        if __debug__:
            if (start is not None) and (not isinstance(start, datetime)):
                raise AssertionError(
                    f'`start` can be `None`, `datetime`, got {start.__class__.__name__}; {start!r}.'
                )

            if (end is not None) and (not isinstance(end, datetime)):
                raise AssertionError(
                    f'`end` can be `None`, `datetime`, got {end.__class__.__name__}; {end!r}.'
                )
        
        self = object.__new__(cls)
        self.start = start
        self.end = end
        return self
    
    
    @classmethod
    @copy_docs(ActivityFieldBase.from_data)
    def from_data(cls, timestamps_data):
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
    
    
    @copy_docs(ActivityFieldBase.to_data)
    def to_data(self):
        timestamps_data = {}
        
        start = self.start
        if (start is not None):
            timestamps_data['start'] = datetime_to_unix_time(start)
        
        end = self.end
        if (end is not None):
            timestamps_data['end'] = datetime_to_unix_time(end)
        
        return timestamps_data
    
    
    
    @copy_docs(ActivityFieldBase.__repr__)
    def __repr__(self):
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
    
    
    @copy_docs(ActivityFieldBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.start != other.start:
            return False
        
        if self.end != other.end:
            return False
        
        return True
    
    
    @copy_docs(ActivityFieldBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        start = self.start
        if (start is not None):
            hash_value ^= hash(start)
            hash_value ^= (1 << 0)
        
        end = self.end
        if (end is not None):
            hash_value ^= hash(end)
            hash_value ^= (1 << 4)
        
        return hash_value


    @copy_docs(ActivityFieldBase.__bool__)
    def __bool__(self):
        start = self.start
        if (start is not None):
            return True
        
        end = self.end
        if (end is not None):
            return True
        
        return False


class ActivityAssets(ActivityFieldBase):
    """
    Represents a discord activity asset.
    
    Attributes
    ----------
    image_large : `None`, `str`
        The id of the activity's large asset to display. Defaults to `None`.
    image_small : `None`, `str`
        The id of the activity's small asset to display. Defaults to `None`.
    text_large : `None`, `str`
        The hover text of the large asset. Defaults to `None`.
    text_small : `None`, `str`
        The hover text of the small asset. Defaults to `None`.
    """
    __slots__ = ('image_large', 'image_small', 'text_large', 'text_small',)
    
    def __new__(cls, *, image_large=None, image_small=None, text_large=None, text_small=None):
        """
        Creates a new ``ActivityAssets`` from the given parameters.
        
        Parameters
        ----------
        image_large : `None`, `str` = `None`, Optional (Keyword only)
            The id of the activity's large asset to display. Defaults to `None`.
        image_small : `None`, `str` = `None`, Optional (Keyword only)
            The id of the activity's small asset to display. Defaults to `None`.
        text_large : `None`, `str` = `None`, Optional (Keyword only)
            The hover text of the large asset. Defaults to `None`.
        text_small : `None`, `str` = `None`, Optional (Keyword only)
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
                    raise AssertionError(
                        f'`image_large` can be `None`, `str`, got {image_large.__class__.__name__}; '
                        f'{image_large!r}.'
                    )
            
            if (not image_large):
                image_large = None
            
            
        if (image_small is not None):
            if __debug__:
                if (not isinstance(image_small, str)):
                    raise AssertionError(
                        f'`image_small` can be `None`, `str`, got {image_small.__class__.__name__}; '
                        f'{image_small!r}.'
                    )
            
            if (not image_small):
                image_small = None
            
        
        if (text_large is not None):
            if __debug__:
                if (not isinstance(text_large, str)):
                    raise AssertionError(
                        f'`text_large` can be `None`, `str`, got {text_large.__class__.__name__}; '
                        f'{text_large!r}.'
                    )
            
            if (not text_large):
                text_large = None
        
        if (text_small is not None):
            if __debug__:
                if (not isinstance(text_small, str)):
                    raise AssertionError(
                        f'`image_large` can be `None`, `str`, got {text_small.__class__.__name__}; '
                        f'{text_small!r}.'
                    )
            
            if (not text_small):
                text_small = None
        
        self = object.__new__(cls)
        self.image_large = image_large
        self.image_small = image_small
        self.text_large = text_large
        self.text_small = text_small
        return self
    
    
    @classmethod
    @copy_docs(ActivityFieldBase.from_data)
    def from_data(cls, assets_data):
        self = object.__new__(cls)
        self.image_large = assets_data.get('large_image', None)
        self.image_small = assets_data.get('small_image', None)
        self.text_large = assets_data.get('large_text', None)
        self.text_small = assets_data.get('small_text', None)
        return self
    
    
    @copy_docs(ActivityFieldBase.to_data)
    def to_data(self):
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
    
    
    @copy_docs(ActivityFieldBase.__repr__)
    def __repr__(self):
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
    
    
    @copy_docs(ActivityFieldBase.__eq__)
    def __eq__(self, other):
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
    
    
    @copy_docs(ActivityFieldBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        image_large = self.image_large
        if (image_large is not None):
            hash_value ^= hash(image_large)
            hash_value ^= (1 << 0)
        
        image_small = self.image_small
        if (image_small is not None):
            hash_value ^= hash(image_small)
            hash_value ^= (1 << 4)
        
        text_large = self.text_large
        if (text_large is not None):
            hash_value ^= hash(text_large)
            hash_value ^= (1 << 8)
        
        text_small = self.text_small
        if (text_small is not None):
            hash_value ^= hash(text_small)
            hash_value ^= (1 << 12)
        
        return hash_value
    
    
    @copy_docs(ActivityFieldBase.__bool__)
    def __bool__(self):
        image_large = self.image_large
        if (image_large is not None):
            return True
        
        image_small = self.image_small
        if (image_small is not None):
            return True
        
        text_large = self.text_large
        if (text_large is not None):
            return True
        
        text_small = self.text_small
        if (text_small is not None):
            return True
        
        return False


class ActivityParty(ActivityFieldBase):
    """
    Represents a discord activity party.
    
    Attributes
    ----------
    id : `None`, `str`
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
        id_ : `None` = `None`, `str`, Optional (Keyword only)
            The party's id, which in the player is. Defaults to `None`.
        size : `int` = `0`, Optional (Keyword only)
            The party's maximal size, which in the player is. Defaults to `0`.
        max_ : `int` = `0`, Optional (Keyword only)
            The party's actual size, which in the player is. Defaults to `0`.
        
        Raises
        ------
        AssertionError
            - If `id_` is neither `None` nor `str`.
            - if `size` is not `int`.
            - If `max_` is not `int`.
            - If `size` is negative`.
            - If `max_` is negative.
        """
        if (id_ is not None):
            if __debug__:
                if (not isinstance(id_, int)):
                    raise AssertionError(
                        f'`id_` can be `None`, `str`, got {id_.__class__.__name__}; {id_!r}.'
                    )
            
            if (not id_):
                id_ = None
        
        if __debug__:
            if (not isinstance(size, int)):
                raise AssertionError(
                    f'`size` can be `int`, got {size.__class__.__name__}; {size!r}.'
                )
            
            if (not isinstance(max_, int)):
                raise AssertionError(
                    f'`max_` can be `int`, got {max_.__class__.__name__}; {max_!r}.'
                )
            
            if (size < 0):
                raise AssertionError(
                    f'`size` cannot be negative, got {size!r}.'
                )
            
            if (max_ < 0):
                raise AssertionError(
                    f'`max_` cannot be negative, got {max_!r}.'
                )
        
        self = object.__new__(cls)
        self.id = id_
        self.size = size
        self.max = max_
        return self
    
    
    @classmethod
    @copy_docs(ActivityFieldBase.from_data)
    def from_data(cls, party_data):
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
    
    
    @copy_docs(ActivityFieldBase.to_data)
    def to_data(self):
        party_data = {}
        
        id_ = self.id
        if (id_ is not None):
            party_data['id'] = id_
        
        size = self.size
        max_ = self.max
        if size or max_:
            party_data['size'] = [size, max_]
        
        return party_data
    
    
    @copy_docs(ActivityFieldBase.__repr__)
    def __repr__(self):
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
    
    
    @copy_docs(ActivityFieldBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.id != other.id:
            return False
        
        if self.size != other.size:
            return False
        
        if self.max != other.max:
            return False
        
        return True
    

    @copy_docs(ActivityFieldBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        id_ = self.id
        if (id_ is not None):
            hash_value ^= hash(id_)
            hash_value ^= (1 << 0)
        
        size = self.size
        if size:
            hash_value ^= hash(size)
            hash_value ^= (1 << 4)
        
        max_ = self.max
        if max_:
            hash_value ^= hash(max_)
            hash_value ^= (1 << 8)
        
        return hash_value
    
    
    @copy_docs(ActivityFieldBase.__bool__)
    def __bool__(self):
        id_ = self.id
        if (id_ is not None):
            return True
        
        size = self.size
        if size:
            return True
        
        max_ = self.max
        if max_:
            return True
        
        return False


class ActivitySecrets(ActivityFieldBase):
    """
    Represents and activity secret.
    
    Attributes
    ----------
    join : `None`, `str`
        Unique hash given for the match context. Defaults to `None`.
    match : `None`, `str`
        Unique hash for spectate button. Defaults to `None`.
    spectate : `None`, `str`
        Unique hash for chat invites and ask to join. Defaults to `None`.
    """
    __slots__ = ('join', 'match', 'spectate', )
    
    def __new__(cls, *, join=None, match=None, spectate=None):
        """
        Creates a new activity secret from the given parameters.
        
        Parameters
        ----------
        join : `None`, `str` = `None`, Optional (Keyword only)
            Unique hash given for the match context. Defaults to `None`.
        match : `None`, `str` = `None`, Optional (Keyword only)
            Unique hash for spectate button. Defaults to `None`.
        spectate : `None`, `str` = `None`, Optional (Keyword only)
            Unique hash for chat invites and ask to join. Defaults to `None`.
        """
        if (join is not None):
            if __debug__:
                if (not isinstance(join, str)):
                    raise AssertionError(
                        f'`join` can be `None`, `str`, got {join.__class__.__name__}; {join!r}.'
                    )
            
            if (not join):
                join = None
            
            
        if (match is not None):
            if __debug__:
                if (not isinstance(match, str)):
                    raise AssertionError(
                        f'`match` can be `None`, `str`, got {match.__class__.__name__}; {match!r}.'
                    )
            
            if (not match):
                match = None
            
        
        if (spectate is not None):
            if __debug__:
                if (not isinstance(spectate, str)):
                    raise AssertionError(
                        f'`spectate` can be `None`, `str`, got {spectate.__class__.__name__}; {spectate!r}.'
                    )
            
            if (not spectate):
                spectate = None
        
        self = object.__new__(cls)
        self.join = join
        self.match = match
        self.spectate = spectate
        return self
    
    
    @classmethod
    @copy_docs(ActivityFieldBase.from_data)
    def from_data(cls, secrets_data):
        self = object.__new__(cls)
        self.join = secrets_data.get('join', None)
        self.spectate = secrets_data.get('spectate', None)
        self.match = secrets_data.get('match', None)
        return self
    
    
    @copy_docs(ActivityFieldBase.to_data)
    def to_data(self):
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
    
    
    @copy_docs(ActivityFieldBase.__repr__)
    def __repr__(self):
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
    
    
    @copy_docs(ActivityFieldBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.join != other.join:
            return False
        
        if self.spectate != other.spectate:
            return False
        
        if self.match != other.match:
            return False
        
        return True
    

    @copy_docs(ActivityFieldBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        join = self.join
        if (join is not None):
            hash_value ^= hash(join)
            hash_value ^= (1 << 0)
        
        spectate = self.spectate
        if (spectate is not None):
            hash_value ^= hash(spectate)
            hash_value ^= (1 << 4)
        
        match = self.match
        if (match is not None):
            hash_value ^= hash(match)
            hash_value ^= (1 << 8)
        
        return hash_value
    
    
    @copy_docs(ActivityFieldBase.__bool__)
    def __bool__(self):
        join = self.join
        if (join is not None):
            return True
        
        spectate = self.spectate
        if (spectate is not None):
            return True
        
        match = self.match
        if (match is not None):
            return True
        
        return False


class ActivityBase(RichAttributeErrorBaseType):
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

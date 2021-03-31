# -*- coding: utf-8 -*-
__all__ = ('ActivityAssets', 'ActivityBase', 'ActivityCustom', 'ActivityParty', 'ActivityRich', 'ActivitySecrets',
    'ActivityTimestamps', 'ActivityTypes', 'ActivityUnknown', )

from datetime import datetime


from ..backend.utils import modulize

from .utils import DISCORD_EPOCH_START
from .bases import FlagBase
from .color import Color
from .http import URLS
from .preconverters import preconvert_str, preconvert_int

from . import preinstanced as module_preinstanced

create_partial_emoji = NotImplemented

DEFAULT_CUSTOM_ID = 'UNKNOWN'

CUSTOM_IDS = {
    2 : 'spotify:1',
    4 : 'custom',
        }

class ActivityFlag(FlagBase):
    """
    The flags of an activity provided by Discord. These flags supposed to describe what the activity's payload
    includes.
    
    The activity flags are the following:
    
    +-------------------+-------------------+
    | Respective name   | Bitwise position  |
    +===================+===================+
    | INSTANCE          | 0                 |
    +-------------------+-------------------+
    | JOIN              | 1                 |
    +-------------------+-------------------+
    | SPECTATE          | 2                 |
    +-------------------+-------------------+
    | JOIN_REQUEST      | 3                 |
    +-------------------+-------------------+
    | SYNC              | 4                 |
    +-------------------+-------------------+
    | PLAY              | 5                 |
    +-------------------+-------------------+
    """
    __keys__ = {
        'INSTANCE'    : 0,
        'JOIN'        : 1,
        'SPECTATE'    : 2,
        'JOIN_REQUEST': 3,
        'SYNC'        : 4,
        'PLAY'        : 5,
            }


@modulize
class ActivityTypes:
    """
    A module, which contains the activity types' discord side value.
    
    +-----------+-------+
    | Name      | Value |
    +===========+=======+
    | game      | 0     |
    +-----------+-------+
    | stream    | 1     |
    +-----------+-------+
    | spotify   | 2     |
    +-----------+-------+
    | watching  | 3     |
    +-----------+-------+
    | custom    | 4     |
    +-----------+-------+
    | competing | 5     |
    +-----------+-------+
    """
    game = 0
    stream = 1
    spotify = 2
    watching = 3
    custom = 4
    competing = 5


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
        result = [
            '<',
            self.__class__.__name__,
                ]
        
        start = self.start
        if start:
            result.append(' start=')
            result.append(repr(start))
            put_comma = True
        else:
            put_comma = False
        
        end = self.end
        if end:
            if put_comma:
                result.append(',')
            
            result.append(' end=')
            result.append(repr(start))
        
        result.append('>')
        
        return ''.join(result)
    
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
        self.image_large = assets_data.get('large_image')
        self.image_small = assets_data.get('small_image')
        self.text_large = assets_data.get('large_text')
        self.text_small = assets_data.get('small_text')
    
    def __repr__(self):
        """Returns the activity asset's representation."""
        result = [
            '<',
            self.__class__.__name__,
                ]
        
        image_large = self.image_large
        if (image_large is not None):
            result.append(' image_large=')
            result.append(repr(image_large))
            put_comma = True
        else:
            put_comma = False
        
        image_small = self.image_small
        if (image_small is not None):
            if put_comma:
                result.append(',')
            else:
                put_comma = True
            result.append(' image_small=')
            result.append(repr(image_small))
        
        text_large = self.text_large
        if (text_large is not None):
            if put_comma:
                result.append(',')
            else:
                put_comma = True
            result.append(' text_large=')
            result.append(repr(text_large))
        
        text_small = self.text_small
        if (text_small is not None):
            if put_comma:
                result.append(',')
            result.append(' text_small=')
            result.append(repr(text_small))
        
        result.append('>')
        
        return ''.join(result)
    
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
        self.id = party_data.get('id')
        
        try:
            size, max_ = party_data['size']
        except KeyError:
            size = 0
            max_ = 0
        
        self.size = size
        self.max = max_
    
    def __repr__(self):
        """Returns the activity party's representation."""
        result = [
            '<',
            self.__class__.__name__,
                ]
        
        id_ = self.id
        if (id is not None):
            result.append(' id_=')
            result.append(repr(id_))
            put_comma = True
        else:
            put_comma = False
        
        size = self.size
        max_ = self.max
        if size or max_:
            if put_comma:
                result.append(',')
            result.append(' size=')
            result.append(repr(size))
            result.append(', max=')
            result.append(repr(max_))
        
        result.append('>')
        
        return ''.join(result)
    
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
        self.join = secrets_data.get('join')
        self.spectate = secrets_data.get('spectate')
        self.match = secrets_data.get('match')
    
    def __repr__(self):
        """Returns the activity secret's representation."""
        result = [
            '<',
            self.__class__.__name__,
                ]
        
        join = self.join
        if (join is not None):
            result.append(' join=')
            result.append(repr(join))
            put_comma = True
        else:
            put_comma = False
        
        spectate = self.spectate
        if (spectate is not None):
            if put_comma:
                result.append(',')
            else:
                put_comma = True
            result.append(' spectate=')
            result.append(repr(spectate))
        
        match = self.match
        if (match is not None):
            if put_comma:
                result.append(',')
            result.append(' match=')
            result.append(repr(match))
        
        result.append('>')
        
        return ''.join(result)
    
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
    def colour(self):
        """Alias of ``.color``."""
        return self.color
    
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


class ActivityRich(ActivityBase):
    """
    Represents a Discord rich activity.
    
    Attributes
    ----------
    application_id : `int`
        The id of the activity's application. Defaults to `0`.
    assets : `None` or ``ActivityAssets``
        The activity's assets. Defaults to `None`.
    created : `int`
        When the status was created as Unix time in milliseconds. Defaults to `0`.
    details : `None` or `str`
        What the player is currently doing. Defaults to `None`.
    flags : ``ActivityFlag``
        The flags of the activity. Defaults to `ActivityFlag(0)`
    id : `int`
        The id of the activity. Defaults to `0`.
    name : `str`
        The activity's name.
    party : `None` or ``ActivityParty``
        The party's party.
    secrets : `None` or ``ActivitySecrets``
        The activity's secrets. Defaults to `None`.
    session_id : `None` or `str`
        The ``ActivitySpotify``'s session's id. Defaults to `None`.
    state : `str` or `None`
        The player's current party status. Defaults to `None`.
    sync_id : `None` or `str`
        The ID of the currently playing track. Defaults to `None`.
    timestamps : `None` or ``ActivityTimestamp``
        The activity's timestamps.
    type : `int`
        An integer, what represent the activity's type for Discord. Can be one of: `0`, `1`, `2`, `3`, `4`.
    url : `None` or `str`
        The url of the stream (Twitch or Youtube only). Defaults to `None`.
    """
    __slots__ = ('application_id', 'assets', 'created', 'details', 'flags', 'id', 'name', 'party', 'secrets',
        'session_id', 'state', 'sync_id', 'timestamps', 'type', 'url', )
    
    def __new__(cls, name, url=None, type_=ActivityTypes.game):
        """
        Creates a new activity with the given parameters.
        
        Parameters
        ----------
        name : `str`
            The name of the activity.
        url : `str`, Optional
            The url of the activity. Only twitch and youtube urls are supported.
        type_ : `int`, Optional
            The type value of the activity.
        
        Returns
        -------
        activity : ``ActivityRich``
        
        Raises
        ------
        TypeError
            If any argument's type is bad or if unexpected argument is passed.
        ValueError
            If an argument's type is good, but it's value is unacceptable.
        """
        name = preconvert_str(name, 'name', 0, 2048)
        
        if (url is not None):
            url = preconvert_str(name, 'url', 0, 2048)
        
        type_ = preconvert_int(type_, 'type_', 0, 5)
        
        if type_ == ActivityTypes.custom:
            raise RuntimeError(f'Custom activity cannot be created with `{cls.__name__}.__new__`.')
        
        self = object.__new__(cls)
        self.name = name
        self.url = url
        self.type = type_
        
        self.application_id = 0
        self.timestamps = None
        self.details = None
        self.state = None
        self.party = None
        self.assets = None
        self.secrets = None
        self.sync_id = None
        self.session_id = None
        self.flags = ActivityFlag()
        self.created = 0
        self.id = 0
        
        return self
    
    def __repr__(self):
        """Returns the rich activity's representation."""
        return f'<{self.__class__.__name__} name={self.name!r}, type={self.type}>'
    
    @property
    def color(self):
        """
        Returns the activity's color.
        
        Returns
        -------
        color : ``Color``
        """
        type_ = self.type
        if type_ == ActivityTypes.game:
            return Color(0x7289da)
        
        if type_ == ActivityTypes.stream:
            if self.url is None:
                return Color(0x7289da)
            else:
                return Color(0x593695)
        
        if type_ == ActivityTypes.spotify:
            return Color(0x1db954)
        
        if type_ == ActivityTypes.watching:
            return Color(0x7289da)
        
        return Color()
    
    @property
    def start(self):
        """
        Returns when the activity was started if applicable.
        
        Returns
        -------
        start : `None` or `datetime`
        """
        timestamps = self.timestamps
        if timestamps is None:
            return None
        
        start = timestamps.start
        if start == 0:
            return None
        
        return datetime.utcfromtimestamp(start/1000.)
    
    @property
    def end(self):
        """
        Returns when the activity ended or will end if applicable.
        
        Returns
        -------
        start : `None` or `datetime`
        """
        timestamps = self.timestamps
        if timestamps is None:
            return None
        
        end = timestamps.end
        if end == 0:
            return None
        
        return datetime.utcfromtimestamp(end/1000.)
    
    image_large_url = property(URLS.activity_asset_image_large_url)
    image_large_url_as = URLS.activity_asset_image_large_url_as
    image_small_url = property(URLS.activity_asset_image_small_url)
    image_small_url_as = URLS.activity_asset_image_small_url_as
    
    @classmethod
    def from_data(cls, activity_data):
        """
        Creates a new ``ActivityRich`` instance from the given activity data.
        
        Parameters
        ----------
        activity_data : `dict` of (`str`, `Any`) items
            Received activity data.
        
        Returns
        -------
        self : ``ActivityRich``
        """
        self = object.__new__(cls)
        type_ = activity_data['type']
        self.type = type_
        
        if type_ in CUSTOM_IDS:
            id_ = 0
        else:
            id_ = int(activity_data['id'], base=16)
        self.id = id_
        
        self._update_no_return(activity_data)
        return self
    
    def _update_no_return(self, activity_data):
        """
        Updates the activity by overwriting it's old attributes.
        
        Parameters
        ----------
        activity_data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        """
        try:
            application_id = activity_data['application_id']
        except KeyError:
            application_id = 0
        else:
            application_id = int(application_id)
        self.application_id = application_id
        
        try:
            assets_data = activity_data['assets']
        except KeyError:
            assets = None
        else:
            assets = ActivityAssets(assets_data)
        self.assets = assets
        
        self.created = activity_data.get('created_at', 0)
        
        self.details = activity_data.get('details')
        
        self.flags = ActivityFlag(activity_data.get('flags', 0))
        
        self.name = activity_data['name']
        
        try:
            party_data = activity_data['party']
        except KeyError:
            party = None
        else:
            party = ActivityParty(party_data)
        self.party = party
        
        try:
            secrets_data = activity_data['secrets']
        except KeyError:
            secrets = None
        else:
            secrets = ActivitySecrets(secrets_data)
        self.secrets = secrets
        
        self.session_id = activity_data.get('session_id')
        
        self.state = activity_data.get('state')
        
        self.sync_id = activity_data.get('sync_id')
        
        try:
            timestamps_data = activity_data['timestamps']
        except KeyError:
            timestamps = None
        else:
            timestamps = ActivityTimestamps(timestamps_data)
        self.timestamps = timestamps
        
        self.url = activity_data.get('url')
    
    def _update(self, activity_data):
        """
        Updates the activity and returns the changes in a `dict` of (`attribute-name`, `old-value`) items.
        
        Parameters
        ----------
        activity_data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +-------------------+-----------------------------------+
        | Keys              | Values                            |
        +===================+===================================+
        | application_id    | `int`                             |
        +-------------------+-----------------------------------+
        | assets            | `None` or ``ActivityAssets``      |
        +-------------------+-----------------------------------+
        | created           | `int`                             |
        +-------------------+-----------------------------------+
        | details           | `None` or `str`                   |
        +-------------------+-----------------------------------+
        | flags             | ``ActivityFlag``                  |
        +-------------------+-----------------------------------+
        | name              | `str`                             |
        +-------------------+-----------------------------------+
        | party             | `None` or ``ActivityParty``       |
        +-------------------+-----------------------------------+
        | secrets           | `None` or ``ActivitySecrets``     |
        +-------------------+-----------------------------------+
        | session_id        | `None` or `str`                   |
        +-------------------+-----------------------------------+
        | state             | `None` or `str`                   |
        +-------------------+-----------------------------------+
        | sync_id           | `None` or `str`                   |
        +-------------------+-----------------------------------+
        | timestamps        | `None` or `ActivityTimestamps``   |
        +-------------------+-----------------------------------+
        | url               | `None` or `str`                   |
        +-------------------+-----------------------------------+
        """
        old_attributes = {}
        
        try:
            application_id = activity_data['application_id']
        except KeyError:
            application_id = 0
        else:
            application_id = int(application_id)
        
        if self.application_id != application_id:
            old_attributes['application_id'] = self.application_id
            self.application_id = application_id
        
        try:
            assets_data = activity_data['assets']
        except KeyError:
            assets = None
        else:
            assets = ActivityAssets(assets_data)
        
        if self.assets != assets:
            old_attributes['assets'] = self.assets
            self.assets = assets
        
        created = activity_data.get('created_at', 0)
        if self.created != created:
            old_attributes['created'] = self.created
            self.created = created
        
        details = activity_data.get('details')
        if self.details != details:
            old_attributes['details'] = self.details
            self.details = details
        
        flags = activity_data.get('flags', 0)
        if self.flags != flags:
            old_attributes['flags'] = self.flags
            self.flags = ActivityFlag(flags)
        
        name = activity_data['name']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        try:
            party_data = activity_data['party']
        except KeyError:
            party = None
        else:
            party = ActivityParty(party_data)
        
        if self.party != party:
            old_attributes['party'] = self.party
            self.party = party
        
        try:
            secrets_data = activity_data['secrets']
        except KeyError:
            secrets = None
        else:
            secrets = ActivitySecrets(secrets_data)
        
        if self.secrets != secrets:
            old_attributes['secrets'] = self.secrets
            self.secrets = secrets
        
        session_id = activity_data.get('session_id')
        if self.session_id != session_id:
            old_attributes['session_id'] = self.session_id
            self.session_id = session_id
        
        state = activity_data.get('state')
        if self.state != state:
            old_attributes['state'] = self.state
            self.state = state
        
        sync_id = activity_data.get('sync_id')
        if self.sync_id != sync_id:
            old_attributes['sync_id'] = self.sync_id
            self.sync_id = sync_id
        
        try:
            timestamps_data = activity_data['timestamps']
        except KeyError:
            timestamps = None
        else:
            timestamps = ActivityTimestamps(timestamps_data)
        
        if self.timestamps != timestamps:
            old_attributes['timestamps'] = self.timestamps
            self.timestamps = timestamps
        
        url = activity_data.get('url')
        if self.url != url:
            old_attributes['url'] = self.url
            self.url = url
        
        return old_attributes
    
    def bot_dict(self):
        """
        Converts the activity to json serializable dictionary, which can be sent with bot account to change activity.
        
        Returns
        -------
        activity_data : `dict` of (`str`, `Any`) items
        """
        activity_data = {
            'type' : self.type,
            'name' : self.name,
                }
        
        url = self.url
        if (url is not None):
            activity_data['url'] = url
        
        return activity_data
    
    def user_dict(self):
        """
        Converts the activity to json serializable dictionary, which can (?) be sent with user account to change
        activity.
        
        Returns
        -------
        activity_data : `dict` of (`str`, `Any`) items
        """
        activity_data = self.bot_dict()
        
        application_id = self.application_id
        if application_id:
            activity_data['application_id'] = application_id
        
        assets = self.assets
        if (assets is not None):
            assets_data = assets.to_data()
            if assets_data:
                activity_data['assets'] = assets_data
        
        details = self.details
        if (details is not None):
            activity_data['details'] = details
        
        flags = self.flags
        if flags:
            activity_data['flags'] = flags
        
        party = self.party
        if (party is not None):
            party_data = party.to_data()
            if party_data:
                activity_data['party'] = party_data
        
        secrets = self.secrets
        if (secrets is not None):
            secrets_data = secrets.to_data()
            activity_data['secrets'] = secrets_data
        
        session_id = self.session_id
        if (session_id is not None):
            activity_data['session_id'] = session_id
        
        state = self.state
        if (state is not None):
            activity_data['state'] = state
        
        sync_id = self.sync_id
        if (sync_id is not None):
            activity_data['sync_id'] = sync_id
        
        timestamps = self.timestamps
        if (timestamps is not None):
            timestamps_data = timestamps.to_data()
            if timestamps_data:
                activity_data['timestamps'] = timestamps_data
        
        return activity_data
    
    def full_dict(self):
        """
        Converts the whole activity to a dictionary.
        
        Returns
        -------
        activity_data : `dict` of (`str`, `Any`) items
        """
        activity_data = self.user_dict()

        #receive only?
        activity_data['id'] = self.discord_side_id
        
        #receive only?
        created = self.created
        if created:
            activity_data['created_at'] = created
        
        return activity_data
    
    def __hash__(self):
        """Returns the activity's hash value."""
        id_ = self.id
        if id_:
            return id_
        
        # Spotify activity has no `.id`, but has `.session_id`
        return hash(self.session_id)
    
    @property
    def twitch_name(self):
        """
        If the user streams on twitch, returns it's twitch name.
        
        Returns
        -------
        name : `None` or `str`
        """
        if self.type != ActivityTypes.stream:
            return None
        
        assets = self.assets
        if assets is None:
            return None
        
        image_large = assets.image_large
        if image_large is None:
            return None
        
        if not image_large.startswith('twitch:'):
            return None
        
        return image_large[7:]
    
    @property
    def duration(self):
        """
        Returns the spotify activity's duration, or `None` if not applicable.
        
        Returns
        -------
        duration : `None` or `timedelta`
        """
        if self.type != ActivityTypes.spotify:
            return None
        
        timestamps = self.timestamps
        start = timestamps.start
        if start is None:
            return None
        
        end = timestamps.end
        if end is None:
            return None
        
        return datetime.utcfromtimestamp(end/1000.0) - datetime.utcfromtimestamp(start/1000.0)
    
    @property
    def album_cover_url(self):
        """
        Returns the spotify activity's currently playing track's album url if applicable.
        
        Returns
        -------
        album_cover_url : `None` or `str`
        """
        if self.type != ActivityTypes.spotify:
            return None
        
        assets = self.assets
        if assets is None:
            return None
        
        image_large = assets.image_large
        if image_large is None:
            return None
            
        return f'https://i.scdn.co/image/{image_large}'

class ActivityUnknown(ActivityBase):
    """
    Represents if a user has no activity set. This activity type is not a valid Discord activity.
    
    ``activity_unknown`` is a singleton with type value of `127`.
    
    Class Attributes
    ----------------
    created : `int` = `0`
        When the activity was created as Unix time in milliseconds.
    color : ``Color`` = `Color(0)
        The color of the activity.
    name : `str` = `'Unknown'`
        The activity's name. Subclasses might overwrite it as member descriptor.
    id : `int` = `0`
        The activity's id. Subclasses might overwrite it as member descriptor.
    type : `int` = `127`
        The activity's type value.
    """
    __slots__ = ()
    
    def __repr__(self):
        """Returns the activity's representation."""
        return f'<{self.__class__.__name__}>'

ActivityUnknown = object.__new__(ActivityUnknown)


class ActivityCustom(ActivityBase):
    """
    Represents a Discord custom activity.
    
    Attributes
    ----------
    created : `int`
        When the status was created as Unix time in milliseconds. Defaults to `0`.
    emoji : `None` or ``Emoji``
        The emoji of the activity. If it has no emoji, then set as `None`.
    state : `str` or `None`
        The activity's text under it's emoji. Defaults to `None`.
    
    Class Attributes
    ----------------
    id : `int` = `0`
        The activity's id.
    type : `int` = `4`
        The activity's type value.
    """
    __slots__ = ('created', 'emoji', 'state', )
    
    type = ActivityTypes.custom
    
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
        self._update_no_return(activity_data)
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
    
    def _update_no_return(self, activity_data):
        """
        Updates the activity by overwriting it's old attributes.
        
        Parameters
        ----------
        activity_data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        """
        self.state = activity_data.get('state')
        
        emoji_data = activity_data.get('emoji')
        if emoji_data is None:
            emoji = None
        else:
            emoji = create_partial_emoji(emoji_data)
        self.emoji = emoji
        
        self.created = activity_data.get('created_at', 0)
    
    def _update(self, activity_data):
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
        
        Returned Data Structure
        -----------------------
        +-----------+-----------------------+
        | key       | value                 |
        +===========+=======================+
        | created   | `int`                 |
        +-----------+-----------------------+
        | emoji     | `None` or ``Emoji``   |
        +-----------+-----------------------+
        | state     | `str` or `None`       |
        +-----------+-----------------------+
        """
        old_attributes = {}
        
        state = activity_data.get('state')
        if self.state != state:
            old_attributes['state'] = self.state
            self.state = state
        
        emoji_data = activity_data.get('emoji')
        if emoji_data is None:
            emoji = None
        else:
            emoji = create_partial_emoji(emoji_data)
        
        if self.emoji != emoji:
            old_attributes['emoji'] = self.emoji
            self.emoji = emoji
        
        created = activity_data.get('created_at', 0)
        if self.created != created:
            old_attributes['created'] = self.created
            self.created = created
        
        return old_attributes
    
    def full_dict(self):
        """
        Converts the whole activity to a dictionary.
        
        Returns
        -------
        activity_data : `dict` of (`str`, `Any`) items
        """
        activity_data = {
            'name' : 'Custom Status',
            'id' : 'custom',
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
        
        created = self.created
        if created:
            activity_data['created_at'] = created
        
        return activity_data

def create_activity(activity_data):
    """
    A factory function to create activity from the json data sent by Discord.
    
    If the data is `None` returns ``ActivityUnknown``.
    
    Parameters
    ----------
    activity_data : `dict` of (`str`, `Any`) items
        Activity data received from Discord.
    
    Returns
    -------
    activity : ``ActivityBase`` instance
    """
    if activity_data is None:
        return ActivityUnknown
    
    if activity_data['type'] == ActivityTypes.custom:
        activity_type = ActivityCustom
    else:
        activity_type = ActivityRich
    
    return activity_type.from_data(activity_data)


module_preinstanced.ActivityTypes = ActivityTypes

del module_preinstanced

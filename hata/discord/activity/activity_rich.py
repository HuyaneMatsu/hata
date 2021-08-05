__all__ = ('ActivityRich',)

from datetime import datetime

from ..color import Color
from ..preconverters import preconvert_str, preconvert_int_options, preconvert_snowflake, preconvert_flag
from ..http import urls as module_urls
from ..utils import is_url, DISCORD_EPOCH_START, unix_time_to_datetime, datetime_to_unix_time

from . import activity_types as ACTIVITY_TYPES
from .activity_base import ActivityBase, ACTIVITY_TYPE_NAMES, ActivityAssets, ActivityParty, ActivitySecrets, \
    ActivityTimestamps, CUSTOM_IDS
from .flags import ActivityFlag

ACTIVITY_TYPE_NAME_UNKNOWN = 'unknown'

VALID_RICH_ACTIVITY_TYPES = frozenset((
    ACTIVITY_TYPES.game,
    ACTIVITY_TYPES.stream,
    ACTIVITY_TYPES.spotify,
    ACTIVITY_TYPES.watching,
    ACTIVITY_TYPES.competing,
))

class ActivityRich(ActivityBase):
    """
    Represents a Discord rich activity.
    
    Attributes
    ----------
    application_id : `int`
        The id of the activity's application. Defaults to `0`.
    assets : `None` or ``ActivityAssets``
        The activity's assets. Defaults to `None`.
    created_at : `datetime`
        When the activity was created. Defaults to Discord epoch.
    details : `None` or `str`
        What the player is currently doing. Defaults to `None`.
    flags : ``ActivityFlag``
        The flags of the activity. Defaults to `ActivityFlag(0)`
    id : `int`
        The id of the activity. Defaults to `0`.
    name : `str`
        The activity's name.
    party : `None` or ``ActivityParty``
        The activity's party.
    secrets : `None` or ``ActivitySecrets``
        The activity's secrets. Defaults to `None`.
    session_id : `None` or `str`
        Spotify activity's session's id. Defaults to `None`.
    state : `None` or `str`
        The player's current party status. Defaults to `None`.
    sync_id : `None` or `str`
        The ID of the currently playing track of a spotify activity. Defaults to `None`.
    timestamps : `None` or ``ActivityTimestamps``
        The activity's timestamps.
    type : `int`
        An integer, what represent the activity's type for Discord. Can be one of: `0`, `1`, `2`, `3`, `4`.
    url : `None` or `str`
        The url of the stream (Twitch or Youtube only). Defaults to `None`.
    """
    __slots__ = ('application_id', 'assets', 'created_at', 'details', 'flags', 'id', 'name', 'party', 'secrets',
        'session_id', 'state', 'sync_id', 'timestamps', 'type', 'url', )
    
    def __new__(cls, name, *, application_id=..., assets=None, created_at=..., details=None, flags=..., id_=...,
            party=None, secrets=None, session_id=None, state=None, sync_id=None, timestamps=None, type_=..., url=None):
        """
        Creates a new activity with the given parameters.
        
        Parameters
        ----------
        name : `str`
            The name of the activity.
        application_id : `None` or `int`, Optional (Keyword only)
            The id of the activity's application. Defaults to `0`.
        assets : `None` or ``ActivityAssets``, Optional (Keyword only)
             The activity's assets. Defaults to `None`.
        details : `None` or `str`, Optional (Keyword only)
            What the player is currently doing. Defaults to `None`.
        flags : ``ActivityFlag``, `int`, Optional (Keyword only)
            The flags of the activity. Defaults to `ActivityFlag(0)`
        id_ : `int`, Optional (Keyword only)
            The id of the activity. Defaults to `0`.
        party : `None` or ``ActivityParty``, Optional (Keyword only)
            The activity's party.
        secrets : `None` or ``ActivitySecret``, Optional (Keyword only)
            The activity's secrets. Defaults to `None`.
        session_id : `None` or `str`, Optional (Keyword only)
            Spotify activity's session's id. Defaults to `None`.
        state : `None` or `str`, Optional (Keyword only)
            The player's current party status. Defaults to `None`.
        sync_id : `None` or `str`, Optional (Keyword only)
            The ID of the currently playing track of a spotify activity. Defaults to `None`.
        timestamps : `None` or ``ActivityTimestamps``, Optional (Keyword only)
            The activity's timestamps.
        type_ : `int`, Optional (Keyword only)
            The type value of the activity.
        url : `None`, `str`, Optional (Keyword only)
            The url of the activity. Only twitch and youtube urls are supported.
        
        Returns
        -------
        activity : ``ActivityRich``
        
        Raises
        ------
        TypeError
            - If `name` was not given as `str` instance.
            - If `url`'s type is neither `None` sor `str`.
            - If `type_` is not `int` instance.
            - If `application_id` is not `int` instance.
            - If `details` is neither `None` nor `str` instance.
            - If `assets` is neither `None` nor ``ActivityAssets`` instance.
            - If `party` is neither `None` nor ``ActivityParty`` instance.
            - If `id_` is not `int` instance.
            - If `created_at` is not `int` instance.
            - If `session_id` is neither `None` sor `str`
            - If `state` is neither `None` sor `str` instance.
            - if `timestamps` is neither `None` nor ``ActivityTimestamps`` instance.
            - If `sync_id` is neither `None` nor `str` instance.
        ValueError
            - If `name`'s length is out of range [1:2048].
            - If `url`'s length is out of range [0:2048].
            - If `type_` is not any of the expected values.
            - If `details`'s length is out of range [0:2048].
            - If `state`'s length is out of range [0:2048].
            - If `sync_id`'s length is out of range [0:2048].
            - If `session_id`'s length is out of range [0:2048].
        AssertionError
            - If `url` is nto a valid url.
        """
        name = preconvert_str(name, 'name', 1, 2048)
        
        if application_id is ...:
            application_id = 0
        else:
            application_id = preconvert_snowflake(application_id, 'application_id')
        
        
        if (assets is not None) and (not isinstance(assets, ActivityAssets)):
            raise TypeError(f'`assets` can be either `None` or `{ActivityAssets.__name__}` instance, got '
                f'{assets.__class__.__name__}')
        
        
        if created_at is ...:
            created_at = DISCORD_EPOCH_START
        else:
            if not isinstance(created_at, datetime):
                raise TypeError(f'`created_at` can be `datetime` instance, got {created_at.__class__.__name__}.')
        
        
        if (details is not None):
            details = preconvert_str(details, 'details', 0, 2048)
            if (not details):
                details = None
        
        
        if (flags is ...):
            flags = ActivityFlag(0)
        else:
            flags = preconvert_flag(flags, 'flags', ActivityFlag)
        
        
        
        if id_ is ...:
            id_ = 0
        else:
            id_ = preconvert_snowflake(id_, 'id_')
        
        
        if (party is not None) and (not isinstance(party, ActivityParty)):
            raise TypeError(f'`party` can be either `None` or `{ActivityParty.__name__}` instance, got '
                f'{party.__class__.__name__}.')
        
        
        if (secrets is not None) and (not isinstance(secrets, ActivitySecrets)):
            raise TypeError(f'`secrets` can be either `None` or `{ActivitySecrets.__name__}` instance, got '
                f'{secrets.__class__.__name__}.')
        
        
        if (session_id is not None):
            session_id = preconvert_str(session_id, 'session_id', 0, 2048)
            if (not session_id):
                session_id = None
        
        
        if (state is not None):
            state = preconvert_str(state, 'state', 0, 2048)
            if (not state):
                state = None
        
        
        if (timestamps is not None) and (not isinstance(timestamps, ActivityTimestamps)):
            raise TypeError(f'`timestamps` can be either `None` or `{ActivityTimestamps.__name__}` instance, got '
                f'{timestamps.__class__.__name__}')
        
        
        if (sync_id is not None):
            sync_id = preconvert_str(sync_id, 'sync_id', 0, 2048)
            if (not sync_id):
                sync_id = None
        
        
        if (url is not None):
            url = preconvert_str(url, 'url', 0, 2048)
            if url:
                if __debug__:
                    if not is_url(url):
                        raise AssertionError(f'`url` was not given as a valid url, got {url!r}.')
            
            else:
                url = None
        
        if type_ is ...:
            type_ = ACTIVITY_TYPES.game
        else:
            type_ = preconvert_int_options(type_, 'type_', VALID_RICH_ACTIVITY_TYPES)
        
        
        
        self = object.__new__(cls)
        self.name = name
        
        self.application_id = application_id
        self.details = details
        self.flags = flags
        self.state = state
        self.party = party
        self.assets = assets
        self.secrets = secrets
        self.sync_id = sync_id
        self.session_id = session_id
        self.created_at = created_at
        self.id = id_
        self.timestamps = timestamps
        self.type = type_
        self.url = url
        
        return self
    
    def __repr__(self):
        """Returns the rich activity's representation."""
        repr_parts = ['<', self.__class__.__name__, ' name=', repr(self.name), ' type=']
        
        type_value = self.type
        type_name = ACTIVITY_TYPE_NAMES.get(type_value, ACTIVITY_TYPE_NAME_UNKNOWN)
        repr_parts.append(type_name)
        repr_parts.append(' (')
        repr_parts.append(repr(type_value))
        repr_parts.append(')')
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    @property
    def color(self):
        """
        Returns the activity's color.
        
        Returns
        -------
        color : ``Color``
        """
        type_ = self.type
        if type_ == ACTIVITY_TYPES.game:
            return Color(0x7289da)
        
        if type_ == ACTIVITY_TYPES.stream:
            if self.url is None:
                return Color(0x7289da)
            else:
                return Color(0x593695)
        
        if type_ == ACTIVITY_TYPES.spotify:
            return Color(0x1db954)
        
        if type_ == ACTIVITY_TYPES.watching:
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
        if (timestamps is not None):
            return timestamps.start
    
    
    @property
    def end(self):
        """
        Returns when the activity ended or will end if applicable.
        
        Returns
        -------
        start : `None` or `datetime`
        """
        timestamps = self.timestamps
        if (timestamps is not None):
            return timestamps.end
    
    
    image_large_url = property(module_urls.activity_asset_image_large_url)
    image_large_url_as = module_urls.activity_asset_image_large_url_as
    image_small_url = property(module_urls.activity_asset_image_small_url)
    image_small_url_as = module_urls.activity_asset_image_small_url_as
    
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
            try:
                raw_id = activity_data['id']
            except KeyError:
                id_ = 0
            else:
                id_ = int(raw_id, base=16)
        
        self.id = id_
        
        self._update_attributes(activity_data)
        return self
    
    
    def _update_attributes(self, activity_data):
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
            assets = ActivityAssets.from_data(assets_data)
        self.assets = assets
        
        created_at = activity_data.get('created_at', None)
        if created_at is None:
            created_at = DISCORD_EPOCH_START
        else:
            created_at = unix_time_to_datetime(created_at)
        self.created_at = created_at
        
        self.details = activity_data.get('details', None)
        
        self.flags = ActivityFlag(activity_data.get('flags', 0))
        
        self.name = activity_data['name']
        
        try:
            party_data = activity_data['party']
        except KeyError:
            party = None
        else:
            party = ActivityParty.from_data(party_data)
        self.party = party
        
        try:
            secrets_data = activity_data['secrets']
        except KeyError:
            secrets = None
        else:
            secrets = ActivitySecrets.from_data(secrets_data)
        self.secrets = secrets
        
        self.session_id = activity_data.get('session_id', None)
        
        self.state = activity_data.get('state', None)
        
        self.sync_id = activity_data.get('sync_id', None)
        
        try:
            timestamps_data = activity_data['timestamps']
        except KeyError:
            timestamps = None
        else:
            timestamps = ActivityTimestamps.from_data(timestamps_data)
        self.timestamps = timestamps
        
        self.url = activity_data.get('url', None)
    
    
    def _difference_update_attributes(self, activity_data):
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
        | created_at        | `datetime`                        |
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
            assets = ActivityAssets.from_data(assets_data)
        
        if self.assets != assets:
            old_attributes['assets'] = self.assets
            self.assets = assets
        
        created_at = activity_data.get('created_at', None)
        if created_at is None:
            created_at = DISCORD_EPOCH_START
        else:
            created_at = unix_time_to_datetime(created_at)
        if self.created_at != created_at:
            old_attributes['created_at'] = self.created_at
            self.created_at = created_at
        
        details = activity_data.get('details', None)
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
            party = ActivityParty.from_data(party_data)
        
        if self.party != party:
            old_attributes['party'] = self.party
            self.party = party
        
        try:
            secrets_data = activity_data['secrets']
        except KeyError:
            secrets = None
        else:
            secrets = ActivitySecrets.from_data(secrets_data)
        
        if self.secrets != secrets:
            old_attributes['secrets'] = self.secrets
            self.secrets = secrets
        
        session_id = activity_data.get('session_id', None)
        if self.session_id != session_id:
            old_attributes['session_id'] = self.session_id
            self.session_id = session_id
        
        state = activity_data.get('state', None)
        if self.state != state:
            old_attributes['state'] = self.state
            self.state = state
        
        sync_id = activity_data.get('sync_id', None)
        if self.sync_id != sync_id:
            old_attributes['sync_id'] = self.sync_id
            self.sync_id = sync_id
        
        try:
            timestamps_data = activity_data['timestamps']
        except KeyError:
            timestamps = None
        else:
            timestamps = ActivityTimestamps.from_data(timestamps_data)
        
        if self.timestamps != timestamps:
            old_attributes['timestamps'] = self.timestamps
            self.timestamps = timestamps
        
        url = activity_data.get('url', None)
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
        activity_data = {}
        
        assets = self.assets
        if (assets is not None):
            assets_data = assets.to_data()
            if assets_data:
                activity_data['assets'] = assets_data
        
        details = self.details
        if (details is not None):
            activity_data['details'] = details
        
        party = self.party
        if (party is not None):
            party_data = party.to_data()
            if party_data:
                activity_data['party'] = party_data
        
        secrets = self.secrets
        if (secrets is not None):
            secrets_data = secrets.to_data()
            activity_data['secrets'] = secrets_data
        
        state = self.state
        if (state is not None):
            activity_data['state'] = state
        
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
        activity_data.update(self.bot_dict())
        
        # spotify only
        flags = self.flags
        if flags:
            activity_data['flags'] = flags
        
        # spotify only
        session_id = self.session_id
        if (session_id is not None):
            activity_data['session_id'] = session_id
        
        # spotify only
        sync_id = self.sync_id
        if (sync_id is not None):
            activity_data['sync_id'] = sync_id
        
        # receive only?
        application_id = self.application_id
        if application_id:
            activity_data['application_id'] = application_id
        
        # receive only?
        activity_data['id'] = self.discord_side_id
        
        # receive only?
        created_at = self.created_at
        if created_at != DISCORD_EPOCH_START:
            activity_data['created_at'] = datetime_to_unix_time(created_at)
        
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
        
        Only applicable for stream activities.
        
        Returns
        -------
        name : `None` or `str`
        """
        if self.type != ACTIVITY_TYPES.stream:
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
        
        Only applicable for spotify activities.
        
        Returns
        -------
        duration : `None` or `timedelta`
        """
        if self.type != ACTIVITY_TYPES.spotify:
            return None
        
        timestamps = self.timestamps
        start = timestamps.start
        if start is None:
            return None
        
        end = timestamps.end
        if end is None:
            return None
        
        return end-start
    
    
    @property
    def album_cover_url(self):
        """
        Returns the spotify activity's currently playing track's album url if applicable.
        
        Only applicable for spotify activities.
        
        Returns
        -------
        album_cover_url : `None` or `str`
        """
        if self.type != ACTIVITY_TYPES.spotify:
            return None
        
        assets = self.assets
        if assets is None:
            return None
        
        image_large = assets.image_large
        if image_large is None:
            return None
            
        return f'https://i.scdn.co/image/{image_large}'
    
    
    @property
    def track_id(self):
        """
        Returns the song's identifier.
        
        Only applicable for spotify activities.
        
        Returns
        -------
        track_id : `None` or `str`
        """
        if self.type != ACTIVITY_TYPES.spotify:
            return None
        
        return self.sync_id
    
    
    @property
    def track_url(self):
        """
        Returns url to the spotify activity's song.
        
        Only applicable for spotify activities.
        
        Returns
        -------
        url : `None` or `str`
        """
        if self.type != ACTIVITY_TYPES.spotify:
            return None
        
        return f'https://open.spotify.com/track/{self.sync_id}'

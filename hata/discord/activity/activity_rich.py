__all__ = ('ActivityRich',)

from datetime import datetime

from ..color import Color
from ..preconverters import preconvert_str, preconvert_int
from ..http import urls as module_urls

from . import activity_types as ACTIVITY_TYPES
from .activity_base import ActivityBase, ACTIVITY_TYPE_NAMES, ActivityAssets, ActivityParty, ActivitySecrets, \
    ActivityTimestamps, CUSTOM_IDS
from .flags import ActivityFlag

ACTIVITY_TYPE_NAME_UNKNOWN = 'unknown'


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
    
    def __new__(cls, name, url=None, type_=ACTIVITY_TYPES.game):
        """
        Creates a new activity with the given parameters.
        
        Parameters
        ----------
        name : `str`
            The name of the activity.
        url : `None`, `str`, Optional
            The url of the activity. Only twitch and youtube urls are supported.
        type_ : `int`, Optional
            The type value of the activity.
        
        Returns
        -------
        activity : ``ActivityRich``
        
        Raises
        ------
        TypeError
            If any parameter's type is bad or if unexpected parameter is passed.
        ValueError
            If an parameter's type is good, but it's value is unacceptable.
        """
        name = preconvert_str(name, 'name', 0, 2048)
        
        if (url is not None):
            url = preconvert_str(url, 'url', 0, 2048)
        
        type_ = preconvert_int(type_, 'type_', 0, 5)
        
        if type_ == ACTIVITY_TYPES.custom:
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
        
        self.details = activity_data.get('details', None)
        
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
        
        self.session_id = activity_data.get('session_id', None)
        
        self.state = activity_data.get('state', None)
        
        self.sync_id = activity_data.get('sync_id', None)
        
        try:
            timestamps_data = activity_data['timestamps']
        except KeyError:
            timestamps = None
        else:
            timestamps = ActivityTimestamps(timestamps_data)
        self.timestamps = timestamps
        
        self.url = activity_data.get('url', None)
    
    
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
            timestamps = ActivityTimestamps(timestamps_data)
        
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
        
        return datetime.utcfromtimestamp(end/1000.0) - datetime.utcfromtimestamp(start/1000.0)
    
    
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

__all__ = ('ACTIVITY_UNKNOWN', 'Activity')

import warnings

from scarletio import RichAttributeErrorBaseType

from ..color import Color
from ..http import urls as module_urls
from ..utils import DISCORD_EPOCH_START
from ..preconverters import preconvert_preinstanced_type

from .constants import ACTIVITY_CUSTOM_ID_DEFAULT, ACTIVITY_CUSTOM_IDS
from .preinstanced import ActivityType


class Activity(RichAttributeErrorBaseType):
    """
    Represents a Discord activity.
    
    Attributes
    ----------
    metadata : ``ActivityMetadataBase``
        Metadata of the activity containing extra fields about itself.
    type : ``ActivityType``
        The activity's type.
    """
    __slots__ = ('metadata', 'type')
    
    def __new__(cls, name, *, type_=None, **keyword_parameters):
        """
        Creates a new activity with the given parameters.
        
        Parameters
        ----------
        name : `str`
            The name of the activity.
        type_ : `None`, `int` = `None`, Optional (Keyword only)
            The type value of the activity.
        **keyword_parameters : Keyword parameters
            Additional parameters to pass to the activity-type specific constructor.
        
        Other Parameters
        ----------------
        application_id : `int`, Optional (Keyword only)
            The id of the activity's application.
        assets : `None`, ``ActivityAssets``, Optional (Keyword only)
             The activity's assets.
        created_at : `None`, `datetime`, Optional (Keyword only)
            When the activity was created.
        details : `None`, `str`, Optional (Keyword only)
            What the player is currently doing.
        flags : ``ActivityFlag``, `int`, Optional (Keyword only)
            The flags of the activity.
        id_ : `int`, Optional (Keyword only)
            The id of the activity.
        party : `None`, ``ActivityParty``, Optional (Keyword only)
            The activity's party.
        secrets : `None`, ``ActivitySecret``, Optional (Keyword only)
            The activity's secrets.
        session_id : `None`, `str`, Optional (Keyword only)
            Spotify activity's session's id.
        state : `None`, `str`, Optional (Keyword only)
            The player's current party status.
        sync_id : `None`, `str`, Optional (Keyword only)
            The ID of the currently playing track of a spotify activity.
        timestamps : ``ActivityTimestamps``, Optional (Keyword only)
            The activity's timestamps.
        url : `None`, `str`, Optional (Keyword only)
            The url of the activity. Only twitch and youtube urls are supported.
        
        Returns
        -------
        activity : ``Activity``
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
            - If extra or unused parameters were given.
        ValueError
            - If a parameter's value is incorrect.
        """
        if type_ is None:
            type_ = ActivityType.game
        else:
            type_ = preconvert_preinstanced_type(type_, 'type_', ActivityType)
        
        keyword_parameters['name'] = name
        metadata = type_.metadata_type(keyword_parameters)
        
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused parameters: {keyword_parameters!r}.'
            )
        
        self = object.__new__(cls)
        self.metadata = metadata
        self.type = type_
        return self
    
    
    def __hash__(self):
        """Returns the activity's hash value."""
        hash_value = 0
        
        # metadata
        hash_value ^= hash(self.metadata)
        
        # type
        hash_value ^= self.type.value
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two activities are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # metadata
        if self.metadata != other.metadata:
            return False
        
        # type
        if self.type != other.type:
            return False
        
        return True
    
    
    def __repr__(self):
        """Returns the activity's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # type
        type_ = self.type
        repr_parts.append(' type=')
        repr_parts.append(type_.name)
        repr_parts.append('~')
        repr_parts.append(repr(type_.value))
        
        # metadata
        repr_parts.append(', metadata=')
        repr_parts.append(repr(self.repr_parts))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates an activity from the json data sent by Discord.
        
        If the data is `None` returns `ACTIVITY_UNKNOWN`.
        
        Parameters
        ----------
        data : `None`, `dict` of (`str`, `Any`) items
            Activity data received from Discord.
        
        Returns
        -------
        activity : ``Activity``
        """
        if data is None:
            return ACTIVITY_UNKNOWN
        
        type_ = ActivityType.get(data.get('type', 0))
        metadata = type_.metadata_type.from_data(data)
        
        self = object.__new__(cls)
        self.metadata = metadata
        self.type = type_
        return self
    
    def to_data(self):
        """
        Converts the activity to json serializable dictionary, which can be sent with bot account to change activity.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = self.metadata.to_data()
        data['type'] = self.type.value
        return data
    
    
    def to_data_user(self):
        """
        Converts the activity to json serializable dictionary, which can (?) be sent with user account to change
        activity.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = self.metadata.to_data_user()
        data['type'] = self.type.value
        return data
    
    
    def to_data_full(self):
        """
        Converts the whole activity to a dictionary.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = self.metadata.to_data_full()
        data['type'] = self.type.value
                
        # id | receive only?
        data['id'] = self.discord_side_id
        
        return data
    
    
    def bot_dict(self):
        """
        Deprecated and will be removed in 2023 Jan, please use ``.to_data`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.bot_dict` is deprecated and will be removed in 2023 Jan. '
                f'Please use `.to_data` instead.'
            ),
            FutureWarning,
        )
        
        return self.to_data()
    
    
    def user_dict(self):
        """
        Deprecated and will be removed in 2023 Jan, please use ``.to_data_user`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.user_dict` is deprecated and will be removed in 2023 Jan. '
                f'Please use `.to_data_user` instead.'
            ),
            FutureWarning,
        )
        
        return self.to_data_user()
    
    
    def full_dict(self):
        """
        Deprecated and will be removed in 2023 Jan, please use ``.to_data_full`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.full_dict` is deprecated and will be removed in 2023 Jan. '
                f'Please use `.to_data_full` instead.'
            ),
            FutureWarning,
        )
        
        return self.to_data_full()
    
    
    def _update_attributes(self, data):
        """
        Updates the activity by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        """
        type_ = ActivityType.get(data.get('type', 0))
        self.type = type_
        
        metadata_type = type_.metadata_type
        metadata = self.metadata
        
        if type(metadata) is metadata_type:
            metadata._update_attributes(data)
        else:
            self.metadata = metadata_type.from_data(data)
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the activity and returns the changes in a `dict` of (`attribute-name`, `old-value`) items.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
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
        | assets            | `None`, ``ActivityAssets``        |
        +-------------------+-----------------------------------+
        | created_at        | `None`, `datetime`                |
        +-------------------+-----------------------------------+
        | details           | `None`, `str`                     |
        +-------------------+-----------------------------------+
        | emoji             | `None`, ``Emoji``                 |
        +-------------------+-----------------------------------+
        | flags             | ``ActivityFlag``                  |
        +-------------------+-----------------------------------+
        | name              | `str`                             |
        +-------------------+-----------------------------------+
        | party             | `None`, ``ActivityParty``         |
        +-------------------+-----------------------------------+
        | secrets           | `None`, ``ActivitySecrets``       |
        +-------------------+-----------------------------------+
        | session_id        | `None`, `str`                     |
        +-------------------+-----------------------------------+
        | state             | `None`, `str`                     |
        +-------------------+-----------------------------------+
        | sync_id           | `None`, `str`                     |
        +-------------------+-----------------------------------+
        | timestamps        | `None`, `ActivityTimestamps``     |
        +-------------------+-----------------------------------+
        | type              | ``ActivityType``                  |
        +-------------------+-----------------------------------+
        | url               | `None`, `str`                     |
        +-------------------+-----------------------------------+
        """
        type_ = ActivityType.get(data.get('type', 0))
        metadata_type = type_.metadata_type
        metadata = self.metadata
        if type(metadata) is metadata_type:
            old_attributes = metadata._difference_update_attributes(data)
        else:
            # If we edit the metadata type, we should just ignore the changes. This should be checked beforehand.
            self.metadata = metadata_type.from_data(data)
            old_attributes = {}
        
        if type_ is not self.type:
            old_attributes['type'] = self.type
            self.type = type_
        
        return old_attributes
    
    
    # Field proxies
    
    @property
    def created_at(self):
        """
        Returns when the activity was created.
        
        Returns
        -------
        created_at : `datetime`
        """
        created_at = self.metadata.created_at
        if (created_at is None):
            created_at = DISCORD_EPOCH_START
        
        return created_at
    
    
    @property
    def emoji(self):
        """
        Returns the emoji of the activity. If it has no emoji, then set as `None`.
        
        Returns
        -------
        emoji : `None`, ``Emoji``
        """
        return self.metadata.emoji
    
    
    @property
    def id(self):
        """
        Returns the activity's id.
        
        Returns
        -------
        id : `int`
        """
        return self.metadata.id
    
    
    @property
    def name(self):
        """
        Returns the activity's name.
        
        Returns
        -------
        name : `str`
        """
        return self.metadata.name
    
    
    @property
    def state(self):
        """
        Returns the activity's state.
        
        > If the activity has ``.emoji`` it appears next to it.
        
        Returns
        -------
        state : `None`, `str`
        """
        return self.metadata.state
    
    # Properties
    

    @property
    def color(self):
        """
        Returns the activity's color.
        
        Returns
        -------
        color : ``Color``
        """
        type_ = self.type
        if type_ is ActivityType.game:
            return Color(0x7289da)
        
        if type_ is ActivityType.stream:
            if self.url is None:
                return Color(0x7289da)
            else:
                return Color(0x593695)
        
        if type_ is ActivityType.spotify:
            return Color(0x1db954)
        
        if type_ is ActivityType.watching:
            return Color(0x7289da)
        
        return Color()
    
    
    @property
    def discord_side_id(self):
        """
        Returns the activity's Discord side id. If the activity implements id returns that, else tries to look it put
        from constants.
        
        Returns
        -------
        discord_side_id : `str`
        """
        id_ = self.id
        if id_:
            discord_side_id = format(self.id, 'x')
        else:
            discord_side_id = ACTIVITY_CUSTOM_IDS.get(self.type, ACTIVITY_CUSTOM_ID_DEFAULT)
        
        return discord_side_id
    

    
    @property
    def twitch_name(self):
        """
        If the user streams on twitch, returns it's twitch name.
        
        Only applicable for stream activities.
        
        Returns
        -------
        name : `None`, `str`
        """
        if self.type is not ActivityType.stream:
            return None
        
        assets = self.assets
        if assets is None:
            return None
        
        image_large = assets.image_large
        if image_large is None:
            return None
        
        if not image_large.startswith('twitch:'):
            return None
        
        return image_large[len('twitch:'):]
    
    
    @property
    def twitch_preview_image_url(self):
        """
        Returns the activity's twitch preview image url.
        
        Only applicable for stream activities.
        
        Returns
        -------
        preview_image_url : `None`, `str`
        """
        twitch_name = self.twitch_name
        if (twitch_name is not None):
            return f'https://static-cdn.jtvnw.net/previews-ttv/live_user_{twitch_name}.png'
    
    
    @property
    def youtube_video_id(self):
        """
        If the user streams on youtube, returns it's stream's respective video identifier.
        
        Only applicable for stream activities.
        
        Returns
        -------
        video_id : `None`, `str`
        """
        if self.type is not ActivityType.stream:
            return None
        
        assets = self.assets
        if assets is None:
            return None
        
        image_large = assets.image_large
        if image_large is None:
            return None
        
        if not image_large.startswith('youtube:'):
            return None
        
        return image_large[len('youtube:'):]
    
    
    @property
    def youtube_preview_image_url(self):
        """
        Returns the activity's youtube preview image url.
        
        Only applicable for stream activities.
        
        Returns
        -------
        preview_image_url : `None`, `str`
        """
        youtube_video_id = self.youtube_video_id
        if (youtube_video_id is not None):
            return f'https://i.ytimg.com/vi/{youtube_video_id}/hqdefault_live.jpg'
    
    
    @property
    def duration(self):
        """
        Drops a deprecation warning and returns ``.spotify_track_duration``.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.duration` is deprecated and will be removed in 2022 December. '
                f'Please use `.spotify_track_duration` instead.'
            ),
            FutureWarning,
            stacklevel = 2
        )
        return self.spotify_track_duration
    
    
    @property
    def spotify_track_duration(self):
        """
        Returns the spotify activity's duration, or `None` if not applicable.
        
        Only applicable for spotify activities.
        
        Returns
        -------
        duration : `None`, `timedelta`
        """
        if self.type is not ActivityType.spotify:
            return None
        
        timestamps = self.timestamps
        start = timestamps.start
        if start is None:
            return None
        
        end = timestamps.end
        if end is None:
            return None
        
        return end - start
    
    
    @property
    def spotify_cover_id(self):
        """
        If the user listens to spotify, returns it's spotify name.
        
        Only applicable for spotify activities.
        
        Returns
        -------
        name : `None`, `str`
        """
        if self.type is not ActivityType.spotify:
            return None
        
        assets = self.assets
        if assets is None:
            return None
        
        image_large = assets.image_large
        if image_large is None:
            return None
        
        if not image_large.startswith('spotify:'):
            return None
        
        return image_large[len('spotify:'):]
    
    
    @property
    def spotify_album_cover_url(self):
        """
        Returns the spotify activity's currently playing track's album's cover url if applicable.
        
        Only applicable for spotify activities.
        
        Returns
        -------
        album_cover_url : `None`, `str`
        """
        spotify_cover_id = self.spotify_cover_id
        if (spotify_cover_id is not None):
            return f'https://i.scdn.co/image/{spotify_cover_id}'
    
    
    @property
    def album_cover_url(self):
        """
        Drops a deprecation warning and returns ``.spotify_album_cover_url``.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.album_cover_url` is deprecated and will be removed in 2022 December. '
                f'Please use `.spotify_album_cover_url` instead.'
            ),
            FutureWarning,
            stacklevel = 2
        )
        return self.spotify_album_cover_url
    
    
    @property
    def track_id(self):
        """
        Returns the song's identifier.
        
        Only applicable for spotify activities.
        
        Returns
        -------
        track_id : `None`, `str`
        """
        if self.type is not ActivityType.spotify:
            return None
        
        return self.sync_id
    
    
    @property
    def track_url(self):
        """
        Returns url to the spotify activity's song.
        
        Only applicable for spotify activities.
        
        Returns
        -------
        url : `None`, `str`
        """
        if self.type is not ActivityType.spotify:
            return None
        
        return f'https://open.spotify.com/track/{self.sync_id}'
    
    image_large_url = property(module_urls.activity_asset_image_large_url)
    image_large_url_as = module_urls.activity_asset_image_large_url_as
    image_small_url = property(module_urls.activity_asset_image_small_url)
    image_small_url_as = module_urls.activity_asset_image_small_url_as
    
    
    @property
    def start(self):
        """
        Returns when the activity was started if applicable.
        
        Returns
        -------
        start : `None`, `datetime`
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
        start : `None`, `datetime`
        """
        timestamps = self.timestamps
        if (timestamps is not None):
            return timestamps.end


ACTIVITY_UNKNOWN = Activity('', type_=ActivityType.unknown)
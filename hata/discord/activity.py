# -*- coding: utf-8 -*-
__all__ = ( 'ActivityBase', 'ActivityCustom', 'ActivityFlag', 'ActivityGame', 'ActivityRich', 'ActivitySpotify',
    'ActivityStream', 'ActivityUnknown', 'ActivityWatching', )

from datetime import datetime

from .bases import FlagBase
from .color import Color
from .http import URLS

PartialEmoji=NotImplemented

class ActivityFlag(FlagBase):
    """
    The flags of an activity provided by Discord. These flags supposed to describe what the activity's payload
    includes.
    
    There is one predefined activity created, because ``ActivitySpotify``-s always have the same flags.
    
    +-----------------------+-------------------+
    | Class attribute name  | value             |
    +=======================+===================+
    | spotify               | ActivityFlag(48)  |
    +-----------------------+-------------------+
    """
    __keys__ = {
        'INSTANCE'    : 0,
        'JOIN'        : 1,
        'SPECTATE'    : 2,
        'JOIN_REQUEST': 3,
        'SYNC'        : 4,
        'PLAY'        : 5,
            }
    
    spotify = NotImplemented

ActivityFlag.spotify = ActivityFlag(48)

class ActivityBase(object):
    """
    Base class for activites. This class should not be instanced.
    
    Contains general methods used arround it's subclasses. And can be used for `isinstance` checks as well.
    
    Class Attributes
    ----------------
    DATA_SIZE_LIMIT : `int` = `3`
        Tells over how much data an activity will be created as `ActivityRich` over sub-activity-types.
    ACTIVITY_FLAG : `int` = `0b0000000000000000`
        Represents which attribute groups the activity type implements. These are:
        
        +----------------+--------------------+
        | group name     | binary value       |
        +================+====================+
        | timestamps     | 0b0000000000000001 |
        +----------------+--------------------+
        | details        | 0b0000000000000010 |
        +----------------+--------------------+
        | state          | 0b0000000000000100 |
        +----------------+--------------------+
        | party          | 0b0000000000001000 |
        +----------------+--------------------+
        | asset          | 0b0000000000010000 |
        +----------------+--------------------+
        | secret         | 0b0000000000100000 |
        +----------------+--------------------+
        | url            | 0b0000000001000000 |
        +----------------+--------------------+
        | sync_id        | 0b0000000010000000 |
        +----------------+--------------------+
        | session_id     | 0b0000000100000000 |
        +----------------+--------------------+
        | flags          | 0b0000001000000000 |
        +----------------+--------------------+
        | application_id | 0b0000010000000000 |
        +----------------+--------------------+
        | emoji          | 0b0000100000000000 |
        +----------------+--------------------+
        | id             | 0b0001000000000000 |
        +----------------+--------------------+
        
        These flags are not same as ``ActivityFlag`` and this value is neither `activity.flags`.
    
    color : ``Color`` = `Color(0)
        The color of the activity. Subclasses might overwrite it even as a property.
    name : `str` = `'Unknown'`
        The activity's name. Subclasses might overwrite it as member descriptor.
    id : `int` = `0`
        The activity's id. Subclasses might overwrite it as member descriptor.
    """
    __slots__=()
    
    DATA_SIZE_LIMIT = 3
    #timestamps     = 0b0000000000000001
    #details        = 0b0000000000000010
    #state          = 0b0000000000000100
    #party          = 0b0000000000001000
    #asset          = 0b0000000000010000
    #secret         = 0b0000000000100000
    #url            = 0b0000000001000000
    #sync_id        = 0b0000000010000000
    #session_id     = 0b0000000100000000
    #flags          = 0b0000001000000000
    #application_id = 0b0000010000000000
    #emoji          = 0b0000100000000000
    #id             = 0b0001000000000000
    ACTIVITY_FLAG   = 0b0000000000000000
    
    color           = Color(0)
    name            = 'Unknown'
    id              = 0
    
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
        """Returns the acitvity's name."""
        return self.name
    
    def __hash__(self):
        """Returns the activity's hash value."""
        return self.id
    
    def __repr__(self):
        """Returns the activity's representation."""
        return f'<{self.__class__.__name__} name={self.name!r}>'
    
    def __eq__(self,other):
        """Compares whether the two ``ActivityBase`` instance's `.type` and `.id`."""
        if isinstance(other, ActivityBase):
            return self.type==other.type and self.id==other.id
        return NotImplemented
    
    @property
    def type(self):
        """
        The type of an unknown activity is `-1`.
        
        Returns
        -------
        type : `int` = `-1`
        """
        return -1
    
    @property
    def created(self):
        """
        When the status was created as Unix time in milliseconds. Defaults to `0`.
        
        Returns
        -------
        created : `int` = 0
        """
        return 0
    
    @property
    def discord_side_id(self):
        """
        Returns the activity's Discord side id. If the activity implements id returns that, else returns it's
        `CUSTOM_ID` class attribute.
        
        Returns
        -------
        activity_id : `str`
        """
        if self.ACTIVITY_FLAG&0b0001000000000000:
            return self.id.__format__('0>16x')
        return self.CUSTOM_ID
    
    @classmethod
    def create(cls):
        """
        Returns an activity with the given attributes. Neither ``ActivityBase`` or it's subclasses: ``ActivityUnknown``
        and `ActivityCustom` cannot be created like this and they raise `RuntimeError`.
        
        Raises
        ------
        RuntimeError
        """
        raise RuntimeError(f'{cls.__name__} cannot be instanced.')
    
    def botdict(self):
        """
        Converts the activity to json serializible dictionary, which can be sent with bot account to change activity.
        
        Returns
        -------
        activity_data : `dict` of (`str`, `Any`) items
        """
        data = {
            'type':self.type,
                }
        
        if self.type==4:
            name='Custom Status'
        else:
            name=self.name
        data['name']=name
        
        if self.ACTIVITY_FLAG&0b0000000001000000:
            url=self.url
            if url:
                data['url']=url

        return data
    
    def hoomandict(self):
        """
        Converts the activity to json serializible dictionary, which can (?) be sent with user account to change
        activity.
        
        Returns
        -------
        activity_data : `dict` of (`str`, `Any`) items
        """
        data=self.botdict()
        
        ACTIVITY_FLAG=self.ACTIVITY_FLAG
        if ACTIVITY_FLAG&0b0000000000000001:
            timestamps_data={}
            
            timestamp_start=self.timestamp_start
            if timestamp_start:
                timestamps_data['start']=timestamp_start
                
            timestamp_end=self.timestamp_end
            if timestamp_end:
                timestamps_data['end']=timestamp_end
            
            if timestamps_data:
                data['timestamps']=timestamps_data
            
        if ACTIVITY_FLAG&0b0000000000000010:
            details=self.details
            if details:
                data['details']=details

        if ACTIVITY_FLAG&0b0000000000000100:
            state=self.state
            if state is not None:
                data['state']=state

        if self.ACTIVITY_FLAG&0b0000000000001000:
            party_data={}
            
            party_id=self.party_id
            if party_id:
                party_data['id']=party_id
            
            party_size=self.party_size
            if party_size:
                party_data['size']=[party_size,self.party_max]
            
            if party_data:
                data['party']=party_data
        
        if self.ACTIVITY_FLAG&0b0000000000010000:
            assets_data={}
            
            asset_image_large=self.asset_image_large
            if asset_image_large:
                assets_data['large_image']=asset_image_large
            
            asset_image_small=self.asset_image_small
            if asset_image_small:
                assets_data['small_image']=asset_image_small
            
            asset_text_large=self.asset_text_large
            if asset_text_large:
                assets_data['large_text']=asset_text_large
            
            asset_text_small=self.asset_text_small
            if asset_text_small:
                assets_data['small_text']=asset_text_small
            
            if assets_data:
                data['assets']=assets_data

        if self.ACTIVITY_FLAG&0b0000000000100000:
            secrets_data={}
            
            secret_join=self.secret_join
            if secret_join:
                secrets_data['join']=secret_join
            
            secret_spectate=self.secret_spectate
            if secret_spectate:
                secrets_data['spectate']=secret_spectate
            
            secret_match=self.secret_match
            if secret_match:
                secrets_data['match']=secret_match
                
            if secrets_data:
                data['secrets']=secrets_data
            
        if ACTIVITY_FLAG&0b0000000001000000:
            url=self.url
            if url:
                data['url']=url
        
        if ACTIVITY_FLAG&0b0000000010000000:
            sync_id=self.sync_id
            if sync_id:
                data['sync_id']=sync_id
        
        if ACTIVITY_FLAG&0b0000000100000000:
            session_id=self.session_id
            if session_id:
                data['session_id']=session_id

        if ACTIVITY_FLAG&0b0000001000000000:
            flags=self.flags
            if flags:
                data['flags']=flags

        if ACTIVITY_FLAG&0b0000010000000000:
            application_id=self.application_id
            if application_id:
                data['application_id']=application_id
        
        if ACTIVITY_FLAG&0b0000100000000000:
            emoji=self.emoji
            if emoji is not None:
                emoji_data={}
                if emoji.is_custom_emoji():
                    emoji_data['name']=emoji.name
                    emoji_data['id']=emoji.id
                    if emoji.animated:
                        emoji_data['animated']=True
                else:
                    emoji_data['name']=emoji.unicode
                data['emoji']=emoji_data
            
        return data
    
    def fulldict(self):
        """
        Converts the whole activity to a dictionary.
        
        Returns
        -------
        activity_data : `dict` of (`str`, `Any`) items
        """
        data=self.hoomandict()

        #receive only?
        data['id']=self.discord_side_id
        
        #receive only?
        created=self.created
        if created:
            data['created_at']=created
        
        return data
    
    @property
    def created_at(self):
        """
        When the activity was created. If the creation time was not included, will return `None`.
        
        Returns
        -------
        created_at : `None` or `datetime`
        """
        created = self.created
        if created==0:
            return None
        
        return datetime.utcfromtimestamp(created/1000.)

    
    def _update(self, data):
        """
        Updates the activity and returns the changes in a `dict` of (`attribute-name`, `old-value`) items.
        
        This method is just a placeholder of this type and should never be called normally.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.

        Returns
        -------
        changes : `dict`
            Always empty.
        """
        return {}
    
    def _update_no_return(self, data):
        """
        Updates the activity by overwriting it's old attributes.
        
        This method is just a placeholder of this type and should never be called normally.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        """
        pass

class ActivityRich(ActivityBase):
    """
    Represents a Discord rich activity. It can be used instead of any other activity type. By default used, when
    an activity's data is received, what's length passes it's specific activity type's `.DATA_SIZE_LIMIT`.
    
    Attributes
    ----------
    application_id : `int`
        The id of the activity's application. Defaults to `0`.
        > Bound to `ACTIVITY_FLAG&0b0000010000000000` (application_id).
    asset_image_large : `str`
        The id of the activity's large asset to display. Defaults to empty string.
        > Bound to `ACTIVITY_FLAG&0b0000000000010000` (asset).
    asset_image_small : `str`
        The id of the activity's small asset to display. Defaults to empty string.
        > Bound to `ACTIVITY_FLAG&0b0000000000010000` (asset).
    asset_text_large : `str`
        The hover text of the large asset. Defaults to empty string.
        > Bound to `ACTIVITY_FLAG&0b0000000000010000` (asset).
    asset_text_small : `str`
        The hover text of the small asset. Defaults to empty string.
        > Bound to `ACTIVITY_FLAG&0b0000000000010000` (asset).
    created : `int`
        When the status was created as Unix time in milliseconds. Defaults to `0`.
    details : `str`
        What the player is currently doing.
        > Bound to `ACTIVITY_FLAG&0b00000000000000010` (details).
    emoji : `None` or ``Emoji``
        The emoji used for ``ActivityCustom``.
        > Bound to `ACTIVITY_FLAG&0b0000100000000000` (emoji).
    flags : ``ActivityFlag``
        The flags of the activity. Defaults to `ActivityFlag(0)`
        > Bound to `ACTIVITY_FLAG&0b0000001000000000` (flags).
    id : `int`
        The id of the activity. Defaults to `0`.
        > Bound to `ACTIVITY_FLAG&0b0001000000000000` (id)
    name : `str`
        The activity's name.
    party_id : `str`
        The party's id, which in the player is. Defaults to empty string.
        > Bound to `ACTIVITY_FLAG&0b0000000000001000` (party).
    party_max : `int`
        The party's maximal size, which in the player is. Defaults to `0`.
        > Bound to `ACTIVITY_FLAG&0b0000000000001000` (party).
    party_size : `int`
        The party's actual size, which in the player is. Defaults to `0`.
        > Bound to `ACTIVITY_FLAG&0b0000000000001000` (party).
    secret_join : `str`
        Unique hash given for the match context. Defaults to empty string.
        > Bound to `ACTIVITY_FLAG&0b0000000000100000` (secret).
    secret_match : `str`
        Unique hash for spectate button. Defaults to empty string.
        > Bound to `ACTIVITY_FLAG&0b0000000000100000` (secret).
    secret_spectate : `str`
        Unique hash for chat invites and ask to join. Defaults to empty string.
        > Bound to `ACTIVITY_FLAG&0b0000000000100000` (secret).
    session_id : `str`
        The ``ActivitySpotify``'s session's id. Defaults to empty string.
    state : `str` or `None`
        The player's current party status. Defaults to `None`.
        > Bound to `ACTIVITY_FLAG&0b0000000000000100` (state).
    sync_id : `str`
        The ID of the currently playing track. Used at ``ActivitySpotify``. Defaults to empty string.
        > Bound to `ACTIVITY_FLAG&0b0000000010000000` (sync_id).
    timestamp_end : `int`
        The time when the activity ends as Unix time in milliseconds. Defaults to `0`.
        > Bound to `ACTIVITY_FLAG&0b0000000000000001` (timestamps).
    timestamp_start : `int`
        The time when the activity starts as Unix time in milliseconds. Defaults to `0`.
        > Bound to `ACTIVITY_FLAG&0b0000000000000001` (timestamps).
    type : `int`
        An integer, what represent the activity's type for Discord. Can be one of: `0`, `1`, `2`, `3`, `4`.
    url : `str`
        The url of the stream (Twitch only). Defaults to empty string.
        > Bound to `ACTIVITY_FLAG&0b0000000001000000` (url).
    
    Class Attributes
    ----------------
    DATA_SIZE_LIMIT : `int` = `16`
        Tells over how much data an activity will be created as `ActivityRich` over sub-activity-types.
    ACTIVITY_FLAG : `int` = `0b0001111111111111`
        Represents which attribute groups the activity type implements.
    """
    __slots__ = ('application_id', 'asset_image_large', 'asset_image_small', 'asset_text_large', 'asset_text_small',
        'created', 'details', 'emoji', 'flags', 'id', 'name', 'party_id', 'party_max', 'party_size', 'secret_join',
        'secret_match', 'secret_spectate', 'session_id', 'state', 'sync_id', 'timestamp_end', 'timestamp_start',
        'type', 'url', )
    
    DATA_SIZE_LIMIT = 16
    #timestamps     = 0b0000000000000001
    #details        = 0b0000000000000010
    #state          = 0b0000000000000100
    #party          = 0b0000000000001000
    #asset          = 0b0000000000010000
    #secret         = 0b0000000000100000
    #url            = 0b0000000001000000
    #sync_id        = 0b0000000010000000
    #session_id     = 0b0000000100000000
    #flags          = 0b0000001000000000
    #application_id = 0b0000010000000000
    #emoji          = 0b0000100000000000
    #id             = 0b0001000000000000
    ACTIVITY_FLAG   = 0b0001111111111111
    
    def __new__(cls, data):
        """
        Creates an ``ActivityRich`` instance from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Activity data received from Discord.
            
        Returns
        -------
        activity : ``ActivityRich``
        """
        self = object.__new__(cls)
        self._update_no_return(data)
        return self
    
    @property
    def color(self):
        """
        The color of the activity.
        
        Returns
        -------
        color : ``Color``
        """
        return ACTIVITY_TYPES[self.type].color
    
    def _update_no_return(self, data):
        """
        Updates the activity by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        """
        self.name=data['name']
        
        self.type=data['type']
        
        try:
            self.application_id=int(data['application_id'])
        except KeyError:
            self.application_id=0
        
        try:
            timestamp_data=data['timestamps']
        except KeyError:
            self.timestamp_end=0
            self.timestamp_start=0
        else:
            self.timestamp_end=timestamp_data.get('end',0)
            self.timestamp_start=timestamp_data.get('start',0)

        self.details=data.get('details','')
        
        self.state=data.get('state',None)

        try:
            party_data=data['party']
        except KeyError:
            self.party_id=''
            self.party_size=self.party_max=0
        else:
            self.party_id=party_data.get('id','')
            try:
                self.party_size,self.party_max=data['size']
            except KeyError:
                self.party_size=self.party_max=0
        
        try:
            asset_data=data['assets']
        except KeyError:
            self.asset_image_large=''
            self.asset_image_small=''
            self.asset_text_large=''
            self.asset_text_small=''
        else:
            self.asset_image_large=asset_data.get('large_image','')
            self.asset_image_small=asset_data.get('small_image','')
            self.asset_text_large=asset_data.get('large_text','')
            self.asset_text_small=asset_data.get('small_text','')
        
        try:
            secret_data=data['secrets']
        except KeyError:
            self.secret_join=''
            self.secret_spectate=''
            self.secret_match=''
        else:
            self.secret_join=secret_data.get('join','')
            self.secret_spectate=secret_data.get('spectate','')
            self.secret_match=secret_data.get('match','')

        self.url=data.get('url','')

        self.sync_id=data.get('sync_id','')
        
        self.session_id=data.get('session_id','')
        
        self.flags=ActivityFlag(data.get('flags',0))
        
        emoji_data=data.get('emoji',None)
        if emoji_data is None:
            emoji=None
        else:
            emoji=PartialEmoji(emoji_data)
        self.emoji=emoji
        
        self.created=data.get('created_at',0)
        
        if ACTIVITY_TYPES[self.type].ACTIVITY_FLAG&0b0001000000000000:
            id_=int(data['id'],base=16)
        else:
            id_=0
        self.id=id_
    
    def _update(self, data):
        """
        Updates the activity and returns the changes in a `dict` of (`attribute-name`, `old-value`) items.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        
        Returns
        -------
        changes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +-----------------------+-----------------------+
        | key                   | value                 |
        +=======================+=======================+
        | application_id        | `int`                 |
        +-----------------------+-----------------------+
        | asset_image_large     | `str`                 |
        +-----------------------+-----------------------+
        | asset_image_small     | `str`                 |
        +-----------------------+-----------------------+
        | asset_text_large      | `str`                 |
        +-----------------------+-----------------------+
        | asset_text_small      | `str`                 |
        +-----------------------+-----------------------+
        | created               | `int`                 |
        +-----------------------+-----------------------+
        | details               | `str`                 |
        +-----------------------+-----------------------+
        | emoji                 | ``Emoji`` / `None`    |
        +-----------------------+-----------------------+
        | flags                 | ``ActivityFlag``      |
        +-----------------------+-----------------------+
        | id                    | `int`                 |
        +-----------------------+-----------------------+
        | name                  | `str`                 |
        +-----------------------+-----------------------+
        | party_id              | `str`                 |
        +-----------------------+-----------------------+
        | party_max             | `int`                 |
        +-----------------------+-----------------------+
        | party_size            | `int`                 |
        +-----------------------+-----------------------+
        | secret_join           | `str`                 |
        +-----------------------+-----------------------+
        | secret_match          | `str`                 |
        +-----------------------+-----------------------+
        | secret_spectate       | `str`                 |
        +-----------------------+-----------------------+
        | session_id            | `str`                 |
        +-----------------------+-----------------------+
        | state                 | `str` / `None`        |
        +-----------------------+-----------------------+
        | sync_id               | `str`                 |
        +-----------------------+-----------------------+
        | timestamp_end         | `int`                 |
        +-----------------------+-----------------------+
        | timestamp_start       | `int`                 |
        +-----------------------+-----------------------+
        | type                  | `int`                 |
        +-----------------------+-----------------------+
        | url                   | `str`                 |
        +-----------------------+-----------------------+
        """
        old={}
        
        name=data['name']
        if self.name!=name:
            old['name']=self.name
            self.name=name
        
        type_=data['type']
        if self.type!=type_:
            old['type']=self.type
            self.type=type_
        
        try:
            application_id=int(data['application_id'])
        except KeyError:
            application_id=0
            
        if self.application_id!=application_id:
            old['application_id']=self.application_id
            self.application_id=application_id
            
        try:
            timestamp_data=data['timestamps']
        except KeyError:
            timestamp_end=0
            timestamp_start=0
        else:
            timestamp_end=timestamp_data.get('end',0)
            timestamp_start=timestamp_data.get('start',0)
            
        if self.timestamp_end!=timestamp_end:
            old['timestamp_end']=self.timestamp_end
            self.timestamp_end=timestamp_end
        
        if self.timestamp_start!=timestamp_start:
            old['timestamp_start']=self.timestamp_start
            self.timestamp_start=timestamp_start

        details=data.get('details','')
        if self.details!=details:
            old['details']=self.details
            self.details=details

        state=data.get('state',None)
        if (self.state is None):
            if (state is not None):
                old['state']=None
                self.state=state
        else:
            if (state is None):
                old['state']=self.state
                self.state=None
            elif (self.state!=state):
                old['state']=self.state
                self.state=state
        
        try:
            party_data=data['party']
        except KeyError:
            party_id=''
            party_size=party_max=0
        else:
            party_id=party_data.get('id','')
            try:
                party_size,party_max=party_data['size']
            except KeyError:
                party_size=party_max=0
                
        if self.party_id!=party_id:
            old['party_id']=self.party_id
            self.party_id=party_id
            
        if self.party_size!=party_size:
            old['party_size']=self.party_size
            self.party_size=party_size
            
        if self.party_max!=party_max:
            old['party_max']=self.party_max
            self.party_max=party_max

        try:
            asset_data=data['assets']
        except KeyError:
            asset_image_large=''
            asset_image_small=''
            asset_text_large=''
            asset_text_small=''
        else:
            asset_image_large=asset_data.get('large_image','')
            asset_image_small=asset_data.get('small_image','')
            asset_text_large=asset_data.get('large_text','')
            asset_text_small=asset_data.get('small_text','')
            
        if self.asset_image_large!=asset_image_large:
            old['asset_image_large']=self.asset_image_large
            self.asset_image_large=asset_image_large
            
        if self.asset_image_small!=asset_image_small:
            old['asset_image_small']=self.asset_image_small
            self.asset_image_small=asset_image_small
            
        if self.asset_text_large!=asset_text_large:
            old['asset_text_large']=self.asset_text_large
            self.asset_text_large=asset_text_large
            
        if self.asset_text_small!=asset_text_small:
            old['asset_text_small']=self.asset_text_small
            self.asset_text_small=asset_text_small
            
        try:
            secret_data=data['secrets']
        except KeyError:
            secret_join=''
            secret_spectate=''
            secret_match=''
        else:
            secret_join=secret_data.get('join','')
            secret_spectate=secret_data.get('spectate','')
            secret_match=secret_data.get('match','')
        
        if self.secret_join!=secret_join:
            old['secret_join']=self.secret_join
            self.secret_join=self.secret_join
            
        if self.secret_spectate!=secret_spectate:
            old['secret_spectate']=self.secret_spectate
            self.secret_spectate=secret_spectate
            
        if self.secret_match!=secret_match:
            old['secret_match']=self.secret_match
            self.secret_match=secret_match

        url=data.get('url','')
        if self.url!=url:
            old['url']=self.url
            self.url=url

        sync_id=data.get('sync_id','')
        if self.sync_id!=sync_id:
            old['sync_id']=self.sync_id
            self.sync_id=sync_id
                
        session_id=data.get('session_id','')
        if self.session_id!=session_id:
            old['session_id']=self.session_id
            self.session_id=session_id
        
        flags=ActivityFlag(data.get('flags',0))
        if self.flags!=flags:
            old['flags']=self.flags
            self.flags=flags

        emoji_data=data.get('emoji',None)
        if emoji_data is None:
            emoji=None
        else:
            emoji=PartialEmoji(emoji_data)
        
        if (self.emoji is None):
            if (emoji is not None):
                old['emoji']=None
                self.emoji=emoji
        else:
            if (emoji is None):
                old['emoji']=self.emoji
                self.emoji=None
            elif self.emoji!=emoji:
                old['emoji']=self.emoji
                self.emoji=emoji
        
        created=data.get('created_at',0)
        if self.created!=created:
            old['created']=created
            self.created=created
    
        if ACTIVITY_TYPES[self.type].ACTIVITY_FLAG&0b0001000000000000:
            id_=int(data['id'],base=16)
        else:
            id_=0
        if self.id!=id_:
            old['id']=self.id
            self.id=id_
        
        return old
    
    @classmethod
    def create(cls, name, url='', type_=0):
        """
        Returns an activity with the given attributes. `url` is for streaming activity only (right now only twitch is
        supported). Bot account activities support only `name`, `url` and `type` parameters, so this method does like
        that as well.
        
        Parameters
        ----------
        name : `str`
            The name of the activity.
        url : `str`, Optional
            The url of the activity. Only twitch urls are supported. ``ActivityStream`` only.
        type_ : `int`, Optional
            The type value of the activity.
        
        Returns
        -------
        activity : ``ActivityRich``
        
        Raises
        ------
        ValueError
            If `type_` is not any of the accepted ones
        """
        if type_ < 0 or type_ >= len(ACTIVITY_TYPES):
            raise ValueError(f'Invalid `type_` passed, it can be between `0` and `{len(ACTIVITY_TYPES)-1}`, got {type_}.')
        
        type_reference = ACTIVITY_TYPES[type_]
        
        if type(type_reference.name) is str:
            name = ''
        
        if not (type_reference.ACTIVITY_FLAG&0b0000000001000000): #for streaming only, twitch url only!
            url = ''
        
        self = object.__new__(cls)
        self.type               = type_
        self.name               = name
        self.url                = url
        
        self.application_id     = 0
        self.timestamp_end      = 0
        self.timestamp_start    = 0
        self.details            = ''
        self.state              = None
        self.party_id           = ''
        self.party_size         = 0
        self.party_max          = 0
        self.asset_image_large  = ''
        self.asset_image_small  = ''
        self.asset_text_large   = ''
        self.asset_text_small   = ''
        self.secret_join        = ''
        self.secret_spectate    = ''
        self.secret_match       = ''
        self.sync_id            = ''
        self.session_id         = ''
        self.flags              = ActivityFlag(0)
        self.emoji              = None
        self.created            = 0
        self.id                 = 0
        
        return self
    
    def __repr__(self):
        """Returs the activity's representation."""
        return f'<{self.__class__.__name__} name={self.name!r}, type={self.type}>'
    
    @property
    def start(self):
        """
        Returns when the activity was started if applicable.
        
        Returns
        -------
        start : `None` or `datetime`
        """
        timestamp_start=self.timestamp_start
        if timestamp_start==0:
            return None
        
        return datetime.utcfromtimestamp(timestamp_start/1000.)
    
    @property
    def end(self):
        """
        Returns when the activity ended or will end if applicable.
        
        Returns
        -------
        start : `None` or `datetime`
        """
        timestamp_end=self.timestamp_end
        if timestamp_end==0:
            return None
        
        return datetime.utcfromtimestamp(timestamp_end/1000.)
    
    image_large_url=property(URLS.activity_asset_image_large_url)
    image_large_url_as=URLS.activity_asset_image_large_url_as
    image_small_url=property(URLS.activity_asset_image_small_url)
    image_small_url_as=URLS.activity_asset_image_small_url_as

class ActivityUnknown(ActivityBase):
    """
    Represents if a user has no activity set. This activity type is not a valid Discord activity.
    
    ``activity_unknown`` is a singleton with type value of `-1`.
    
    Class Attributes
    ----------------
    DATA_SIZE_LIMIT : `int` = `3`
        Tells over how much data an activity will be created as `ActivityRich` over sub-activity-types.
    ACTIVITY_FLAG : `int` = `0b0000000000000000`
        Represents which attribute groups the activity type implements.
    color : ``Color`` = `Color(0)
        The color of the activity.
    name : `str` = `'Unknown'`
        The activity's name. Subclasses might overwrite it as member descriptor.
    id : `int` = `0`
        The activity's id. Subclasses might overwrite it as member descriptor.
    """
    
    def __repr__(self):
        """Returns the activity's representation."""
        return f'<{self.__class__.__name__}>'

ActivityUnknown=object.__new__(ActivityUnknown)

class ActivityGame(ActivityBase):
    """
    Represents a Discord gaming activity.
    
    Attributes
    ----------
    application_id : `int`
        The id of the activity's application. Defaults to `0`.
    created : `int`
        When the status was created as Unix time in milliseconds. Defaults to `0`.
    flags : ``ActivityFlag``
        The flags of the activity. Defaults to `ActivityFlag(0)`
    id : `int`
        The id of the activity. Defaults to `0`.
    name : `str`
        The activity's name.
    timestamp_end : `int`
        The time when the activity ends as Unix time in milliseconds. Defaults to `0`.
    timestamp_start : `int`
        The time when the activity starts as Unix time in milliseconds. Defaults to `0`.
    
    Class Attributes
    ----------------
    DATA_SIZE_LIMIT : `int` = `7`
        Tells over how much data an activity will be created as `ActivityRich` over sub-activity-types.
    ACTIVITY_FLAG : `int` = `0b0001011000000001`
        Represents which attribute groups the activity type implements.
    color : ``Color`` = `Color(0x7289da)`
        The color of the activity.
    """
    __slots__ = ('application_id', 'created', 'flags', 'id', 'name', 'timestamp_end', 'timestamp_start', )
    DATA_SIZE_LIMIT = 7
    ACTIVITY_FLAG   = 0b0001011000000001
    
    color=Color(0x7289da)
    
    @property
    def type(self):
        """
        The type of a gaming activity is always `0`.
        
        Returns
        -------
        type : `int` = `0`
        """
        return 0

    def __new__(cls, data):
        """
        Creates an ``ActivityGame`` instance from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Activity data received from Discord.
            
        Returns
        -------
        activity : ``ActivityGame``
        """
        self = object.__new__(cls)
        self._update_no_return(data)
        return self
    
    def _update_no_return(self,data):
        """
        Updates the activity by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        """
        self.name=data['name']
        
        try:
            self.application_id=int(data['application_id'])
        except KeyError:
            self.application_id=0
        
        try:
            timestamp_data=data['timestamps']
        except KeyError:
            self.timestamp_end=0
            self.timestamp_start=0
        else:
            self.timestamp_end=timestamp_data.get('end',0)
            self.timestamp_start=timestamp_data.get('start',0)
        
        self.flags=ActivityFlag(data.get('flags',0))
        
        self.id=int(data['id'],base=16)
        
        self.created=data.get('created_at',0)
        
    def _update(self,data):
        """
        Updates the activity and returns the changes in a `dict` of (`attribute-name`, `old-value`) items.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        
        Returns
        -------
        changes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +-----------------------+-----------------------+
        | key                   | value                 |
        +=======================+=======================+
        | application_id        | `int`                 |
        +-----------------------+-----------------------+
        | created               | `int`                 |
        +-----------------------+-----------------------+
        | flags                 | ``ActivityFlag``      |
        +-----------------------+-----------------------+
        | id                    | `int`                 |
        +-----------------------+-----------------------+
        | name                  | `str`                 |
        +-----------------------+-----------------------+
        | timestamp_end         | `int`                 |
        +-----------------------+-----------------------+
        | timestamp_start       | `int`                 |
        +-----------------------+-----------------------+
        """
        old={}
        
        name=data['name']
        if self.name!=name:
            old['name']=self.name
            self.name=name
        
        try:
            application_id=int(data['application_id'])
        except KeyError:
            application_id=0
        
        if self.application_id!=application_id:
            old['application_id']=self.application_id
            self.application_id=application_id
        
        try:
            timestamp_data=data['timestamps']
        except KeyError:
            timestamp_end=0
            timestamp_start=0
        else:
            timestamp_end=timestamp_data.get('end',0)
            timestamp_start=timestamp_data.get('start',0)
        
        if self.timestamp_end!=timestamp_end:
            old['timestamp_end']=self.timestamp_end
            self.timestamp_end=timestamp_end
        
        if self.timestamp_start!=timestamp_start:
            old['timestamp_start']=self.timestamp_start
            self.timestamp_start=timestamp_start
        
        flags=ActivityFlag(data.get('flags',0))
        if self.flags!=flags:
            old['flags']=self.flags
            self.flags=flags
        
        id_=int(data['id'],base=16)
        if self.id!=id_:
            old['id']=self.id
            self.id=id_
        
        created=data.get('created_at',0)
        if self.created!=created:
            old['created']=self.created
            self.created=created
        
        return old
    
    @classmethod
    def create(cls, name):
        """
        Returns a gaming activity with the given attributes.
        
        Parameters
        ----------
        name : `str`
            The name of the activity.
        
        Returns
        -------
        activity : ``ActivityGame``
        """
        self = object.__new__(cls)
        self.name               = name
        
        self.application_id     = 0
        self.timestamp_end      = 0
        self.timestamp_start    = 0
        self.flags              = ActivityFlag(0)
        self.created            = 0
        self.id                 = 0
        
        return self
    
    @property
    def start(self):
        """
        Returns when the activity was started if applicable.
        
        Returns
        -------
        start : `None` or `datetime`
        """
        timestamp_start=self.timestamp_start
        if timestamp_start==0:
            return None
        
        return datetime.utcfromtimestamp(timestamp_start/1000.)
    
    @property
    def end(self):
        """
        Returns when the activity ended or will end if applicable.
        
        Returns
        -------
        start : `None` or `datetime`
        """
        timestamp_end=self.timestamp_end
        if timestamp_end==0:
            return None
        
        return datetime.utcfromtimestamp(timestamp_end/1000.)

class ActivityStream(ActivityBase):
    """
    Represents a Discord gaming activity.
    
    Attributes
    ----------
    asset_image_large : `str`
        The id of the activity's large asset to display. Defaults to empty string.
    asset_image_small : `str`
        The id of the activity's small asset to display. Defaults to empty string.
    asset_text_large : `str`
        The hover text of the large asset. Defaults to empty string.
    asset_text_small : `str`
        The hover text of the small asset. Defaults to empty string.
    created : `int`
        When the status was created as Unix time in milliseconds. Defaults to `0`.
    details : `str`
        What the player is currently doing.
    flags : ``ActivityFlag``
        The flags of the activity. Defaults to `ActivityFlag(0)`
    id : `int`
        The id of the activity. Defaults to `0`.
    name : `str`
        The activity's name.
    session_id : `str`
        The ``ActivitySpotify``'s session's id. Defaults to empty string.
    sync_id : `str`
        The ID of the currently playing track. Used at ``ActivitySpotify``. Defaults to empty string.
    url : `str`
        The url of the stream (Twitch only). Defaults to empty string.
    
    Class Attributes
    ----------------
    DATA_SIZE_LIMIT : `int` = `9`
        Tells over how much data an activity will be created as `ActivityRich` over sub-activity-types.
    ACTIVITY_FLAG : `int` = `0b0001000111010010`
        Represents which attribute groups the activity type implements.
    default_color : ``Color`` = `Color(0x7289da)
        The default color of the activity, when it has no `.url` included.
    """
    __slots__ = ('asset_image_large', 'asset_image_small', 'asset_text_large', 'asset_text_small', 'created',
        'details', 'flags', 'id', 'name', 'session_id', 'sync_id', 'url', )
    
    DATA_SIZE_LIMIT = 9
    #TODO: test for: flags - 0b0000001000000000
    ACTIVITY_FLAG   = 0b0001000111010010
    
    @property
    def color(self):
        """
        Returns the activity's color.
        
        Returns
        -------
        color : ``Color``
        """
        if self.url:
            return self.default_color
        else:
            return ActivityGame.color
    
    default_color=Color(0x593695)
    
    @property
    def type(self):
        """
        The type of a streaming activity is always `1`.
        
        Returns
        -------
        type : `int` = `1`
        """
        return 1
    
    def __new__(cls, data):
        """
        Creates an ``ActivityStream`` instance from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Activity data received from Discord.
            
        Returns
        -------
        activity : ``ActivityStream``
        """
        self = object.__new__(cls)
        self._update_no_return(data)
        return self
    
    def _update_no_return(self, data):
        """
        Updates the activity by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        """
        self.name=data['name']
        
        self.details=data.get('details','')
        
        try:
            asset_data=data['assets']
        except KeyError:
            self.asset_image_large=''
            self.asset_image_small=''
            self.asset_text_large=''
            self.asset_text_small=''
        else:
            self.asset_image_large=asset_data.get('large_image','')
            self.asset_image_small=asset_data.get('small_image','')
            self.asset_text_large=asset_data.get('large_text','')
            self.asset_text_small=asset_data.get('small_text','')
        
        self.url=data.get('url','')
        
        self.sync_id=data.get('sync_id','')
        
        self.session_id=data.get('session_id','')
        
        self.flags=ActivityFlag(data.get('flags',0))
        
        self.id=int(data['id'],base=16)
        
        self.created=data.get('created_at',0)
    
    def _update(self,data):
        """
        Updates the activity and returns the changes in a `dict` of (`attribute-name`, `old-value`) items.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        
        Returns
        -------
        changes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +-----------------------+-----------------------+
        | key                   | value                 |
        +=======================+=======================+
        | application_id        | `int`                 |
        +-----------------------+-----------------------+
        | asset_image_large     | `str`                 |
        +-----------------------+-----------------------+
        | asset_image_small     | `str`                 |
        +-----------------------+-----------------------+
        | asset_text_large      | `str`                 |
        +-----------------------+-----------------------+
        | asset_text_small      | `str`                 |
        +-----------------------+-----------------------+
        | created               | `int`                 |
        +-----------------------+-----------------------+
        | details               | `str`                 |
        +-----------------------+-----------------------+
        | flags                 | ``ActivityFlag``      |
        +-----------------------+-----------------------+
        | id                    | `int`                 |
        +-----------------------+-----------------------+
        | name                  | `str`                 |
        +-----------------------+-----------------------+
        | session_id            | `str`                 |
        +-----------------------+-----------------------+
        | url                   | `str`                 |
        +-----------------------+-----------------------+
        """
        old={}
        
        name=data['name']
        if self.name!=name:
            old['name']=self.name
            self.name=name
        
        details=data.get('details','')
        if self.details!=details:
            old['details']=self.details
            self.details=details
        
        try:
            asset_data=data['assets']
        except KeyError:
            asset_image_large=''
            asset_image_small=''
            asset_text_large=''
            asset_text_small=''
        else:
            asset_image_large=asset_data.get('large_image','')
            asset_image_small=asset_data.get('small_image','')
            asset_text_large=asset_data.get('large_text','')
            asset_text_small=asset_data.get('small_text','')
        
        if self.asset_image_large!=asset_image_large:
            old['asset_image_large']=self.asset_image_large
            self.asset_image_large=asset_image_large
        
        if self.asset_image_small!=asset_image_small:
            old['asset_image_small']=self.asset_image_small
            self.asset_image_small=asset_image_small
        
        if self.asset_text_large!=asset_text_large:
            old['asset_text_large']=self.asset_text_large
            self.asset_text_large=asset_text_large
        
        if self.asset_text_small!=asset_text_small:
            old['asset_text_small']=self.asset_text_small
            self.asset_text_small=asset_text_small
        
        url=data.get('url','')
        if self.url!=url:
            old['url']=self.url
            self.url=url
        
        sync_id=data.get('sync_id','')
        if self.sync_id!=sync_id:
            old['sync_id']=self.sync_id
            self.sync_id=sync_id
            
        session_id=data.get('session_id','')
        if self.session_id!=session_id:
            old['session_id']=self.session_id
            self.session_id=session_id
        
        flags=ActivityFlag(data.get('flags',0))
        if self.flags!=flags:
            old['flags']=self.flags
            self.flags=flags
        
        id_=int(data['id'],base=16)
        if self.id!=id_:
            old['id']=self.id
            self.id=id_
        
        created=data.get('created_at',0)
        if self.created!=created:
            old['created']=self.created
            self.created=created
        
        return old
    
    @classmethod
    def create(cls, name, url=''):
        """
        Returns a streaming activity with the given attributes.
        
        Parameters
        ----------
        name : `str`
            The name of the activity.
        url : `str`, Optional
            The url of the activity. Only twitch urls are supported. ``ActivityStream`` only.
        
        Returns
        -------
        activity : ``ActivityStream``
        """
        self = object.__new__(cls)
        self.name               = name
        self.url                = url
        
        self.details            = ''
        self.asset_image_large  = ''
        self.asset_image_small  = ''
        self.asset_text_large   = ''
        self.sync_id            = ''
        self.session_id         = ''
        self.flags              = ActivityFlag(0)
        self.created            = 0
        self.id                 = 0
        
        return self
    
    @property
    def twitch_name(self):
        """
        If the user streams on twitch, returns it's twitch name, else an empty string.
        
        Returns
        -------
        name : `str`
        """
        name=self.asset_image_large
        if name and name.startswith('twitch:'):
            return name[7:]
        return ''

class ActivitySpotify(ActivityBase):
    """
    Represents a Discord gaming activity.
    
    Attributes
    ----------
    asset_image_large : `str`
        The id of the activity's large asset to display. Defaults to empty string.
    asset_image_small : `str`
        The id of the activity's small asset to display. Defaults to empty string.
    asset_text_large : `str`
        The hover text of the large asset. Defaults to empty string.
    asset_text_small : `str`
        The hover text of the small asset. Defaults to empty string.
    created : `int`
        When the status was created as Unix time in milliseconds. Defaults to `0`.
    details : `str`
        What the player is currently doing.
    flags : ``ActivityFlag``
        The flags of the activity. Defaults to `ActivityFlag(0)`
    name : `str`
        The activity's name.
    party_id : `str`
        The party's id, which in the player is. Defaults to empty string.
    party_max : `int`
        The party's maximal size, which in the player is. Defaults to `0`.
    party_size : `int`
        The party's actual size, which in the player is. Defaults to `0`.
    session_id : `str`
        The ``ActivitySpotify``'s session's id. Defaults to empty string.
    state : `str` or `None`
        The player's current party status. Defaults to `None`.
    sync_id : `str`
        The ID of the currently playing track. Used at ``ActivitySpotify``. Defaults to empty string.
    timestamp_end : `int`
        The time when the activity ends as Unix time in milliseconds. Defaults to `0`.
    timestamp_start : `int`
        The time when the activity starts as Unix time in milliseconds. Defaults to `0`.
    
    Class Attributes
    ----------------
    DATA_SIZE_LIMIT : `int` = `12`
        Tells over how much data an activity will be created as `activity_rich` over sub-activity-types.
    ACTIVITY_FLAG : `int` = `0b0000001110011111`
        Represents which attribute groups the activity type implements.
    color : ``Color`` = `Color(0x1db954)
        The color of the activity.
    CUSTOM_ID : str` = `'spotify:1'`
        The custom id of the activity.
    """
    __slots__ = ('asset_image_large', 'asset_image_small', 'asset_text_large', 'asset_text_small', 'created',
        'details', 'flags', 'name', 'party_id', 'party_max', 'party_size', 'session_id', 'state', 'sync_id',
        'timestamp_end', 'timestamp_start', )
    
    DATA_SIZE_LIMIT = 12
    ACTIVITY_FLAG   = 0b0000001110011111
    CUSTOM_ID       = 'spotify:1'
    color           = Color(0x1db954)
    
    @property
    def type(self):
        """
        The type of a spotify activity is always `2`.
        
        Returns
        -------
        type : `int` = `2`
        """
        return 2
    
    def __new__(cls, data):
        """
        Creates an ``ActivitySpotify`` instance from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Activity data received from Discord.
            
        Returns
        -------
        activity : ``ActivitySpotify``
        """
        self = object.__new__(cls)
        #ignore id, it is static
        self._update_no_return(data)
        return self

    def _update_no_return(self, data):
        """
        Updates the activity by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        """
        self.name=data['name']
        
        try:
            timestamp_data=data['timestamps']
        except KeyError:
            self.timestamp_end=0
            self.timestamp_start=0
        else:
            self.timestamp_end=timestamp_data.get('end',0)
            self.timestamp_start=timestamp_data.get('start',0)

        self.details=data.get('details','')
        
        self.state=data.get('state',None)

        try:
            party_data=data['party']
        except KeyError:
            self.party_id=''
            self.party_size=self.party_max=0
        else:
            self.party_id=party_data.get('id','')
            try:
                self.party_size,self.party_max=data['size']
            except KeyError:
                self.party_size=self.party_max=0
        
        try:
            asset_data=data['assets']
        except KeyError:
            self.asset_image_large=''
            self.asset_image_small=''
            self.asset_text_large=''
            self.asset_text_small=''
        else:
            self.asset_image_large=asset_data.get('large_image','')
            self.asset_image_small=asset_data.get('small_image','')
            self.asset_text_large=asset_data.get('large_text','')
            self.asset_text_small=asset_data.get('small_text','')

        self.sync_id=data.get('sync_id','')
        
        self.session_id=data.get('session_id','')
        
        try:
            self.flags=ActivityFlag(data['flags'])
        except KeyError:
            self.flags=ActivityFlag.spotify #customization
        
        self.created=data.get('created_at',0)
        
    def _update(self,data):
        """
        Updates the activity and returns the changes in a `dict` of (`attribute-name`, `old-value`) items.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        
        Returns
        -------
        changes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +-----------------------+-----------------------+
        | key                   | value                 |
        +=======================+=======================+
        | application_id        | `int`                 |
        +-----------------------+-----------------------+
        | asset_image_large     | `str`                 |
        +-----------------------+-----------------------+
        | asset_image_small     | `str`                 |
        +-----------------------+-----------------------+
        | asset_text_large      | `str`                 |
        +-----------------------+-----------------------+
        | asset_text_small      | `str`                 |
        +-----------------------+-----------------------+
        | created               | `int`                 |
        +-----------------------+-----------------------+
        | details               | `str`                 |
        +-----------------------+-----------------------+
        | flags                 | ``ActivityFlag``      |
        +-----------------------+-----------------------+
        | name                  | `str`                 |
        +-----------------------+-----------------------+
        | party_id              | `str`                 |
        +-----------------------+-----------------------+
        | party_max             | `int`                 |
        +-----------------------+-----------------------+
        | party_size            | `int`                 |
        +-----------------------+-----------------------+
        | session_id            | `str`                 |
        +-----------------------+-----------------------+
        | state                 | `str` / `None`        |
        +-----------------------+-----------------------+
        | sync_id               | `str`                 |
        +-----------------------+-----------------------+
        | timestamp_end         | `int`                 |
        +-----------------------+-----------------------+
        | timestamp_start       | `int`                 |
        +-----------------------+-----------------------+
        """
        old={}
        
        name=data['name']
        if self.name!=name:
            old['name']=self.name
            self.name=name
            
        try:
            timestamp_data=data['timestamps']
        except KeyError:
            timestamp_end=0
            timestamp_start=0
        else:
            timestamp_end=timestamp_data.get('end',0)
            timestamp_start=timestamp_data.get('start',0)
            
        if self.timestamp_end!=timestamp_end:
            old['timestamp_end']=self.timestamp_end
            self.timestamp_end=timestamp_end
            
        if self.timestamp_start!=timestamp_start:
            old['timestamp_start']=self.timestamp_start
            self.timestamp_start=timestamp_start

        details=data.get('details','')
        if self.details!=details:
            old['details']=self.details
            self.details=details

        state=data.get('state',None)
        if (self.state is None):
            if (state is not None):
                old['state']=None
                self.state=state
        else:
            if (state is None):
                old['state']=self.state
                self.state=None
            elif (self.state!=state):
                old['state']=self.state
                self.state=state
        
        try:
            party_data=data['party']
        except KeyError:
            party_id=''
            party_size=party_max=0
        else:
            party_id=party_data.get('id','')
            try:
                party_size,party_max=party_data['size']
            except KeyError:
                party_size=party_max=0
                
        if self.party_id!=party_id:
            old['party_id']=self.party_id
            self.party_id=party_id
            
        if self.party_size!=party_size:
            old['party_size']=self.party_size
            self.party_size=party_size
            
        if self.party_max!=party_max:
            old['party_max']=self.party_max
            self.party_max=party_max

        try:
            asset_data=data['assets']
        except KeyError:
            asset_image_large=''
            asset_image_small=''
            asset_text_large=''
            asset_text_small=''
        else:
            asset_image_large=asset_data.get('large_image','')
            asset_image_small=asset_data.get('small_image','')
            asset_text_large=asset_data.get('large_text','')
            asset_text_small=asset_data.get('small_text','')
            
        if self.asset_image_large!=asset_image_large:
            old['asset_image_large']=self.asset_image_large
            self.asset_image_large=asset_image_large
            
        if self.asset_image_small!=asset_image_small:
            old['asset_image_small']=self.asset_image_small
            self.asset_image_small=asset_image_small
            
        if self.asset_text_large!=asset_text_large:
            old['asset_text_large']=self.asset_text_large
            self.asset_text_large=asset_text_large
            
        if self.asset_text_small!=asset_text_small:
            old['asset_text_small']=self.asset_text_small
            self.asset_text_small=asset_text_small

        sync_id=data.get('sync_id','')
        if self.sync_id!=sync_id:
            old['sync_id']=self.sync_id
            self.sync_id=sync_id
                
        session_id=data.get('session_id','')
        if self.session_id!=session_id:
            old['session_id']=self.session_id
            self.session_id=session_id
        
        created=data.get('created_at',0)
        if self.created!=created:
            old['created']=self.created
            self.created=created
        
        return old

    @classmethod
    def create(cls, name,):
        """
        Returns a spotify activity with the given attributes.
        
        Parameters
        ----------
        name : `str`
            The name of the activity.
        
        Returns
        -------
        activity : ``ActivitySpotify``
        """
        self = object.__new__(cls)
        self.name               = name
        
        self.timestamp_end      = 0
        self.timestamp_start    = 0
        self.details            = ''
        self.state              = None
        self.party_id           = ''
        self.party_size         = 0
        self.party_max          = 0
        self.asset_image_large  = ''
        self.asset_image_small  = ''
        self.asset_text_large   = ''
        self.asset_text_small   = ''
        self.sync_id            = ''
        self.session_id         = ''
        self.flags              = ActivityFlag(0)
        self.created            = 0
        
        return self
    
    def __hash__(self):
        """Returns the activity's hash value."""
        return hash(self.session_id)
    
    @property
    def title(self):
        """
        Returns the currently playing track on spotify, which is equal to `.details`.
        
        Returns
        -------
        title : `str`
        """
        return self.details

    @property
    def artists(self):
        """
        Returns the track's artists. If it has non or one, it still returns a list.
        
        Returns
        -------
        artists : `list` of `str`
        """
        state = self.state
        if state is None:
            return []
        return state.split(';')
    
    @property
    def artist(self):
        """
        Returns the track's artist. If it has more, they are separated with `';'`.
        
        Returns
        -------
        artist : `str`
        """
        state=self.state
        if state is None:
            return ''
        return state
    
    @property
    def album(self):
        """
        Returns the currently playing track's album title. This value is equal to the `.asset_text_large` instance
        attribute.
        
        Returns
        -------
        album : `str`
        """
        return self.asset_text_large

    @property
    def album_cover_url(self):
        """
        Returns the currently playing track's album url if it has any.
        
        Returns
        -------
        album_cover_url : `str`
        """
        image=self.asset_image_large
        if image:
            return f'https://i.scdn.co/image/{image}'
        return image

    @property
    def track_id(self):
        """
        The id of the currently playing track. This value is same as the `.sync_id`.
        
        Returns
        -------
        track_id : `str`
        """
        return self.sync_id

    @property
    def duration(self):
        """
        The duration of the track.
        
        Returns
        -------
        duration : `str`
        """
        return self.timestamp_end-self.timestamp_start

    @property
    def start(self):
        """
        Returns when the activity was started.
        
        Returns
        -------
        start : `datetime`
        """
        return datetime.utcfromtimestamp(self.timestamp_start/1000.)

    @property
    def end(self):
        """
        Returns when the activity ended.
        
        Returns
        -------
        start : `datetime`
        """
        return datetime.utcfromtimestamp(self.timestamp_end/1000.)

class ActivityWatching(ActivityBase):
    """
    Represents a Discord watching activity.
    
    Attributes
    ----------
    created : `int`
        When the status was created as Unix time in milliseconds. Defaults to `0`.
    id : `int`
        The id of the activity. Defaults to `0`.
    name : `str`
        The activity's name.
    
    Class Attributes
    ----------------
    DATA_SIZE_LIMIT : `int` = `4`
        Tells over how much data an activity will be created as `ActivityRich` over sub-activity-types.
    ACTIVITY_FLAG : `int` = `0b0001000000000000`
        Represents which attribute groups the activity type implements.
    color : ``Color`` = `Color(0x7289da)
        The color of the activity.
    """
    __slots__ = ('created', 'id', 'name', )
    
    DATA_SIZE_LIMIT = 4
    ACTIVITY_FLAG   = 0b0001000000000000
    color           = ActivityGame.color
    
    @property
    def type(self):
        """
        The type of a gaming activity is always `3`.
        
        Returns
        -------
        type : `int` = `3`
        """
        return 3
    
    def __new__(cls, data):
        """
        Creates an ``ActivityWatching`` instance from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Activity data received from Discord.
            
        Returns
        -------
        activity : ``ActivityWatching``
        """
        self = object.__new__(cls)
        self._update_no_return(data)
        return self

    def _update_no_return(self, data):
        """
        Updates the activity by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        """
        self.name       = data['name']
        self.id         = int(data['id'],base=16)
        self.created    = data.get('created_at',0)
    
    def _update(self, data):
        """
        Updates the activity and returns the changes in a `dict` of (`attribute-name`, `old-value`) items.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        
        Returns
        -------
        changes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +-----------------------+-----------------------+
        | key                   | value                 |
        +=======================+=======================+
        | created               | `int`                 |
        +-----------------------+-----------------------+
        | id                    | `int`                 |
        +-----------------------+-----------------------+
        | name                  | `str`                 |
        +-----------------------+-----------------------+
        """
        old={}
        
        name=data['name']
        if self.name!=name:
            old['name']=self.name
            self.name=name
        
        id_=int(data['id'],base=16)
        if self.id!=id_:
            old['id']=self.id
            self.id=id_
        
        created=data.get('created_at',0)
        if self.created!=created:
            old['created']=self.created
            self.created=created
        
        return old

    @classmethod
    def create(cls, name,):
        """
        Returns a watching activity with the given attributes.
        
        Parameters
        ----------
        name : `str`
            The name of the activity.
        
        Returns
        -------
        activity : ``ActivityWatching``
        """
        self = object.__new__(cls)
        self.name       = name
        
        self.created    = datetime.now()
        self.id         = 0
        
        return self

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
    DATA_SIZE_LIMIT : `int` = `6`
        Tells over how much data an activity will be created as `ActivityRich` over sub-activity-types.
    ACTIVITY_FLAG : `int` = `0b0000100000000100`
        Represents which attribute groups the activity type implements.
    color : ``Color`` = `Color(0)
        The color of the activity.
    id : `int` = `0`
        The activity's id.
    CUSTOM_ID : str` = `'custom'`
        The custom id of the activity.
    """
    __slots__ = ('created', 'emoji', 'state', )
    
    DATA_SIZE_LIMIT = 6
    ACTIVITY_FLAG   = 0b0000100000000100
    CUSTOM_ID       = 'custom'
    
    @property
    def type(self):
        """
        The type of a custom activity is always `4`.
        
        Returns
        -------
        type : `int` = `4`
        """
        return 4
    
    def __new__(cls, data):
        """
        Creates an ``ActivityCustom`` instance from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Activity data received from Discord.
            
        Returns
        -------
        activity : ``ActivityCustom``
        """
        self = object.__new__(cls)
        #ignore `name` and `id` in keys, those are always static
        self._update_no_return(data)
        return self

    def __hash__(self):
        """Returns the activity's hash value."""
        state=self.state
        emoji=self.emoji
        if (state is None):
            if (emoji is None):
                return 0
            else:
                return emoji.id
        else:
            if (emoji is None):
                return state.__hash__()
            else:
                return state.__hash__()^emoji.id
    
    @property
    def name(self):
        """
        Returns the activity's display text.
        
        Returns
        -------
        name : `str`
        """
        state=self.state
        emoji=self.emoji
        if (state is None):
            if (emoji is None):
                return ''
            else:
                return emoji.as_emoji
        else:
            if (emoji is None):
                return state
            else:
                return f'{emoji.as_emoji} {state}'
    
    def _update_no_return(self,data):
        """
        Updates the activity by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        """
        self.state=data.get('state',None)
        emoji_data=data.get('emoji',None)
        if emoji_data is None:
            emoji=None
        else:
            emoji=PartialEmoji(emoji_data)
        self.emoji=emoji
        
        self.created=data.get('created_at',0)
        
    def _update(self,data):
        """
        Updates the activity and returns the changes in a `dict` of (`attribute-name`, `old-value`) items.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        
        Returns
        -------
        changes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +-----------------------+-----------------------+
        | key                   | value                 |
        +=======================+=======================+
        | created               | `int`                 |
        +-----------------------+-----------------------+
        | emoji                 | ``Emoji`` / `None`    |
        +-----------------------+-----------------------+
        | state                 | `str` / `None`        |
        +-----------------------+-----------------------+
        """
        old={}
        
        state=data.get('state',None)
        if (self.state is None):
            if (state is not None):
                old['state']=None
                self.state=state
        else:
            if (state is None):
                old['state']=self.state
                self.state=None
            elif (self.state!=state):
                old['state']=self.state
                self.state=state
                
        emoji_data=data.get('emoji',None)
        if emoji_data is None:
            emoji=None
        else:
            emoji=PartialEmoji(emoji_data)
        
        if (self.emoji is None):
            if (emoji is not None):
                old['emoji']=None
                self.emoji=emoji
        else:
            if (emoji is None):
                old['emoji']=self.emoji
                self.emoji=None
            elif self.emoji!=emoji:
                old['emoji']=self.emoji
                self.emoji=emoji
        
        created=data.get('created_at',0)
        if self.created!=created:
            old['created']=self.created
            self.created=created
        
        return old

ACTIVITY_TYPES = (
    ActivityGame,
    ActivityStream,
    ActivitySpotify,
    ActivityWatching,
    ActivityCustom,
        )

def Activity(data):
    """
    A factory function to create activity from deserialized json data sent by Discord.
    
    If the data is `None` returns ``ActivityUnknown``. If the length of the data exceeds the activty type's maximal
    size, it will instance ``ActivityRich`` instead.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Activity data received from Discord.
    
    Returns
    -------
    activity : ``ActivityBase`` instance
    """
    if data is None:
        return ActivityUnknown
    try:
        activity_type=ACTIVITY_TYPES[data['type']]
    except IndexError:
        return ActivityUnknown
    if len(data)>activity_type.DATA_SIZE_LIMIT:
        return ActivityRich(data)
    return activity_type(data)

del URLS
del Color
del FlagBase

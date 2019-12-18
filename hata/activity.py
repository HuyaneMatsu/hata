# -*- coding: utf-8 -*-
__all__ = ( 'ActivityBase', 'ActivityCustom', 'ActivityFlag', 'ActivityGame',
    'ActivityRich', 'ActivitySpotify', 'ActivityStream', 'ActivityUnknown',
    'ActivityWatching', )

from datetime import datetime

from .color import Color
from .http import URLS

PartialEmoji=NotImplemented

class ActivityFlag(int):
    
    @property
    def INSTANCE(self):
        return self&1

    @property
    def JOIN(self):
        return (self>>1)&1

    @property
    def SPECTATE(self):
        return (self>>2)&1

    @property
    def JOIN_REQUEST(self):
        return (self>>3)&1

    @property
    def SYNC(self):
        return (self>>4)&1

    @property
    def PLAY(self):
        return (self>>5)&1

    def __iter__(self):
        if self&1:
            yield 'INSTANCE'
        
        if (self>>1)&1:
            yield 'JOIN'
        
        if (self>>2)&1:
            yield 'SPECTATE'
        
        if (self>>3)&1:
            yield 'JOIN_REQUEST'
        
        if (self>>4)&1:
            yield 'SYNC'
        
        if (self>>5)&1:
            yield 'PLAY'

    def __repr__(self):
        return f'{self.__class__.__name__}({int.__repr__(self)})'

    spotify = NotImplemented

ActivityFlag.spotify = ActivityFlag(48)

class ActivityBase(object):
    __slots__=()

    DATA_SIZE_LIMIT = 0
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

    @property
    def discord_side_id(self):
        if self.ACTIVITY_FLAG&0b0001000000000000:
            return self.id.__format__('0>16x')
        return self.CUSTOM_ID
    
    #this is for bots only, because bots can send only this 3 information!
    @classmethod
    def create(cls,name,url='',type_=0):
        self=object.__new__(cls)
        
        if self.ACTIVITY_FLAG&0b0000000001000000: #for streaming only, twitch url only!
            self.url=url

        if not hasattr(cls,'type'): #type lookup is auto for subclasses.
            self.type=type_ 
        
        if self.type!=4:
            self.name=name
        
        self._fillup()
        return self

    def botdict(self):
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
        created=self.created
        if created==0:
            return None
        
        return datetime.utcfromtimestamp(created/1000.)
    
    def __eq__(self,other):
        if isinstance(other,ActivityBase):
            return self.type==other.type and self.id==other.id
        return NotImplemented

    def __ne__(self,other):
        if isinstance(other,ActivityBase):
            return self.type!=other.type or self.id!=other.id
        return NotImplemented
    
class ActivityRich(ActivityBase):
    __slots__=('application_id', 'asset_image_large', 'asset_image_small',
        'asset_text_large', 'asset_text_small', 'created', 'details',
        'emoji', 'flags', 'id', 'name', 'party_id', 'party_max',
        'party_size', 'secret_join', 'secret_match', 'secret_spectate',
        'session_id', 'state', 'sync_id', 'timestamp_end', 'timestamp_start',
        'type', 'url',)
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

    def __init__(self,data):
        self._update_no_return(data)

    def _update_no_return(self,data):
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
    
    @property
    def color(self):
        try:
            return ACTIVITY_TYPES[self.type].color
        except KeyError:
            return ActivityUnknown.color
        
    def _update(self,data):
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
    
    def _fillup(self):
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

    def __str__(self):
        return self.name

    def __hash__(self):
        return self.id

    def __repr__(self):
        return f'<{self.__class__.__name__} type={self.type} name=\'{self.name}\'>'

    @property
    def start(self):
        timestamp_start=self.timestamp_start
        if timestamp_start==0:
            return None

        return datetime.utcfromtimestamp(timestamp_start/1000.)

    @property
    def end(self):
        timestamp_end=self.timestamp_end
        if timestamp_end==0:
            return None

        return datetime.utcfromtimestamp(timestamp_end/1000.)

    image_large_url=property(URLS.activity_asset_image_large_url)
    image_large_url_as=URLS.activity_asset_image_large_url_as
    image_small_url=property(URLS.activity_asset_image_small_url)
    image_small_url_as=URLS.activity_asset_image_small_url_as

class ActivityUnknown(ActivityBase):
    __slots__=()

    DATA_SIZE_LIMIT = 3
    ACTIVITY_FLAG   = 0b0000000000000000
    color           = Color(0)

    @property
    def type(self):
        return -1

    def __init__(self,data):
        pass

    def _update(self,data):
        return {}

    def _update_no_return(self,data):
        pass

    def _fillup(self):
        pass

    def __str__(self):
        return 'Unknown'

    def __hash__(self):
        return 0

    def __repr__(self):
        return f'<{self.__class__.__name__}>'

    name=property(__str__)
    
    id=property(__hash__)

    @property
    def created(self):
        return 0



ActivityUnknown=ActivityUnknown(None)

class ActivityGame(ActivityBase):
    __slots__=('application_id', 'created', 'flags', 'id', 'name',
        'timestamp_end', 'timestamp_start',)
    DATA_SIZE_LIMIT = 7
    ACTIVITY_FLAG   = 0b0001011000000001

    color=Color(0x7289da)

    @property
    def type(self):
        return 0

    def __init__(self,data):
        self._update_no_return(data)

    def _update_no_return(self,data):
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

    def _fillup(self):
        self.application_id     = 0
        self.timestamp_end      = 0
        self.timestamp_start    = 0
        self.flags              = ActivityFlag(0)
        self.created            = 0
        self.id                 = 0

    def __str__(self):
        return self.name

    def __hash__(self):
        return self.id

    def __repr__(self):
        return f'<{self.__class__.__name__} name=\'{self.name}\'>'

    @property
    def start(self):
        timestamp_start=self.timestamp_start
        if timestamp_start is None:
            return None

        return datetime.utcfromtimestamp(timestamp_start/1000.)

    @property
    def end(self):
        timestamp_end=self.timestamp_end
        if timestamp_end is None:
            return None

        return datetime.utcfromtimestamp(timestamp_end/1000.)

class ActivityStream(ActivityBase):
    __slots__=('asset_image_large', 'asset_image_small', 'asset_text_large',
        'asset_text_small', 'created', 'details', 'flags', 'id', 'name',
        'session_id', 'sync_id', 'url',)
    
    DATA_SIZE_LIMIT = 9
    #TODO: test for: flags - 0b0000001000000000
    ACTIVITY_FLAG   = 0b0001000111010010

    @property
    def color(self):
        if self.url:
            return self.default_color
        else:
            return ActivityGame.color

    default_color=Color(0x593695)

    @property
    def type(self):
        return 1

    def __init__(self,data):
        self._update_no_return(data)

    def _update_no_return(self,data):
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

    def _fillup(self):
        self.details            = ''
        self.asset_image_large  = ''
        self.asset_image_small  = ''
        self.asset_text_large   = ''
        self.sync_id            = ''
        self.session_id         = ''
        self.flags              = ActivityFlag(0)
        self.created            = 0
        self.id                 = 0

    def __str__(self):
        return self.name

    def __hash__(self):
        return self.id

    def __repr__(self):
        return f'<{self.__class__.__name__} name=\'{self.name}\'>'

    @property
    def twitch_name(self):
        name=self.asset_image_large
        if name and name.startswith('twitch:'):
            return name[7:]
        return ''

class ActivitySpotify(ActivityBase):
    __slots__=('asset_image_large', 'asset_image_small', 'asset_text_large',
        'asset_text_small', 'created', 'details', 'flags', 'name',
        'party_id', 'party_max', 'party_size', 'session_id', 'state',
        'sync_id', 'timestamp_end', 'timestamp_start',)
    
    DATA_SIZE_LIMIT = 12
    ACTIVITY_FLAG   = 0b0000001110011111
    CUSTOM_ID       = 'spotify:1'
    color           = Color(0x1db954)

    @property
    def type(self):
        return 2
    
    @property
    def id(self):
        return 0
    
    def __init__(self,data):
        #ignore id, it is static
        self._update_no_return(data)

    def _update_no_return(self,data):
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

    def _fillup(self):
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

    def __str__(self):
        return self.name

    def __hash__(self):
        return self.session_id.__hash__()

    def __repr__(self):
        return f'<{self.__class__.__name__} name=\'{self.name}\'>'

    @property
    def title(self):
        return self.details

    @property
    def artists(self):
        state=self.state
        if state is None:
            return []
        return state.split(';')

    @property
    def artist(self):
        state=self.state
        if state is None:
            return ''
        return state

    @property
    def album(self):
        return self.asset_text_large

    @property
    def album_cover_url(self):
        image=self.asset_image_large
        if image:
            return f'https://i.scdn.co/image/{image}'
        return image

    @property
    def track_id(self):
        return self.sync_id

    @property
    def duration(self):
        return self.timestamp_end-self.timestamp_start

    @property
    def start(self):
        return datetime.utcfromtimestamp(self.timestamp_start/1000.)

    @property
    def end(self):
        return datetime.utcfromtimestamp(self.timestamp_end/1000.)

class ActivityWatching(ActivityBase):
    __slots__=('created', 'id', 'name',)
    
    DATA_SIZE_LIMIT = 4
    ACTIVITY_FLAG   = 0b0001000000000000
    color           = ActivityGame.color

    @property
    def type(self):
        return 3
    
    def __init__(self,data):
        self._update_no_return(data)

    def _update_no_return(self,data):
        self.name       = data['name']
        self.id         = int(data['id'],base=16)
        self.created    = data.get('created_at',0)
    
    def _update(self,data):
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

    def _fillup(self):
        self.created    = datetime.now()
        self.id         = 0

    def __str__(self):
        return self.name

    def __hash__(self):
        return self.id

    def __repr__(self):
        return f'<{self.__class__.__name__} name=\'{self.name}\'>'

class ActivityCustom(ActivityBase):
    __slots__=('created', 'emoji', 'state')
    DATA_SIZE_LIMIT = 6
    ACTIVITY_FLAG   = 0b0000100000000100
    CUSTOM_ID       = 'custom'
    color           = ActivityUnknown.color
    
    @property
    def type(self):
        return 4
    
    def __init__(self,data):
        #ignore `name` and `id` in keys, those are always static
        self._update_no_return(data)
        
    def __hash__(self):
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

    def __str__(self):
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

    def __repr__(self):
        state=self.state
        emoji=self.emoji
        if (state is None):
            if (emoji is None):
                name_repr=''
            else:
                name_repr=f':{emoji.name}:'
        else:
            if (emoji is None):
                name_repr=state
            else:
                name_repr=f':{emoji.name}: {state}'

        return f'<{self.__class__.__name__} name=\'{name_repr}\'>'

    name=property(__str__)

    def _update_no_return(self,data):
        self.state=data.get('state',None)
        emoji_data=data.get('emoji',None)
        if emoji_data is None:
            emoji=None
        else:
            emoji=PartialEmoji(emoji_data)
        self.emoji=emoji
        
        self.created=data.get('created_at',0)
        
    def _update(self,data):
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

    def _fillup(self):
        self.state      = None
        self.emoji      = None
        self.created    = 0
        
    @property
    def id(self):
        return 0
    
ACTIVITY_TYPES = (
    ActivityGame,
    ActivityStream,
    ActivitySpotify,
    ActivityWatching,
    ActivityCustom,
        )

def Activity(data):
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

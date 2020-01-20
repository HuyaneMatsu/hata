# -*- coding: utf-8 -*-
__all__ = ('Relationship', 'ContentFilterLevel', 'DISCORD_EPOCH',
    'FriendRequestFlag', 'Gift', 'HypesquadHouse', 'MFA',
    'MessageNotificationLevel', 'PremiumType', 'RelationshipType', 'Status',
    'Theme', 'Unknown', 'VerificationLevel', 'VoiceRegion', 'filter_content',
    'id_to_time', 'is_id', 'is_mention', 'is_role_mention', 'is_user_mention',
    'now_as_id', 'random_id', 'time_to_id', )

import random, re, sys
from urllib.parse import _ALWAYS_SAFE_BYTES as ALWAYS_SAFE_BYTES,Quoter
from datetime import datetime
from base64 import b64encode
from time import time as time_now
from json import dumps as dump_to_json, loads as from_json

try:
    from dateutil.relativedelta import relativedelta
except ImportError:
    relativedelta = None

from .dereaddons_local import titledstr, modulize

#preparing encoding
safe='/ '.encode('ascii','ignore')
ALWAYS_SAFE_BYTES+=safe
QUOTER=Quoter(safe)
del safe,Quoter
def quote(text):
    #text must be str
    text=text.encode('utf-8','strict')
    if not text.rstrip(ALWAYS_SAFE_BYTES):
        return text.decode()
    return ''.join([QUOTER[char] for char in text])

#base64 conversions

def bytes_to_base64(data,ext=None):
    if ext is None:
        if data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
            ext='image/png'
        elif data.startswith(b'\xFF\xD8') and data.rstrip(b'\0').endswith(b'\xFF\xD9'):
            ext='image/jpeg'
        elif data.startswith(b'\x47\x49\x46\x38\x37\x61') or data.startswith(b'\x47\x49\x46\x38\x39\x61'):
            ext='image/gif'
        else:
            raise ValueError('Unsupported image type given')
    return ''.join(['data:',ext,';base64,',b64encode(data).decode('ascii')])

def ext_from_base64(data):
    return data[11:data.find(';',11)]
    
DISCORD_EPOCH=1420070400000
# example dates:
# "2016-03-31T19:15:39.954000+00:00"
# "2019-04-28T15:14:38+00:00"
# at edit:
# "2019-07-17T18:52:50.758993+00:00" #this is before desuppress!
# at desuppress:
# "2019-07-17T18:52:50.758000+00:00"

PARSE_TIME_RP=re.compile('(\\d{4})-(\\d{2})-(\\d{2})T(\\d{2}):(\\d{2}):(\\d{2})(?:\\.(\\d{3})?)?.*')

def parse_time(timestamp):
    parsed=PARSE_TIME_RP.fullmatch(timestamp)
    if parsed is None:
        sys.stderr.write(f'Cannot parse timestamp: `{timestamp}`, returning` None`\n')
        return None
    
    year    = int(parsed.group(1))
    month   = int(parsed.group(2))
    day     = int(parsed.group(3))
    hour    = int(parsed.group(4))
    minute  = int(parsed.group(5))
    second  = int(parsed.group(6))
    micro   = parsed.group(7)
    
    if micro is None:
        micro = 0
    else:
        micro = int(micro)
    
    return datetime(year, month, day, hour, minute, second, micro)

def id_to_time(id_):
    return datetime.utcfromtimestamp(((id_>>22)+DISCORD_EPOCH)/1000.)
        
def time_to_id(time):
    return ((time.timestamp()*1000.).__int__()-DISCORD_EPOCH)<<22

def random_id():
    return (((time_now()*1000.).__int__()-DISCORD_EPOCH)<<22)+(random.random()*4194304.).__int__()

def to_json(data):
    return dump_to_json(data,separators=(',',':'),ensure_ascii=True)

class VerificationLevel(object):
    # class related
    INSTANCES = [NotImplemented] * 5
    
    # object related
    __slots__=('name', 'value',)
    
    def __init__(self,value,name):
        self.value=value
        self.name=name
        
        self.INSTANCES[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'
    
    # predefined
    none    = NotImplemented
    low     = NotImplemented
    medium  = NotImplemented
    high    = NotImplemented
    extreme = NotImplemented

VerificationLevel.none     = VerificationLevel(0,'none')
VerificationLevel.low      = VerificationLevel(1,'low')
VerificationLevel.medium   = VerificationLevel(2,'medium')
VerificationLevel.high     = VerificationLevel(3,'high')
VerificationLevel.extreme  = VerificationLevel(4,'extreme')

class VoiceRegion(object):
    # class related
    INSTANCES = {}
    
    @classmethod
    def get(cls,id_):
        try:
            voice_region=cls.INSTANCES[id_]
        except KeyError:
            voice_region=cls._from_id(id_)
        
        return voice_region
    
    @classmethod
    def _from_id(cls,id_):
        name_parts      = id_.split('-')
        for index in range(len(name_parts)):
            name_part=name_parts[index]
            if len(name_part)<4:
                name_part=name_part.upper()
            else:
                name_part=name_part.capitalize()
            name_parts[index]=name_part
        
        name=' '.join(name_parts)
        
        self                = object.__new__(cls)
        self.name           = name
        self.id             = id_
        self.deprecated     = False
        self.vip            = id_.startswith('vip-')
        self.custom         = True
        self.INSTANCES[id_] = self
        return self
        
    @classmethod
    def from_data(cls,data):
        id_=data['id']
        try:
            return cls.INSTANCES[id_]
        except KeyError:
            pass
        
        self                = object.__new__(cls)
        self.name           = data['name']
        self.id             = id_
        self.deprecated     = data['deprecated']
        self.vip            = data['vip']
        self.custom         = data['custom']
        self.INSTANCES[id_] = self
        
        return self
    
    # object related
    __slots__=('custom', 'deprecated', 'id', 'name', 'vip',)
    
    def __init__(self,name,id_,deprecated,vip):
        self.name           = name
        self.id             = id_
        self.deprecated     = deprecated
        self.vip            = vip
        self.custom         = False
        self.INSTANCES[id_] = self
    
    def __str__(self):
        return self.id
    
    def __repr__(self):
        return f'<{self.__class__.__name__} name={self.name!r} id={self.id!r}>'
    
    # predefined
    
    # normal
    brazil          = NotImplemented
    dubai           = NotImplemented
    eu_central      = NotImplemented
    eu_west         = NotImplemented
    europe          = NotImplemented
    hongkong        = NotImplemented
    india           = NotImplemented
    japan           = NotImplemented
    russia          = NotImplemented
    singapore       = NotImplemented
    southafrica     = NotImplemented
    sydney          = NotImplemented
    us_central      = NotImplemented
    us_east         = NotImplemented
    us_south        = NotImplemented
    us_west         = NotImplemented
    # deprecated
    amsterdam       = NotImplemented
    frankfurt       = NotImplemented
    london          = NotImplemented
    # vip
    vip_us_east     = NotImplemented
    vip_us_west     = NotImplemented
    # vip + deprecated
    vip_amsterdam   = NotImplemented

VoiceRegion.brazil          = VoiceRegion('Brazil',         'brazil',       False,  False)
VoiceRegion.dubai           = VoiceRegion('Dubai',          'dubai',        False,  False)
VoiceRegion.eu_central      = VoiceRegion('Central Europe', 'eu-central',   False,  False)
VoiceRegion.eu_west         = VoiceRegion('Western Europe', 'eu-west',      False,  False)
VoiceRegion.europe          = VoiceRegion('Europe',         'europe',       False,  False)
VoiceRegion.hongkong        = VoiceRegion('Hong Kong',      'hongkong',     False,  False)
VoiceRegion.india           = VoiceRegion('India',          'india',        False,  False)
VoiceRegion.japan           = VoiceRegion('Japan',          'japan',        False,  False)
VoiceRegion.russia          = VoiceRegion('Russia',         'russia',       False,  False)
VoiceRegion.singapore       = VoiceRegion('Singapore',      'singapore',    False,  False)
VoiceRegion.southafrica     = VoiceRegion('South Africa',   'southafrica',  False,  False)
VoiceRegion.sydney          = VoiceRegion('Sydney',         'sydney',       False,  False)
VoiceRegion.us_central      = VoiceRegion('US Central',     'us-central',   False,  False)
VoiceRegion.us_east         = VoiceRegion('US East',        'us-east',      False,  False)
VoiceRegion.us_south        = VoiceRegion('US South',       'us-south',     False,  False)
VoiceRegion.us_west         = VoiceRegion('US West',        'us-west',      False,  False)
#deprecated
VoiceRegion.amsterdam       = VoiceRegion('Amsterdam',      'amsterdam',    True,   False)
VoiceRegion.frankfurt       = VoiceRegion('Frankfurt',      'frankfurt',    True,   False)
VoiceRegion.london          = VoiceRegion('London',         'london',       True,   False)
#vip
VoiceRegion.vip_us_east     = VoiceRegion('VIP US West',    'vip-us-west',  False,  True)
VoiceRegion.vip_us_west     = VoiceRegion('VIP US East',    'vip-us-east',  False,  True)
#vip + deprecated
VoiceRegion.vip_amsterdam   = VoiceRegion('VIP Amsterdam',  'vip-amsterdam',True,   True)

class ContentFilterLevel(object):
    # class related
    INSTANCES = [NotImplemented] * 3
    
    # object related
    __slots__=('name', 'value', )
    
    def __init__(self,value,name):
        self.value=value
        self.name=name

        self.INSTANCES[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'
    
    # predefined
    disabled    = NotImplemented
    no_role     = NotImplemented
    everyone    = NotImplemented

ContentFilterLevel.disabled = ContentFilterLevel(0,'disabled')
ContentFilterLevel.no_role  = ContentFilterLevel(1,'no_role')
ContentFilterLevel.everyone = ContentFilterLevel(2,'everyone')

class HypesquadHouse(object):
    # class related
    INSTANCES = [NotImplemented] * 4
    
    #object related
    __slots__=('name', 'value', )
    
    def __init__(self,value,name):
        self.value=value
        self.name=name

        self.INSTANCES[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'
    
    # predefined
    none        = NotImplemented
    bravery     = NotImplemented
    brilliance  = NotImplemented
    balance     = NotImplemented

HypesquadHouse.none         = HypesquadHouse(0,'none')
HypesquadHouse.bravery      = HypesquadHouse(1,'bravery')
HypesquadHouse.brilliance   = HypesquadHouse(2,'brilliance')
HypesquadHouse.balance      = HypesquadHouse(3,'balance')


class Status(object):
    # class related
    INSTANCES = {}
    
    # object related
    __slots__=('position', 'value', )
    
    def __init__(self,value,position):
        self.value=value
        self.position=position
        self.INSTANCES[value]=self

    def __str__(self):
        return self.value
    
    name=property(__str__)
    
    def __repr__(self):
        return f'<{self.__class__.__name__} value={self.value!r}>'

    def __gt__(self,other):
        if type(self) is type(other):
            return self.position>other.position
        if isinstance(other,str):
            try:
                other=type(self).INSTANCES[other]
            except KeyError:
                return NotImplemented
            return self.position>other.position
        return NotImplemented

    def __ge__(self,other):
        if type(self) is type(other):
            return self.position>=other.position
        if isinstance(other,str):
            try:
                other=type(self).INSTANCES[other]
            except KeyError:
                return NotImplemented
            return self.position>=other.position
        return NotImplemented

    def __eq__(self,other):
        if type(self) is type(other):
            return self.position==other.position
        if isinstance(other,str):
            try:
                other=type(self).INSTANCES[other]
            except KeyError:
                return NotImplemented
            return self.position==other.position
        return NotImplemented

    def __ne__(self,other):
        if type(self) is type(other):
            return self.position!=other.position
        if isinstance(other,str):
            try:
                other=type(self).INSTANCES[other]
            except KeyError:
                return NotImplemented
            return self.position!=other.position
        return NotImplemented

    def __le__(self,other):
        if type(self) is type(other):
            return self.position<=other.position
        if isinstance(other,str):
            try:
                other=type(self).INSTANCES[other]
            except KeyError:
                return NotImplemented
            return self.position<=other.position
        return NotImplemented

    def __lt__(self,other):
        if type(self) is type(other):
            return self.position<other.position
        if isinstance(other,str):
            try:
                other=type(self).INSTANCES[other]
            except KeyError:
                return NotImplemented
            return self.position<other.position
        return  NotImplemented
    
    # predefined
    online      = NotImplemented
    idle        = NotImplemented
    dnd         = NotImplemented
    offline     = NotImplemented
    invisible   = NotImplemented

Status.online   = Status('online',0)
Status.idle     = Status('idle',1)
Status.dnd      = Status('dnd',2)
Status.offline  = Status('offline',3)
Status.invisible= Status('invisible',3)

class MessageNotificationLevel(object):
    # class related
    INSTANCES = [NotImplemented] * 2
    
    # object related
    __slots__=('name', 'value', )
    
    def __init__(self,value,name):
        self.value=value
        self.name=name

        self.INSTANCES[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'
    
    # predefined
    all_messages    = NotImplemented
    only_mentions   = NotImplemented
    
MessageNotificationLevel.all_messages   = MessageNotificationLevel(0,'all_messages')
MessageNotificationLevel.only_mentions  = MessageNotificationLevel(1,'only_mentions')

class MFA(object):
    # class related
    INSTANCES = [NotImplemented] * 2
    
    # object related
    __slots__=('name', 'value', )
    
    def __init__(self,value,name):
        self.value=value
        self.name=name

        self.INSTANCES[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'

    none    = NotImplemented
    elevated= NotImplemented

MFA.none    = MFA(0,'none')
MFA.elevated= MFA(1,'elevated')

class PremiumType(object):
    # class related
    INSTANCES = [NotImplemented] * 3
    
    # object related
    __slots__=('name', 'value',)
    values={}
    def __init__(self,value,name):
        self.value=value
        self.name=name

        self.INSTANCES[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'
    
    # predefined
    none            = NotImplemented
    nitro_classic   = NotImplemented
    nitro           = NotImplemented

PremiumType.none            = PremiumType(0,'none')
PremiumType.nitro_classic   = PremiumType(1,'nitro_classic')
PremiumType.nitro           = PremiumType(2,'nitro')

class RelationshipType(object):
    #class related
    INSTANCES = [NotImplemented] * 5
    
    # object related
    __slots__=('name', 'value',)
    
    def __init__(self,value,name):
        self.value=value
        self.name=name

        self.INSTANCES[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'
    
    # predefined
    stranger        = NotImplemented
    friend          = NotImplemented
    blocked         = NotImplemented
    received_request= NotImplemented
    sent_request    = NotImplemented

RelationshipType.stranger         = RelationshipType(0,'stranger')
RelationshipType.friend           = RelationshipType(1,'friend')
RelationshipType.blocked          = RelationshipType(2,'blocked')
RelationshipType.received_request = RelationshipType(3,'received_request')
RelationshipType.sent_request     = RelationshipType(4,'sent_request')

class Relationship(object):
    __slots__=('type', 'user',)
    def __init__(self,client,user,data):
        self.user=user
        self.type=RelationshipType.INSTANCES[data['type']]
        client.relationships[user.id]=self
        
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.type.name} user={self.user.full_name}>'

def log_time_converter(value):
    if hasattr(value,'id'):
        return value.id
    
    if isinstance(value,int):
        return value
    
    if isinstance(value,datetime):
        return time_to_id(value)

    raise TypeError(f'Expected Discord type with `.id`, `int` as snowfake, or a `datetime` object, got `{value!r}`')

IS_ID_RP=re.compile('(\d{7,21})')
IS_MENTION_RP=re.compile('@everyone|@here|<@[!&]?\d{7,21}>|<#\d{7,21}>')

USER_MENTION_RP=re.compile('<@!?(\d{7,21})>')
CHANNEL_MENTION_RP=re.compile('<#(\d{7,21})>')
ROLE_MENTION_RP=re.compile('<@&(\d{7,21})>')

EMOJI_RP=re.compile('<([a]{0,1}):([a-zA-Z0-9_]{2,32}(~[1-9]){0,1}):(\d{7,21})>')
EMOJI_NAME_RP=re.compile(':{0,1}([a-zA-Z0-9_\\-~]{1,32}):{0,1}')
FILTER_RP=re.compile('("(.+?)"|\S+)')

def is_id(text):
    return IS_ID_RP.fullmatch(text) is not None

def is_mention(text):
    return IS_MENTION_RP.fullmatch(text) is not None

def is_user_mention(text):
    return USER_MENTION_RP.fullmatch(text) is not None

def is_channel_mention(text):
    return CHANNEL_MENTION_RP.fullmatch(text) is not None

def is_role_mention(text):
    return ROLE_MENTION_RP.fullmatch(text) is not None

def now_as_id():
    return ((time_now()*1000.)-DISCORD_EPOCH).__int__()<<22

#thanks Pythonic#6090 for the simple design
def filter_content(content):
    return [match[1] or match[0] for match in FILTER_RP.findall(content)]

def chunkify(lines,limit=2000):
    result=[]
    ln_count=0
    shard=[]
    for line in lines:
        ln=len(line)+1
        ln_count+=ln
        if ln_count>limit:
            ln_count=ln
            result.append('\n'.join(shard))
            shard.clear()
        shard.append(line)
    result.append('\n'.join(shard))
    return result

def cchunkify(lines,lang='',limit=2000):
    limit=limit-4
    starter=f'```{lang}'
    ln_starter=len(starter)
    
    result=[]
    ln_count=ln_starter
    shard=[starter]
    for line in lines:
        ln=len(line)+1
        ln_count+=ln
        if ln_count>limit:
            ln_count=ln+ln_starter
            shard.append('```')
            result.append('\n'.join(shard))
            shard.clear()
            shard.append(starter)
        shard.append(line)
    if len(shard)>1:
        shard.append('```')
        result.append('\n'.join(shard))
    return result

if (relativedelta is not None):
    __all__=(*__all__,'elapsed_time')
    def elapsed_time(obj,limit=3,names=('years','months','days','hours','minutes','seconds')):
        if type(obj) is datetime:
            delta=relativedelta(datetime.utcnow(),obj)
        elif type(obj) is relativedelta:
            delta=obj
        else:
            raise TypeError(f'Expected, relativedelta or datetime, got {obj!r}')
            
        values=(delta.years,delta.months,delta.days,delta.hours,delta.minutes,delta.seconds)
        result=[]
        is_higher=None
        for index in range(6):
            value=values[index]
            if is_higher is not None:
                result.append(value)
                continue
            if value:
                is_higher=index
                result.append(value)

        del result[limit:]

        text=[]
        for value,name in zip(result,names[is_higher:]):
            if value<0:
                value=-value
            text.append(f'{value} {name}')
        return ', '.join(text)


class Unknown(object):
    __slots__=('id', 'name', 'type', )
    
    def __init__(self,type_,id_,name=''):
        self.type=type_
        self.id=id_
        if name:
            self.name=name
        else:
            self.name=type_
    
    def __repr__(self):
        return f'<{self.__class__.__name__} type={self.type} id={self.id} name=\'{self.name}\'>'

    def __gt__(self,other):
        try:
            other_id=other.id
        except AttributeError:
            return NotImplemented
        
        if self.name in other.__class__.__name__:
            return self.id>other_id
        
        return NotImplemented
        
    def __ge__(self,other):
        try:
            other_id=other.id
        except AttributeError:
            return NotImplemented
        
        if self.name in other.__class__.__name__:
            return self.id>=other_id
        
        return NotImplemented
    
    def __eq__(self,other):
        try:
            other_id=other.id
        except AttributeError:
            return NotImplemented
        
        if self.name in other.__class__.__name__:
            return self.id==other_id
        
        return NotImplemented
    
    def __ne__(self,other):
        try:
            other_id=other.id
        except AttributeError:
            return NotImplemented
        
        if self.name in other.__class__.__name__:
            return self.id!=other_id
        
        return NotImplemented
    
    def __le__(self,other):
        try:
            other_id=other.id
        except AttributeError:
            return NotImplemented
        
        if self.name in other.__class__.__name__:
            return self.id<=other_id
        
        return NotImplemented
    
    def __lt__(self,other):
        try:
            other_id=other.id
        except AttributeError:
            return NotImplemented
        
        if self.name in other.__class__.__name__:
            return self.id<other_id
        
        return NotImplemented

    @property
    def created_at(self):
        return id_to_time(self.id)

#parse image hash formats
def _parse_ih_fs(value):
    if value is None:
        return 0
    if type(value) is str:
        return int(value,16)
    if type(value) is int:
        return value
    raise TypeError(f'Image hash can be `NoneType`, `str` or `int` type, got {value.__class__.__name__}')

#parse image hash formats animated
def _parse_ih_fsa(value,animated):
    if type(animated) is not bool:
        raise TypeError('Animated should be type bool, got {animated.__class__.__name__}')
    if value is None:
        return 0,False
    if type(value) is str:
        if value.startswith('a_'):
            return int(value[2:],16),True
        return int(value,16),animated
    if type(value) is int:
        return value,animated
    raise TypeError(f'Image hash can be `NoneType`, `str` or `int` type, got {value.__class__.__name__}')

class FriendRequestFlag(object):
    # class related
    INSTANCES = [NotImplemented] * 5
    
    @classmethod
    def decode(cls,data):
        if data is None:
            return cls.none
        
        all_=data.get('all',False)
        if all_:
            key=4
        else:
            mutual_guilds=data.get('mutual_guilds',False)
            mutual_friends=data.get('mutual_friends',False)
            
            key=mutual_guilds+(mutual_friends<<1)
        
        return cls.INSTANCES[key]
    
    # object related
    __slots__=('name', 'value',)
    
    def __init__(self,value,name):
        self.value=value
        self.name=name

        self.INSTANCES[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'
    
    def encode(self):
        value=self.value
        if value==0:
            return {}
        
        if value==1:
            return {'mutual_guilds': True}
        
        if value==2:
            return {'mutual_friends': True}
        
        if value==3:
            return {'mutual_guilds': True, 'mutual_friends': True}
        
        if value==4:
            return {'all': True}
        
        # should not happen
        return {}
    
    # predefined
    none                        = NotImplemented
    mutual_guilds               = NotImplemented
    mutual_friends              = NotImplemented
    mutual_guilds_and_friends   = NotImplemented
    all                         = NotImplemented

FriendRequestFlag.none                      = FriendRequestFlag(0,'none')
FriendRequestFlag.mutual_guilds             = FriendRequestFlag(1,'mutual_guilds')
FriendRequestFlag.mutual_friends            = FriendRequestFlag(2,'mutual_friends')
FriendRequestFlag.mutual_guilds_and_friends = FriendRequestFlag(3,'mutual_guilds_and_friends')
FriendRequestFlag.all                       = FriendRequestFlag(4,'all')

class Theme(object):
    INSTANCES = {}
    
    __slots__=('value',)
    values={}
    def __init__(self,value):
        self.value=value
        self.INSTANCES[value]=self

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'<{self.__class__.__name__} value={self.value!r}>'

    @property
    def name(self):
        return self.value

    dark    = NotImplemented
    light   = NotImplemented

Theme.dark  = Theme('dark')
Theme.light = Theme('light')

class Gift(object):
    __slots__=('uses', 'code')
    def __init__(self,data):
        self.uses=data['uses']
        self.code=data['code']

@modulize
class Discord_hdrs:
    #to receive
    AUDIT_LOG_REASON=titledstr('X-Audit-Log-Reason')
    RATELIMIT_REMAINING=titledstr('X-Ratelimit-Remaining')
    RATELIMIT_RESET=titledstr('X-Ratelimit-Reset')
    RATELIMIT_RESET_AFTER=titledstr('X-Ratelimit-Reset-After')

    #to send
    RATELIMIT_PRECISION=titledstr.bypass_titling('X-RateLimit-Precision')

def urlcutter(url):
    if len(url)<50:
        return url
    
    position=url.find('/')
    
    if position==-1:
        return f'{url[:28]}...{url[-19:]}'
    
    position=position+1
    if url[position]=='/':
        position=position+1
        if position==len(url):
            return f'{url[:28]}...{url[-19:]}'
        
        position=url.find('/',position)
        position=position+1
        if position==0 or position==len(url):
            return f'{url[:28]}...{url[-19:]}'
    
    positions=[position]
    
    while True:
        position=url.find('/',position)
        if position==-1:
            break
        position=position+1
        if position==len(url):
            break
        positions.append(position)

    from_start=0
    from_end=0
    top_limit=len(url)
    index=0
    
    while True:
        value=positions[index]
        if value+from_end>47:
            if from_start+from_end<33:
                from_start=47-from_end
                break
            else:
                index=index+1
                if index==len(positions):
                    value=0
                else:
                    value=positions[len(positions)-index]
                value=top_limit-value
                if value+from_start>47:
                    break
                else:
                    from_end=value
                    break
        from_start=value
        
        index=index+1
        value=positions[len(positions)-index]
        value=top_limit-value
        if value+from_start>47:
            if from_start+from_end<33:
                from_end=47-from_start
                break
            else:
                if index==len(positions):
                    value=top_limit
                else:
                    value=positions[index]
                
                if value+from_end>47:
                    break
                else:
                    from_start=value
                    break
        from_end=value
        
    return f'{url[:from_start]}...{url[top_limit-from_end-1:]}'

del re, titledstr, modulize


# -*- coding: utf-8 -*-
__all__ = ('ContentFilterLevel', 'DISCORD_EPOCH', 'FriendRequestFlag', 'Gift', 'HypesquadHouse', 'MFA',
    'MessageNotificationLevel', 'PremiumType', 'Relationship', 'RelationshipType', 'Status', 'Theme', 'Unknown',
    'VerificationLevel', 'VoiceRegion', 'cchunkify', 'chunkify', 'filter_content', 'id_to_time', 'is_id', 'is_mention',
    'is_role_mention', 'is_user_mention', 'now_as_id', 'random_id', 'time_to_id', )

import random, re, sys
from datetime import datetime
from base64 import b64encode
from time import time as time_now
from json import dumps as dump_to_json, loads as from_json

try:
    from dateutil.relativedelta import relativedelta
except ImportError:
    relativedelta = None

from ..backend.dereaddons_local import titledstr, modulize

from .bases import DiscordEntity

from . import bases

PartialUser = NotImplemented

def endswith_xFFxD9(data):
    """
    Checks whether the given data endswith `b'\xD9\xFF'` ignoring empty bytes at the end of it.
    
    Parameters
    ----------
    data : `bytes-like`
    
    Returns
    -------
    result : `bool`
    """
    index = len(data)-1
    while index > 1:
        actual = data[index]
        if actual == b'\xD9'[0] and data[index-1] == b'\xFF'[0]:
            return True
        
        if actual:
            return False
        
        index -=1
        continue
        
def get_image_extension(data):
    """
    Gets the given raw image data's extension and returns it.
    
    Parameters
    ----------
    data : `bytes-like`
        Image data.
    
    Returns
    -------
    extension_name : `str`
    """
    if data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
        extension_name = 'png'
    elif data.startswith(b'\xFF\xD8') and endswith_xFFxD9(data):
        extension_name = 'jpeg'
    elif data.startswith(b'\x47\x49\x46\x38\x37\x61') or data.startswith(b'\x47\x49\x46\x38\x39\x61'):
        extension_name = 'gif'
    else:
        raise ValueError('Unsupported image type given.')
    
    return extension_name

def image_to_base64(data):
    """
    Converts a bytes image to a base64 one.
    
    Parameter
    ----------
    data : `bytes-like`
        Image data.
    
    Returns
    -------
    base64 : `str`
    
    Raises
    ------
    ValueError
        If `ext` was not given and the given `data`'s image format is not any of the expected ones.
    """
    if data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
        extension_value = 'image/png'
    elif data.startswith(b'\xFF\xD8') and endswith_xFFxD9(data):
        extension_value = 'image/jpeg'
    elif data.startswith(b'\x47\x49\x46\x38\x37\x61') or data.startswith(b'\x47\x49\x46\x38\x39\x61'):
        extension_value = 'image/gif'
    else:
        raise ValueError('Unsupported image type given.')
    
    return ''.join(['data:', extension_value, ';base64,', b64encode(data).decode('ascii')])

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
    """
    Parses the given timestamp.
    
    The expected timestamp formats are the following:
        - `2019-04-28T15:14:38+00:00`
        - `2019-07-17T18:52:50.758993+00:00`
        - `2019-07-17T18:52:50.758000+00:00`
        
    Discord might give timestamps with different accuracy, so we use an optimal middle way at parsing them.
    Some events depend on timestamp accuracy, so we really do not want to be wrong about them, or it might cause
    same internal derpage.
    
    If parsing a timestamp failed, the start of the discord epoch is returned and an error message is given at
    `sys.stderr`.
    
    Parameters
    ----------
    timestamp : `str`
    
    Returns
    -------
    time : `datetime`
    
    Notes
    -----
    I already noted that timestamp formats are inconsistent, but even our baka Chiruno could have fix it...
    """
    parsed=PARSE_TIME_RP.fullmatch(timestamp)
    if parsed is None:
        sys.stderr.write(f'Cannot parse timestamp: `{timestamp}`, returning `DISCORD_EPOCH_START`\n')
        return DISCORD_EPOCH_START
    
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
    """
    Converts the given id to datetime.
    
    Parameters
    ----------
    id_ : `int`
        Unique identificator number of a Discord entity.
    
    Returns
    -------
    time : `datetime`
    """
    return datetime.utcfromtimestamp(((id_>>22)+DISCORD_EPOCH)/1000.)

DISCORD_EPOCH_START = id_to_time(0)

def time_to_id(time):
    """
    Converts the given time to it's respective discord identitifactor number.
    
    Parameters
    ----------
    time : `datetime`
    
    Returns
    -------
    id_ `int`
    """
    return ((time.timestamp()*1000.).__int__()-DISCORD_EPOCH)<<22

def random_id():
    """
    Generates a random Discord identificator number what's datetime value did not surpass the current time.
    
    Returns
    -------
    id_ `int`
    """
    return (((time_now()*1000.).__int__()-DISCORD_EPOCH)<<22)+(random.random()*4194304.).__int__()

def added_json_serializer(obj):
    """
    Default json encoder function for supporting additional object types.
    
    Parameters
    ----------
    obj : `iterable`
    
    Returns
    -------
    result : `Any`
    
    Raises
    ------
    TypeError
        If the given object is not json serializable.
    """
    obj_type = obj.__class__
    if hasattr(obj_type, '__iter__'):
        return list(obj)
    
    raise TypeError(f'Object of type {obj_type.__name__!r} is not JSON serializable.',)

def to_json(data):
    """
    Converts the given object to json.
    
    Parameters
    ----------
    data : `Any`
    
    Returns
    -------
    json : `str`
    
    Raises
    ------
    TypeError
        If the given object is /or contains an object with a non convertable type.
    """
    return dump_to_json(data, separators=(',',':'), ensure_ascii=True, default=added_json_serializer)

class VerificationLevel(object):
    """
    Represents Discord's verification level.
    
    Attributes
    ----------
    name : `str`
        The name of the verification level.
    value : `int`
        The discord side identificator value of the verification level.
    
    Class Attributes
    ----------------
    INSTANCES : `list` of ``VerificationLevel``
        Stores the predefined ``VerificationLevel`` instances. These can be accessed with their `value` as index.
    
    Every predefind verification level can be accessed as class attribute as well:
    
    +-----------------------+-----------+-------+
    | Class attribute name  | name      | value |
    +=======================+===========+=======+
    | none                  | none      | 0     |
    +-----------------------+-----------+-------+
    | low                   | low       | 1     |
    +-----------------------+-----------+-------+
    | medium                | medium    | 2     |
    +-----------------------+-----------+-------+
    | high                  | high      | 3     |
    +-----------------------+-----------+-------+
    | extreme               | extreme   | 4     |
    +-----------------------+-----------+-------+
    """
    # class related
    INSTANCES = [NotImplemented] * 5
    
    # object related
    __slots__=('name', 'value',)
    
    def __init__(self, value, name):
        """
        Creates a ``VerificationLevel`` and stores it at the classe's `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identificator value of the verification level.
        name : `str`
            The name of the verification level.
        """
        self.value=value
        self.name=name
        
        self.INSTANCES[value]=self
    
    def __str__(self):
        """Returns the name of the verification level."""
        return self.name
    
    def __int__(self):
        """Returns the value of the verificaiton level."""
        return self.value
    
    def __repr__(self):
        """Returns the representation of the verificaiton level."""
        return f'{self.__class__.__name__}(value={self.value!r}, name={self.name!r})'
    
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
    """
    Represents Discord's voice regions.
    
    Attributes
    ----------
    custom : `bool`
        Whether the voice region is custom (used for events, etc.).
    deprecated : `bool`
        Whether the voice region is deprecated.
    id : `str`
        The unique identificator of the voice region.
    name : `str`
        The name of the voice region.
    vip : `bool`
        Whether the voice region can be used only by guilds with `VIP_REGIONS` feature.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``VoiceRegion``) items
        Stores the created ``VoiceRegion`` instances.
    
    Each predefined voice region is also stored as a class attribute:
    
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | Class attribute name  | id            | name              | deprecated    | vip       | custom    |
    +=======================+===============+===================+===============+===========+===========+
    | brazil                | brazil        | Brazil            | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | dubai                 | dubai         | Dubai             | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | eu_central            | eu-central    | Central Europe    | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | eu_west               | eu-west       | Western Europe    | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | europe                | europe        | Europe            | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | hongkong              | hongkong      | Hong Kong         | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | india                 | india         | India             | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | japan                 | japan         | Japan             | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | russia                | russia        | Russia            | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | singapore             | singapore     | Singapore         | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | southafrica           | southafrica   | South Africa      | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | sydney                | sydney        | Sydney            | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | us_central            | us-central    | US Central        | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | us_east               | us-east       | US East           | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | us_south              | us-south      | US South          | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | us_west               | us-west       | US West           | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | amsterdam             | amsterdam     | Amsterdam         | True          | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | frankfurt             | frankfurt     | Frankfurt         | True          | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | london                | london        | London            | True          | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | vip_us_east           | vip-us-east   | VIP US West       | False         | True      | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | vip_us_west           | vip-us-west   | VIP US East       | False         | True      | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | vip_amsterdam         | vip-amsterdam | VIP Amsterdam     | True          | True      | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    """
    # class related
    INSTANCES = {}
    
    @classmethod
    def get(cls, id_):
        """
        Accessed to get a voice region from `.INSTANCES` by it's `id`. If no already defined voice region is found,
        a new ONE is created.
        
        Parameters
        ----------
        id_ : `str`
            The identificator of the voice region.
        
        Returns
        -------
        voice_region : ``VoiceRegion``
        """
        try:
            voice_region=cls.INSTANCES[id_]
        except KeyError:
            voice_region=cls._from_id(id_)
        
        return voice_region
    
    @classmethod
    def _from_id(cls, id_):
        """
        Creates a voice region from the given id and stores it at classe's `.INSTANCES`.
        
        Called by `.get` when no voice region was found with the given id.
        
        Parameters
        ----------
        id_ : `str`
            The identificator of the voice region.
        
        Returns
        -------
        voice_region : ``VoiceRegion``
        """
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
    def from_data(cls, data):
        """
        Creates a voice region from the given data and stores it at the classe's `.INSTANCES`.
        
        If the voice region already exsists returns that instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received voice region data.

        Returns
        -------
        self : ``VoiceRegion``
        """
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
    
    def __init__(self, name, id_, deprecated, vip):
        """
        Creates a new voice region with the given parameters and stores it at the classe's `.INSTANCES`.
        
        Parameters
        ----------
        deprecated : `bool`
            Whether the voice region is deprecated.
        id_ : `str`
            The unique identificator of the voice region.
        name : `str`
            The name of the voice region.
        vip : `bool`
            Whether the voice region can be used only by guilds with `VIP_REGIONS` feature.
        """
        self.name           = name
        self.id             = id_
        self.deprecated     = deprecated
        self.vip            = vip
        self.custom         = False
        self.INSTANCES[id_] = self
    
    def __str__(self):
        """Returns the voice region's name."""
        return self.name
    
    def __repr__(self):
        """Returns the representation of the voice region."""
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
    """
    Represents Discord's content filter level.
    
    Attributes
    ----------
    value : `int`
        The Discord side identificator value of the content filter level.
    name : `str`
        The name of the content filter level.
    
    Class Attributes
    ----------------
    INSTANCES : `list` of ``ContentFilterLevel``
        Stores the predefined content filter levels. This container is accessed when translating a Discord side
        identificator of a content filter level. The identificator value is used as an index to get it's wrapper side
        representation.
    
    Every predefined content filter level is also stored as a class attribute:
    
    +-----------------------+-----------+-------+
    | Class attribute name  | name      | value |
    +=======================+===========+=======+
    | disabled              | disabled  | 0     |
    +-----------------------+-----------+-------+
    | no_role               | no_role   | 1     |
    +-----------------------+-----------+-------+
    | everyone              | everyone  | 2     |
    +-----------------------+-----------+-------+
    """
    # class related
    INSTANCES = [NotImplemented] * 3
    
    # object related
    __slots__=('name', 'value', )
    
    def __init__(self, value, name):
        """
        Creates a new content filter level instance with the given parameters and stores it at the classe's
        `.INSTANCES` class attribute.
        
        Parameters
        ----------
        value : `int`
            The Discord side identificator value of the content filter level.
        name : `str`
            The name of the content filter level.
        """
        self.value=value
        self.name=name
        
        self.INSTANCES[value]=self
    
    def __str__(self):
        """Returns the content filter level's name."""
        return self.name
    
    def __int__(self):
        """Returns the content filter level's value."""
        return self.value
    
    def __repr__(self):
        """Returns the representation of the content filter level."""
        return f'{self.__class__.__name__}(value={self.value!r}, name={self.name!r})'
    
    # predefined
    disabled    = NotImplemented
    no_role     = NotImplemented
    everyone    = NotImplemented

ContentFilterLevel.disabled = ContentFilterLevel(0,'disabled')
ContentFilterLevel.no_role  = ContentFilterLevel(1,'no_role')
ContentFilterLevel.everyone = ContentFilterLevel(2,'everyone')

class HypesquadHouse(object):
    """
    Represents Discord's hypesquad house.
    
    Attributes
    ----------
    value : `int`
        The Discord side identificator value of the hypesquad house.
    name : `str`
        The name of the hypesquad house.
    
    Class Attributes
    ----------------
    INSTANCES : `list` of ``HypesquadHouse``
        Stores the predefined hypesquad houses. This container is accessed when converting Discord side hypesquad
        house's value to it's wrapper side representation.
    
    Every predefined hypesquad house can also be accessed as class attribute:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | name          | value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | bravery               | bravery       | 1     |
    +-----------------------+---------------+-------+
    | brilliance            | brilliance    | 2     |
    +-----------------------+---------------+-------+
    | balance               | balance       | 3     |
    +-----------------------+---------------+-------+
    """
    # class related
    INSTANCES = [NotImplemented] * 4
    
    #object related
    __slots__=('name', 'value', )
    
    def __init__(self, value, name):
        """
        Creates a hypeaquad house instance with the given parameters and stores it at the classe's
        `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identificator value of the hypesquad house.
        name : `str`
            The name of the hypesquad house.
        """
        self.value=value
        self.name=name

        self.INSTANCES[value]=self

    def __str__(self):
        """Returns the hypesquad house's name."""
        return self.name

    def __int__(self):
        """Returns the hypesquad house's value."""
        return self.value

    def __repr__(self):
        """Returns the representation of the hypesquad house."""
        return f'{self.__class__.__name__}(value={self.value!r}, name={self.name!r})'
    
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
    """
    Represents a Discord user's status.
    
    Attributes
    ----------
    position : `int`
        Internal position of the status for sorting purposes.
    value : `str`
        The identificator value of the status.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``Status``) items
        A container what stores the predefined statuses in `value` - `status relation. This container is acccessed
        when translating status value to ``Status`` object.
    
    Each predefined status also can be accessed as a class attribute:
    
    +-----------------------+-----------+-----------+
    | Class attribute name  | position  | value     |
    +=======================+===========+===========+
    | online                | 0         | idle      |
    +-----------------------+-----------+-----------+
    | idle                  | 1         | idle      |
    +-----------------------+-----------+-----------+
    | dnd                   | 2         | dnd       |
    +-----------------------+-----------+-----------+
    | offline               | 3         | offline   |
    +-----------------------+-----------+-----------+
    | invisible             | 3         | invisible |
    +-----------------------+-----------+-----------+
    """
    # class related
    INSTANCES = {}
    
    # object related
    __slots__ = ('position', 'value', )
    
    def __init__(self, value, position):
        """
        Creates a new status and stores it at the classe's `.INSTANCES` class attribute.
        
        Parameters
        ----------
        value : `str`
            The identificator value of the status.
        position : `int`
            Internal position of the status for sorting purposes.
        """
        self.value=value
        self.position=position
        self.INSTANCES[value]=self

    def __str__(self):
        """Returns the status's value."""
        return self.value
    
    name = property(__str__)
    if (__str__.__doc__ is not None):
        name.__doc__ = (
        """
        Returns the statuse's value.
        
        This property is mainly for compatibility purposes.
        
        Returns
        -------
        value : `str`
        """)
    
    def __repr__(self):
        """Returns the representation of the status."""
        return f'<{self.__class__.__name__} value={self.value!r}>'
    
    def __gt__(self, other):
        """Returns whether this statuse's position is greater than the other's."""
        if type(self) is type(other):
            pass
        elif isinstance(other,str):
            try:
                other=type(self).INSTANCES[other]
            except KeyError:
                return NotImplemented
        else:
            return NotImplemented
        
        if self.position > other.position:
            return True
        
        return False
    
    def __ge__(self,other):
        """Returns whether this statuse's position is greater than the other's or whether the two status is equal."""
        if type(self) is type(other):
            pass
        elif isinstance(other, str):
            try:
                other=type(self).INSTANCES[other]
            except KeyError:
                return NotImplemented
        else:
            return NotImplemented
        
        self_position = self.position
        other_position = other.position
        if self_position > other_position:
            return True
        
        if self_position < other_position:
            return False
        
        if self.value == other.value:
            return True
        
        return False
    
    def __eq__(self,other):
        """Returns whether the two status is equal."""
        if type(self) is type(other):
            pass
        elif isinstance(other, str):
            try:
                other=type(self).INSTANCES[other]
            except KeyError:
                return NotImplemented
        else:
            return NotImplemented
    
        if self.position != other.position:
            return False
        
        if self.value == other.value:
            return True
        
        return False
    
    def __ne__(self,other):
        """Returns whether the two status is not equal."""
        if type(self) is type(other):
            pass
        elif isinstance(other, str):
            try:
                other=type(self).INSTANCES[other]
            except KeyError:
                return NotImplemented
        else:
            return NotImplemented
        
        if self.position != other.position:
            return True
            
        if self.value == other.value:
            return False
        
        return True
    
    def __le__(self, other):
        """Returns whether this statuse's position is less than the other's or whether the two status is equal."""
        if type(self) is type(other):
            pass
        elif isinstance(other, str):
            try:
                other=type(self).INSTANCES[other]
            except KeyError:
                return NotImplemented
        else:
            return NotImplemented
        
        self_position = self.position
        other_position = other.position
        if self_position < other_position:
            return True
        
        if self_position > other_position:
            return False
        
        if self.value == other.value:
            return True
        
        return False
    
    def __lt__(self ,other):
        """Returns whether this statuse's position is less than the other's."""
        if type(self) is type(other):
            pass
        elif isinstance(other, str):
            try:
                other=type(self).INSTANCES[other]
            except KeyError:
                return NotImplemented
        else:
            return NotImplemented
        
        if self.position < other.position:
            return True
        
        return False
    
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
    """
    Represents the default message notificaiton level of a ``Guild``.
    
    Attributes
    ----------
    value : `int`
        The Discord side identificator value of the message notificaiton level.
    name : `str`
        The name of the message notificaiton level.
    
    Class Attributes
    ----------------
    INSTANCES : `list` of ``MessageNotificationLevel``
        Stores the predefined message notification levels. This container is accessed when translating message
        notification level's value to it's representation.
    
    Each predefined message notificaiton level can also be accessed as a class attribute:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | name          | value |
    +=======================+===============+=======+
    | all_messages          | all_messages  | 0     |
    +-----------------------+---------------+-------+
    | only_mentions         | only_mentions | 1     |
    +-----------------------+---------------+-------+
    | no_message            | no_messages   | 2     |
    +-----------------------+---------------+-------+
    | null                  | null          | 3     |
    +-----------------------+---------------+-------+
    """
    # class related
    INSTANCES = [NotImplemented] * 4
    
    # object related
    __slots__=('name', 'value', )
    
    def __init__(self, value, name):
        """
        Creates a new message notifcaiton object with the given parameters and stores it at the classe's
        `.INSTANCES` class attribute.
        
        Parameters
        ----------
        value : `int`
            The Discord side identificator value of the message notificaiton level.
        name : `str`
            The name of the message notificaiton level.
        """
        self.value=value
        self.name=name

        self.INSTANCES[value]=self
    
    def __str__(self):
        """Returns the message notification level's name."""
        return self.name
    
    def __int__(self):
        """Returns the message notificaiton level's value."""
        return self.value
    
    def __repr__(self):
        """Returns the message notification level's representaion."""
        return f'{self.__class__.__name__}(value={self.value!r}, name={self.name!r})'
    
    # predefined
    all_messages   = NotImplemented
    only_mentions  = NotImplemented
    no_messages    = NotImplemented
    null           = NotImplemented

MessageNotificationLevel.all_messages  = MessageNotificationLevel(0, 'all_messages')
MessageNotificationLevel.only_mentions = MessageNotificationLevel(1, 'only_mentions')
MessageNotificationLevel.no_messages   = MessageNotificationLevel(2, 'no_messages')
MessageNotificationLevel.null          = MessageNotificationLevel(3, 'null')


class MFA(object):
    """
    Represents Discord's Multi-Factor Authentication's levels.
    
    Attributes
    ----------
    name : `str`
        The name of the MFA level.
    value : `int`
        The Discord side identificator value of the MFA level.
    
    Class Attributes
    ----------------
    INSTANCES : `list` of ``MFA``
        Stores the predefined MFA level. This container is accessed when converting an MFA level's value to
        it's wrapper side representation.
    
    Each predefined MFA can also be accessed as class attribute:
    
    +-----------------------+-----------+-------+
    | Class attribute name  | name      | value |
    +=======================+===========+=======+
    | none                  | none      | 0     |
    +-----------------------+-----------+-------+
    | elevated              | elevated  | 1     |
    +-----------------------+-----------+-------+
    """
    # class related
    INSTANCES = [NotImplemented] * 2
    
    # object related
    __slots__=('name', 'value', )
    
    def __init__(self, value, name):
        """
        Creates a new MFA level and stores it at the classe's `.INSTANCES.` class attribute.
        
        Parameters
        ----------
        value : `int`
            The Discord side identificator value of the MFA level.
        name : `str`
            The name of the MFA level.
        """
        self.value=value
        self.name=name

        self.INSTANCES[value]=self

    def __str__(self):
        """Returns the name of the MFA level."""
        return self.name

    def __int__(self):
        """Returns the value of the MFA level."""
        return self.value

    def __repr__(self):
        """Returns the representation of the MFA level."""
        return f'{self.__class__.__name__}(value={self.value!r}, name={self.name!r})'

    none    = NotImplemented
    elevated= NotImplemented

MFA.none    = MFA(0,'none')
MFA.elevated= MFA(1,'elevated')

class PremiumType(object):
    """
    Represents Discord's premium types.
    
    Attributes
    ----------
    name : `str`
        The name of the premium type.
    value : `int`
        The Discord side identificator value of the premium type.
    
    Class Attributes
    ----------------
    INSTANCES : `list` of ``PremiumType``
        A container what stores the predefined premium types and also is accessed when translating their identificator
        value to their representation.
    
    Each predefined premium type can also be accessed as class attribute:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | name          | value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | nitro_classic         | nitro_classic | 1     |
    +-----------------------+---------------+-------+
    | nitro                 | nitro         | 2     |
    +-----------------------+---------------+-------+
    """
    # class related
    INSTANCES = [NotImplemented] * 3
    
    # object related
    __slots__=('name', 'value',)
    
    def __init__(self, value, name):
        """
        Creates a new ``PremiumType`` instance and also stores it at the classe's `.INSTANCES` class attribute.
        
        Parameters
        ----------
        value : `int`
            The Discord side identificator value of the premium type.
        name : `str`
            The name of the premium type.
        """
        self.value=value
        self.name=name

        self.INSTANCES[value]=self
    
    def __str__(self):
        """Returns the name of the premium type."""
        return self.name
    
    def __int__(self):
        """Returns the value of the premium type."""
        return self.value
    
    def __repr__(self):
        """Returns the representation of the premium type."""
        return f'{self.__class__.__name__}(value={self.value!r}, name={self.name!r})'
    
    # predefined
    none            = NotImplemented
    nitro_classic   = NotImplemented
    nitro           = NotImplemented

PremiumType.none            = PremiumType(0,'none')
PremiumType.nitro_classic   = PremiumType(1,'nitro_classic')
PremiumType.nitro           = PremiumType(2,'nitro')

class RelationshipType(object):
    """
    Represents a ``Relationship``'s type.
    
    Attributes
    ----------
    name : `str`
        The relationship type's name.
    value : `int`
        The Discord side identificator value of the relationship type.
    
    Class Attributes
    ----------------
    INSTANCES : `list` of ``RelationshipType``
        The predefined relation types stored in a list, so they can be accessed with their respective value as index.
        This behaviour is used to translate their Disord side value to their representation.
    
    Each predefined relationship type can also be accessed as class attribute:
    
    +-----------------------+-------------------+-------+
    | Class attribute name  | name              | value |
    +=======================+===================+=======+
    | stranger              | stranger          | 0     |
    +-----------------------+-------------------+-------+
    | friend                | friend            | 1     |
    +-----------------------+-------------------+-------+
    | blocked               | blocked           | 2     |
    +-----------------------+-------------------+-------+
    | pending_incoiming     | pending_incoiming | 3     |
    +-----------------------+-------------------+-------+
    | pending_outgoing      | pending_outgoing  | 4     |
    +-----------------------+-------------------+-------+
    | implicit              | implicit          | 5     |
    +-----------------------+-------------------+-------+
    """
    #class related
    INSTANCES = [NotImplemented] * 6
    
    # object related
    __slots__=('name', 'value',)
    
    def __init__(self, value, name):
        """
        Creates a new relation type instance with the given parameters and also stores it at the classe's `.INSTANCES`
        class attribute.
        
        Parameters
        ----------
        value : `int`
            The Discord side identificator value of the relationship type.
        name : `str`
            The relationship type's name.
        """
        self.value=value
        self.name=name

        self.INSTANCES[value]=self

    def __str__(self):
        """Returns the name of the relationship type."""
        return self.name

    def __int__(self):
        """Returns the identificator value of the relationship type."""
        return self.value

    def __repr__(self):
        """Returns the representation of the relationship type."""
        return f'{self.__class__.__name__}(value={self.value!r}, name={self.name!r})'
    
    # predefined
    stranger          = NotImplemented
    friend            = NotImplemented
    blocked           = NotImplemented
    pending_incoiming = NotImplemented
    pending_outgoing  = NotImplemented
    implicit          = NotImplemented

RelationshipType.stranger          = RelationshipType(0, 'stranger')
RelationshipType.friend            = RelationshipType(1, 'friend')
RelationshipType.blocked           = RelationshipType(2, 'blocked')
RelationshipType.pending_incoiming = RelationshipType(3, 'pending_incoiming')
RelationshipType.pending_outgoing  = RelationshipType(4, 'pending_outgoing')
RelationshipType.implicit          = RelationshipType(5, 'implicit')

class Relationship(object):
    """
    Represents a Discord relationship.
    
    Attrbiutes
    ----------
    type : ``RelationshipType``
        The relationship's type.
    user : ``User`` or ``Client`` instance
        The target user of the relationship.
    """
    __slots__=('type', 'user',)
    def __init__(self, client, data, user_id):
        """
        Creates a relationship instance with the given parameters.
        
        Parameters
        ----------
        client : ``Client``
            The client, who's relationship is created.
        data : `dict` of (`str`, `Any`)
            Relationship data.
        user_id : `int`
            The relationship's target user's id.
        """
        self.user = PartialUser(user_id)
        self.type = RelationshipType.INSTANCES[data['type']]
        client.relationships[user_id] = self
    
    def __repr__(self):
        """Returns the representation of the relationship."""
        return f'<{self.__class__.__name__} {self.type.name} user={self.user.full_name!r}>'

def log_time_converter(value):
    """
    Converts the given value to it's snowflake representation.
    
    Parameters
    ----------
    value : `int`, ``DiscordEntity`` instance or `datetime`
        If the value is given as `int`, returns it. If given as a ``DiscordEntity``, then returns it's id and if it
        is given as a `datetime` object, then converts that to snowfalke then returns it.
    
    Returns
    -------
    snowfalke : `int`
    
    Raises
    ------
    TypeError
        If the given `value`'s type is not any of the expected ones.
    """
    if isinstance(value,int):
        return value
    
    if isinstance(value, DiscordEntity):
        return value.id
    
    if type(value) is datetime:
        return time_to_id(value)
    
    raise TypeError(f'Expected `int`, `{DiscordEntity.__name__}` instance, or a `datetime` object, got '
        f'`{value.__class__.__name__}`.')

IS_ID_RP=re.compile('(\d{7,21})')
IS_MENTION_RP=re.compile('@everyone|@here|<@[!&]?\d{7,21}>|<#\d{7,21}>')

USER_MENTION_RP=re.compile('<@!?(\d{7,21})>')
CHANNEL_MENTION_RP=re.compile('<#(\d{7,21})>')
ROLE_MENTION_RP=re.compile('<@&(\d{7,21})>')

EMOJI_RP=re.compile('<([a]{0,1}):([a-zA-Z0-9_]{2,32}(~[1-9]){0,1}):(\d{7,21})>')
EMOJI_NAME_RP=re.compile(':{0,1}([a-zA-Z0-9_\\-~]{1,32}):{0,1}')
FILTER_RP=re.compile('("(.+?)"|\S+)')

def is_id(text):
    """
    Returns whether the given text is a valid snowflake.
    
    Parameters
    ----------
    text : `str`
    
    Returns
    -------
    result : `bool`
    """
    return IS_ID_RP.fullmatch(text) is not None

def is_mention(text):
    """
    Returns whether the given text is a mention.
    
    Parameters
    ----------
    text : `str`
    
    Returns
    -------
    result : `bool`
    """
    return IS_MENTION_RP.fullmatch(text) is not None

def is_user_mention(text):
    """
    Returns whether the given text mentions a user.
    
    Parameters
    ----------
    text : `str`
    
    Returns
    -------
    result : `str`
    """
    return USER_MENTION_RP.fullmatch(text) is not None

def is_channel_mention(text):
    """
    Returns whether the given text mentions a channel.
    
    Parameters
    ----------
    text : `str`

    Returns
    -------
    result : `bool`
    """
    return CHANNEL_MENTION_RP.fullmatch(text) is not None

def is_role_mention(text):
    """
    Returns whether the given text mentions a role.
    
    Parameters
    ----------
    text : `str`

    Returns
    -------
    result : `bool`
    """
    return ROLE_MENTION_RP.fullmatch(text) is not None

def now_as_id():
    """
    Returns the current time as a Discord snowflake.

    Returns
    -------
    snowflake : `int`
    """
    return ((time_now()*1000.)-DISCORD_EPOCH).__int__()<<22

def filter_content(content):
    """
    Filters the given content to parts separated with spaces. Parts surrounded with `"` character will count as one
    even if they contain spaces.
    
    Parameters
    ----------
    content : `str`
    
    Returns
    -------
    parts : `list` of `str`
    """
    return [match[1] or match[0] for match in FILTER_RP.findall(content)]

def chunkify(lines, limit=2000):
    """
    Creates chunks of strings from the given lines.
    
    Parameters
    ----------
    lines : `list` of `str`
        Lines of text to be chunkified.
    limit : `int`, Optional
        The maximal length of a generated chunk.
    
    Returns
    -------
    result : `list` of `str`
    
    Raises
    ------
    ValueError`
        If limit is less than `500`.
    """
    if limit<500:
        raise ValueError(f'Minimal limit should be at least 500, got {limit!r}.')
    
    result=[]
    chunk_ln=0
    chunk=[]
    for line in lines:
        while True:
            ln=len(line)+1
            if chunk_ln+ln>limit:
                position=limit-chunk_ln
                if position<250:
                    result.append('\n'.join(chunk))
                    chunk.clear()
                    chunk.append(line)
                    chunk_ln=ln
                    break
                
                position=line.rfind(' ',position-250,position-3)
                if position==-1:
                    position = limit-chunk_ln-3
                    post_part=line[position:]
                else:
                    post_part=line[position+1:]
                
                pre_part=line[:position]+'...'
                
                chunk.append(pre_part)
                result.append('\n'.join(chunk))
                chunk.clear()
                if len(post_part)>limit:
                    line=post_part
                    chunk_ln=0
                    continue
                
                chunk.append(post_part)
                chunk_ln=len(post_part)+1
                break
            
            chunk.append(line)
            chunk_ln+=ln
            break
    
    result.append('\n'.join(chunk))
    
    return result

def cchunkify(lines, lang='', limit=2000):
    """
    Creates code block chunks from the given lines.
    
    Parameters
    ----------
    lines : `list` of `str`
        Lines of text to be chunkified.
    lang : `str`, Optional
        Language prefix of the codeblock.
    limit : `int`, Optional
        The maximal length of a generated chunk.
    
    Returns
    -------
    result : `list` of `str`
    
    Raises
    ------
    ValueError`
        If limit is less than `500`.
    """
    if limit<500:
        raise ValueError(f'Minimal limit should be at least 500, got {limit!r}.')
    
    starter=f'```{lang}'
    limit=limit-len(starter)-5
    
    result=[]
    chunk_ln=0
    chunk=[starter]
    for line in lines:
        while True:
            ln=len(line)+1
            if chunk_ln+ln>limit:
                position=limit-chunk_ln
                if position<250:
                    chunk.append('```')
                    result.append('\n'.join(chunk))
                    chunk.clear()
                    chunk.append(starter)
                    chunk.append(line)
                    chunk_ln=ln
                    break
                
                position=line.rfind(' ',position-250,position-3)
                if position==-1:
                    position = limit-chunk_ln-3
                    post_part=line[position:]
                else:
                    post_part=line[position+1:]
                
                pre_part=line[:position]+'...'
                
                chunk.append(pre_part)
                chunk.append('```')
                result.append('\n'.join(chunk))
                chunk.clear()
                chunk.append(starter)
                
                if len(post_part)>limit:
                    line=post_part
                    chunk_ln=0
                    continue
                
                chunk.append(post_part)
                chunk_ln=len(post_part)+1
                break
            
            chunk.append(line)
            chunk_ln+=ln
            break
    
    if len(chunk)>1:
        chunk.append('```')
        result.append('\n'.join(chunk))
    
    return result

if (relativedelta is not None):
    __all__=(*__all__,'elapsed_time')
    def elapsed_time(delta, limit=3, names=(
            ('year', 'years',),
            ('month', 'months'),
            ('day', 'days', ),
            ('hour', 'hours'),
            ('minute', 'minutes'),
            ('second', 'seconds'),)):
        """
        Generates an elapsed time formula from the given time delta.
        
        Parameters
        ----------
        delta : `datetime` or `relativedelta`
            The time delta. If given as `datetime`, then the delta will be based on the difference between the given
            datetime and the actual time. If given as `relativedelta`, then that will be used directly.
        limit : `int`, Optional
            The maximal amount of connected time units. Defaults to `3`.
        names : `iterable` of `tuple` (`str`, `str`), Optional
            The names of the time units starting from years. Each element of the iterable should yield a `tuple` of two
            `str` elements. The first should be always the singular form of the time unit's name and the second the
            plural. Defaults to the time units' names in engrisssh.
        
        Returns
        -------
        result : `None` or `str`
        
        Raises
        ------
        TypeError
            If delta was neither passed as `datetime` or as `relativedelta` instance.
        """
        if type(delta) is datetime:
            delta = relativedelta(datetime.utcnow(),delta)
        elif type(delta) is relativedelta:
            pass
        else:
            raise TypeError(f'Expected, `relativedelta` or `datetime`, got {delta.__class__.__name__}.')
        
        parts = []
        for value, name_pair in zip((delta.years, delta.months, delta.days, delta.hours, delta.minutes, delta.seconds), names):
            if limit == 0:
                break
            
            if value<0:
                 value = -value
            elif value == 0:
                continue
            
            parts.append(str(value))
            parts.append(' ')
            
            if value == 1:
                name = name_pair[0]
            else:
                name = name_pair[1]
            
            parts.append(name)
            parts.append(', ')
            
            limit -=1
        
        if parts:
            del parts[-1]
            result = ''.join(parts)
        else:
            result = None
        
        return result

class Unknown(DiscordEntity):
    """
    Represents a not found object when creating an ``AuditLog``.
    
    Attributes
    ----------
    id : `int`
        The entitiy's unique identificator number.
    name : `str`
        The entity's name.
    type : `str`
        The entity's respective type's respective name.
        
        Can be one of:
        - `'Channel'`
        - `'Emoji'`
        - `'Integration'`
        - `'Invite'`
        - `'Message'`
        - `'Role'`
        - `'User'`
        - `'Webhook'`
    """
    __slots__=('name', 'type', )
    
    def __init__(self, type_, id_, name=None):
        """
        Creates a new ``Unknown`` object from the given parameters.
        
        Parameters
        ----------
        type_ : `str`
            The entity's respective type's respective name.
        id_ : `int`
            The entitiy's unique identificator number.
        name : `str`, Optional
            The name of the entity if applicable. If not, `type_` will be used as name instead.
        """
        self.type=type_
        self.id=id_
        if name is None:
            name = type_
        self.name = name
    
    def __repr__(self):
        """Returns the representation of the entity."""
        return f'<{self.__class__.__name__} type={self.type} id={self.id} name={self.name!r}>'
    
    def __gt__(self, other):
        """Returns whether this entity's respective type matches with the other's and it's id is greater than the
        other's."""
        if type(other) is type(self):
            if self.type != other.type:
                return NotImplemented
        elif isinstance(other, DiscordEntity):
            if self.type not in other.__class__.__name__:
                return NotImplemented
        else:
            return NotImplemented
        
        return (self.id > other.id)
    
    def __ge__(self ,other):
        """Returns whether this entity's respective type matches with the other's and it's id is greater or equal to
        the other's."""
        if type(other) is type(self):
            if self.type != other.type:
                return NotImplemented
        elif isinstance(other, DiscordEntity):
            if self.type not in other.__class__.__name__:
                return NotImplemented
        else:
            return NotImplemented
        
        return (self.id >= other.id)
    
    def __eq__(self, other):
        """Returns whether this entity's respective type matches with the other's and it's id equals to the other's."""
        if type(other) is type(self):
            if self.type != other.type:
                return NotImplemented
        elif isinstance(other, DiscordEntity):
            if self.type not in other.__class__.__name__:
                return NotImplemented
        else:
            return NotImplemented
        
        return (self.id == other.id)
    
    def __ne__(self,other):
        """Returns whether this entity's respective type matches with the other's and it's id not equals to the
        other's."""
        if type(other) is type(self):
            if self.type != other.type:
                return NotImplemented
        elif isinstance(other, DiscordEntity):
            if self.type not in other.__class__.__name__:
                return NotImplemented
        else:
            return NotImplemented
        
        return (self.id != other.id)
    
    def __le__(self,other):
        """Returns whether this entity's respective type matches with the other's and it's id is less or equal to
        the other's."""
        if type(other) is type(self):
            if self.type != other.type:
                return NotImplemented
        elif isinstance(other, DiscordEntity):
            if self.type not in other.__class__.__name__:
                return NotImplemented
        else:
            return NotImplemented
        
        return (self.id <= other.id)
    
    def __lt__(self,other):
        """Returns whether this entity's respective type matches with the other's and it's id is less than the
        other's."""
        if type(other) is type(self):
            if self.type != other.type:
                return NotImplemented
        elif isinstance(other, DiscordEntity):
            if self.type not in other.__class__.__name__:
                return NotImplemented
        else:
            return NotImplemented
        
        return (self.id < other.id)

class FriendRequestFlag(object):
    """
    Represents the friend request flags of a user.
    
    Attributes
    ----------
    name : `str`
        The name of the friend request flag.
    value : `int`
        Internal identificator value of the friend request flag used for lookup.
    
    Class Attributes
    ----------------
    INSTANCES : `list` of `FriendRequestFlag`
        A container to store the predefined friend request flags. This container is accessed by ``.decode`` what
        translates the friend request flags' value to their wrapper side representation.
    
    Every predefined friend request flag can also be accessed as class attribute:
    
    +---------------------------+---------------------------+-------+
    | Class attribute name      | name                      | value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | mutual_guilds             | mutual_guilds             | 1     |
    +---------------------------+---------------------------+-------+
    | mutual_friends            | mutual_friends            | 2     |
    +---------------------------+---------------------------+-------+
    | mutual_guilds_and_friends | mutual_guilds_and_friends | 3     |
    +---------------------------+---------------------------+-------+
    | all                       | all                       | 4     |
    +---------------------------+---------------------------+-------+
    """
    # class related
    INSTANCES = [NotImplemented] * 5
    
    @classmethod
    def decode(cls, data):
        """
        Converts the friend request flag data sent by Discord to it's wrapper side representation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `bool`)
            Received friend request flag data.
        
        Returns
        -------
        friend_request_flag : ``FriendRequestFlag``
        """
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
    __slots__ = ('name', 'value',)
    
    def __init__(self, value, name):
        """
        Creates a new friend request flag instance and stores it at the classe's `.INSTANCES` class attribute.
        
        Parameters
        ----------
        value : `int`
            Internal identificator value of the friend request flag used for lookup.
        name : `str`
            The name of the friend request flag.
        """
        self.value=value
        self.name=name

        self.INSTANCES[value]=self
    
    def __str__(self):
        """Returns the name of the friend request flag."""
        return self.name
    
    def __int__(self):
        """Returns the value of the friend request flag."""
        return self.value
    
    def __repr__(self):
        """Returns the representation of the friend request flag."""
        return f'{self.__class__.__name__}(value={self.value!r}, name={self.name!r})'
    
    def encode(self):
        """
        Returns the friend request flag's Discord side representation.
        
        Returns
        -------
        result : `dict` of (`str`, `bool`) items
        """
        value = self.value
        result = {}
        if (value>>2)&1:
            result['all'] = True
        else:
            if (value>>1)&1:
                result['mutual_friends'] = True
            if value&1:
                result['mutual_guilds'] = True
        
        return result
    
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
    """
    Represents a user's theme.
    
    Attributes
    ----------
    value : `str`
        The discord side identificator value of the theme.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``Theme``) items
        Stores the predefined themes in `value` - `theme` relation. This container is accessed when converting a theme
        to it's representation.
    
    Each predefined theme instance can also be accessed as class attribute:
    
    +-----------------------+-----------+
    | Class attribute name  | value     |
    +=======================+===========+
    | dark                  | dark      |
    +-----------------------+-----------+
    | light                 | light     |
    +-----------------------+-----------+
    """
    INSTANCES = {}
    
    __slots__=('value',)
    values={}
    def __init__(self, value):
        """
        Creates a new theme with the given value and stores it at the classe's `.INSTANCES` class attribute.
        
        Parameters
        ----------
        value : `str`
            The discord side identificator value of the theme.
        """
        self.value=value
        self.INSTANCES[value]=self

    def __str__(self):
        """Returns the theme's value."""
        return self.value

    def __repr__(self):
        """Returns the theme's representation."""
        return f'<{self.__class__.__name__} value={self.value!r}>'
    
    name = property(__str__)
    if (__str__.__doc__ is not None):
        name.__doc__ = (
        """
        Returns the theme's value.
        
        This property is mainly for compatibility purposes.
        
        Returns
        -------
        value : `str`
        """)
    
    dark    = NotImplemented
    light   = NotImplemented

Theme.dark  = Theme('dark')
Theme.light = Theme('light')

class Gift(object):
    """
    Represents a Discord gift.
    
    Attributes
    ----------
    code : `str`
        The code of the gift.
    uses : `int`
        The amount how much time the gift can be used.
    """
    __slots__ = ('code', 'uses', )
    def __init__(self, data):
        """
        Creates a new ``Gift`` object from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Gift data received from Discord.
        """
        self.uses=data['uses']
        self.code=data['code']

@modulize
class Discord_hdrs:
    #to receive
    AUDIT_LOG_REASON = titledstr('X-Audit-Log-Reason')
    RATELIMIT_REMAINING = titledstr('X-Ratelimit-Remaining')
    RATELIMIT_RESET = titledstr('X-Ratelimit-Reset')
    RATELIMIT_RESET_AFTER = titledstr('X-Ratelimit-Reset-After')
    RATELIMIT_LIMIT = titledstr('X-Ratelimit-Limit')
    #to send
    RATELIMIT_PRECISION = titledstr('X-RateLimit-Precision')

def urlcutter(url):
    """
    Cuts down the given url to a more suitable length.
    
    Parameters
    ----------
    url : `str`
    
    Returns
    -------
    result : `str`
    """
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

bases.id_to_time =id_to_time

del re
del titledstr
del modulize
del bases

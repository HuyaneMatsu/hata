# -*- coding: utf-8 -*-
__all__ = ('ApplicationCommandOptionType', 'ApplicationCommandPermissionOverwriteType', 'AuditLogEvent', 'ContentFilterLevel',
    'DefaultAvatar', 'FriendRequestFlag', 'GuildFeature', 'HypesquadHouse', 'InteractionType', 'InviteTargetType',
    'MFA', 'VerificationScreenStepType', 'MessageActivityType', 'MessageNotificationLevel', 'MessageType',
    'PremiumType', 'RelationshipType', 'RoleManagerType', 'Status', 'StickerType', 'TeamMembershipState', 'Theme',
    'VerificationLevel', 'VideoQualityMode', 'VoiceRegion', 'WebhookType', )

from ..backend.utils import DOCS_ENABLED, any_to_any

from .bases import PreinstancedBase
from .color import Color
from .http import URLS
from .utils import sanitize_mentions

from . import utils as module_utils

ActivityTypes = NotImplemented

class VerificationLevel(PreinstancedBase):
    """
    Represents Discord's verification level.
    
    Attributes
    ----------
    name : `str`
        The default name of the verification level.
    value : `int`
        The discord side identifier value of the verification level.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``VerificationLevel``) items
        Stores the predefined ``VerificationLevel`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The verification levels' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the verification levels.
    
    Every predefined verification level can be accessed as class attribute as well:
    
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
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none    = NotImplemented
    low     = NotImplemented
    medium  = NotImplemented
    high    = NotImplemented
    extreme = NotImplemented

VerificationLevel.none     = VerificationLevel(0, 'none')
VerificationLevel.low      = VerificationLevel(1, 'low')
VerificationLevel.medium   = VerificationLevel(2, 'medium')
VerificationLevel.high     = VerificationLevel(3, 'high')
VerificationLevel.extreme  = VerificationLevel(4, 'extreme')


class VoiceRegion(PreinstancedBase):
    """
    Represents Discord's voice regions.
    
    Attributes
    ----------
    custom : `bool`
        Whether the voice region is custom (used for events, etc.).
    deprecated : `bool`
        Whether the voice region is deprecated.
    value : `str`
        The unique identifier of the voice region.
    name : `str`
        The default name of the voice region.
    vip : `bool`
        Whether the voice region can be used only by guilds with `VIP_REGIONS` feature.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``VoiceRegion``) items
        Stores the created ``VoiceRegion`` instances.
    VALUE_TYPE : `type` = `str`
        The voice regions' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the voice regions.
    
    Each predefined voice region is also stored as a class attribute:
    
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | Class attribute name  | value         | name              | deprecated    | vip       | custom    |
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
    | africa_south          | southafrica   | South Africa      | False         | False     | False     |
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
    INSTANCES = {}
    VALUE_TYPE = str
    
    __slots__ = ('custom', 'deprecated', 'vip',)
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a voice region from the given id and stores it at class's `.INSTANCES`.
        
        Called by `.get` when no voice region was found with the given id.
        
        Parameters
        ----------
        id_ : `str`
            The identifier of the voice region.
        
        Returns
        -------
        voice_region : ``VoiceRegion``
        """
        name_parts = value.split('-')
        for index in range(len(name_parts)):
            name_part = name_parts[index]
            if len(name_part) < 4:
                name_part = name_part.upper()
            else:
                name_part = name_part.capitalize()
            name_parts[index] = name_part
        
        name = ' '.join(name_parts)
        
        self = object.__new__(cls)
        self.name = name
        self.value = value
        self.deprecated = False
        self.vip = value.startswith('vip-')
        self.custom = True
        self.INSTANCES[value] = self
        return self
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a voice region from the given data and stores it at the class's `.INSTANCES`.
        
        If the voice region already exists returns that instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received voice region data.

        Returns
        -------
        self : ``VoiceRegion``
        """
        value = data['id']
        try:
            return cls.INSTANCES[value]
        except KeyError:
            pass
        
        self = object.__new__(cls)
        self.name = data['name']
        self.value = value
        self.deprecated = data['deprecated']
        self.vip = data['vip']
        self.custom = data['custom']
        self.INSTANCES[value] = self
        
        return self
    
    def __init__(self, name, value, deprecated, vip):
        """
        Creates a new voice region with the given parameters and stores it at the class's `.INSTANCES`.
        
        Parameters
        ----------
        deprecated : `bool`
            Whether the voice region is deprecated.
        value : `str`
            The unique identifier of the voice region.
        name : `str`
            The default name of the voice region.
        vip : `bool`
            Whether the voice region can be used only by guilds with `VIP_REGIONS` feature.
        """
        self.name = name
        self.value = value
        self.deprecated = deprecated
        self.vip = vip
        self.custom = False
        self.INSTANCES[value] = self
    
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
    africa_south    = NotImplemented
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
VoiceRegion.africa_south    = VoiceRegion('South Africa',   'southafrica',  False,  False)
VoiceRegion.sydney          = VoiceRegion('Sydney',         'sydney',       False,  False)
VoiceRegion.us_central      = VoiceRegion('US Central',     'us-central',   False,  False)
VoiceRegion.us_east         = VoiceRegion('US East',        'us-east',      False,  False)
VoiceRegion.us_south        = VoiceRegion('US South',       'us-south',     False,  False)
VoiceRegion.us_west         = VoiceRegion('US West',        'us-west',      False,  False)
# deprecated
VoiceRegion.amsterdam       = VoiceRegion('Amsterdam',      'amsterdam',    True,   False)
VoiceRegion.frankfurt       = VoiceRegion('Frankfurt',      'frankfurt',    True,   False)
VoiceRegion.london          = VoiceRegion('London',         'london',       True,   False)
# vip
VoiceRegion.vip_us_east     = VoiceRegion('VIP US West',    'vip-us-west',  False,  True)
VoiceRegion.vip_us_west     = VoiceRegion('VIP US East',    'vip-us-east',  False,  True)
# vip + deprecated
VoiceRegion.vip_amsterdam   = VoiceRegion('VIP Amsterdam',  'vip-amsterdam',True,   True)


class ContentFilterLevel(PreinstancedBase):
    """
    Represents Discord's content filter level.
    
    Attributes
    ----------
    value : `int`
        The Discord side identifier value of the content filter level.
    name : `str`
        The default name of the content filter level.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ContentFilterLevel``) items
        Stores the predefined content filter levels. This container is accessed when translating a Discord side
        identifier of a content filter level. The identifier value is used as a key to get it's wrapper side
        representation.
    VALUE_TYPE : `type` = `int`
        The verification filer levels' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the content filter levels.
    
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
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    disabled = NotImplemented
    no_role  = NotImplemented
    everyone = NotImplemented

ContentFilterLevel.disabled = ContentFilterLevel(0, 'disabled')
ContentFilterLevel.no_role  = ContentFilterLevel(1, 'no_role')
ContentFilterLevel.everyone = ContentFilterLevel(2, 'everyone')


class HypesquadHouse(PreinstancedBase):
    """
    Represents Discord's hypesquad house.
    
    Attributes
    ----------
    value : `int`
        The Discord side identifier value of the hypesquad house.
    name : `str`
        The default name of the hypesquad house.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``HypesquadHouse``) items
        Stores the predefined hypesquad houses. This container is accessed when converting Discord side hypesquad
        house's value to it's wrapper side representation.
    VALUE_TYPE : `type` = `int`
        The hypesquad houses' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the hypesquad houses.
    
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
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()

    # predefined
    none        = NotImplemented
    bravery     = NotImplemented
    brilliance  = NotImplemented
    balance     = NotImplemented

HypesquadHouse.none        = HypesquadHouse(0, 'none')
HypesquadHouse.bravery     = HypesquadHouse(1, 'bravery')
HypesquadHouse.brilliance  = HypesquadHouse(2, 'brilliance')
HypesquadHouse.balance     = HypesquadHouse(3, 'balance')


class Status(PreinstancedBase):
    """
    Represents a Discord user's status.
    
    Attributes
    ----------
    position : `int`
        Internal position of the status for sorting purposes.
    value : `str`
        The identifier value of the status.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``Status``) items
        A container what stores the predefined statuses in `value` - `status` relation. This container is accessed
        when translating status value to ``Status`` object.
    VALUE_TYPE : `type` = `str`
        The statuses' values' type.
    DEFAULT_NAME : `str` = `''`
        The default name of the statuses. Statuses sue their value as names, so this field is not used.
    DEFAULT_POSITION : `int` = `5`
        The default position of the statuses'.
    
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
    INSTANCES = {}
    VALUE_TYPE = str
    DEFAULT_NAME = ''
    DEFAULT_POSITION = 4
    
    __slots__ = ('position', )
    
    def __init__(self, value, position):
        """
        Creates a new status and stores it at the class's `.INSTANCES` class attribute.
        
        Parameters
        ----------
        value : `str`
            The identifier value of the status.
        position : `int`
            Internal position of the status for sorting purposes.
        """
        self.value = value
        self.name = value
        self.position = position
        self.INSTANCES[value] = self
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new status object from the given value.
        
        Parameters
        ----------
        value : ``.VALUE_TYPE``
            The value what has no representation yet.
        
        Returns
        -------
        self : ``Status`` instance
            The created status.
        """
        self = object.__new__(cls)
        self.value = value
        self.name = value
        self.position = cls.DEFAULT_POSITION
        self.INSTANCES[value] = self
        return self
    
    def __repr__(self):
        """Returns the representation of the status."""
        return f'<{self.__class__.__name__} value={self.value!r}>'
    
    def __gt__(self, other):
        """Returns whether this status's position is greater than the other's."""
        other_type = other.__class__
        self_type = self.__class__
        if other_type is other_type:
            pass
        elif issubclass(other_type, self_type.VALUE_TYPE):
            try:
                other = self_type.INSTANCES[other]
            except KeyError:
                return NotImplemented
        else:
            return NotImplemented
        
        if self.position > other.position:
            return True
        else:
            return False
    
    def __ge__(self,other):
        """Returns whether this status's position is greater than the other's or whether the two status is equal."""
        other_type = other.__class__
        self_type = self.__class__
        if other_type is other_type:
            pass
        elif issubclass(other_type, self_type.VALUE_TYPE):
            try:
                other = self_type.INSTANCES[other]
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
    
    def __eq__(self, other):
        """Returns whether the two status is equal."""
        other_type = other.__class__
        self_type = self.__class__
        if other_type is other_type:
            pass
        elif issubclass(other_type, self_type.VALUE_TYPE):
            try:
                other = self_type.INSTANCES[other]
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
        other_type = other.__class__
        self_type = self.__class__
        if other_type is other_type:
            pass
        elif issubclass(other_type, self_type.VALUE_TYPE):
            try:
                other = self_type.INSTANCES[other]
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
        """Returns whether this status's position is less than the other's or whether the two status is equal."""
        other_type = other.__class__
        self_type = self.__class__
        if other_type is other_type:
            pass
        elif issubclass(other_type, self_type.VALUE_TYPE):
            try:
                other = self_type.INSTANCES[other]
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
        """Returns whether this status's position is less than the other's."""
        other_type = other.__class__
        self_type = self.__class__
        if other_type is other_type:
            pass
        elif issubclass(other_type, self_type.VALUE_TYPE):
            try:
                other = self_type.INSTANCES[other]
            except KeyError:
                return NotImplemented
        else:
            return NotImplemented
        
        if self.position < other.position:
            return True
        
        return False
    
    # predefined
    online     = NotImplemented
    idle       = NotImplemented
    dnd        = NotImplemented
    offline    = NotImplemented
    invisible  = NotImplemented

Status.online    = Status('online',    0)
Status.idle      = Status('idle',      1)
Status.dnd       = Status('dnd',       2)
Status.offline   = Status('offline',   3)
Status.invisible = Status('invisible', 3)

class MessageNotificationLevel(PreinstancedBase):
    """
    Represents the default message notification level of a ``Guild``.
    
    Attributes
    ----------
    value : `int`
        The Discord side identifier value of the message notification level.
    name : `str`
        The default name of the message notification level.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``MessageNotificationLevel``) items
        Stores the predefined message notification levels. This container is accessed when translating message
        notification level's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The notification levels' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the notification levels.
    
    Each predefined message notification level can also be accessed as a class attribute:
    
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
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    all_messages  = NotImplemented
    only_mentions = NotImplemented
    no_messages   = NotImplemented
    null          = NotImplemented

MessageNotificationLevel.all_messages  = MessageNotificationLevel(0, 'all_messages')
MessageNotificationLevel.only_mentions = MessageNotificationLevel(1, 'only_mentions')
MessageNotificationLevel.no_messages   = MessageNotificationLevel(2, 'no_messages')
MessageNotificationLevel.null          = MessageNotificationLevel(3, 'null')


class MFA(PreinstancedBase):
    """
    Represents Discord's Multi-Factor Authentication's levels.
    
    Attributes
    ----------
    name : `str`
        The default name of the MFA level.
    value : `int`
        The Discord side identifier value of the MFA level.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``MFA``) items
        Stores the predefined MFA level. This container is accessed when converting an MFA level's value to
        it's wrapper side representation.
    VALUE_TYPE : `type` = `int`
        The mfa levels' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the mfa levels.
    
    Each predefined MFA can also be accessed as class attribute:
    
    +-----------------------+-----------+-------+
    | Class attribute name  | name      | value |
    +=======================+===========+=======+
    | none                  | none      | 0     |
    +-----------------------+-----------+-------+
    | elevated              | elevated  | 1     |
    +-----------------------+-----------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # Predefined
    none     = NotImplemented
    elevated = NotImplemented

MFA.none     = MFA(0, 'none')
MFA.elevated = MFA(1, 'elevated')


class PremiumType(PreinstancedBase):
    """
    Represents Discord's premium types.
    
    Attributes
    ----------
    name : `str`
        The default name of the premium type.
    value : `int`
        The Discord side identifier value of the premium type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``PremiumType``) items
        A container what stores the predefined premium types and also is accessed when translating their identifier
        value to their representation.
    VALUE_TYPE : `type` = `int`
        The premium types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the premium types.
    
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
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none          = NotImplemented
    nitro_classic = NotImplemented
    nitro         = NotImplemented

PremiumType.none          = PremiumType(0, 'none')
PremiumType.nitro_classic = PremiumType(1, 'nitro_classic')
PremiumType.nitro         = PremiumType(2, 'nitro')


class RelationshipType(PreinstancedBase):
    """
    Represents a ``Relationship``'s type.
    
    Attributes
    ----------
    name : `str`
        The relationship type's name.
    value : `int`
        The Discord side identifier value of the relationship type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``RelationshipType``) items
        The predefined relation types stored in a list, so they can be accessed with their respective value as key.
        This behaviour is used to translate their Discord side value to their representation.
    VALUE_TYPE : `type` = `int`
        The relationship types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the relation types.
    
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
    | pending_incoming      | pending_incoming  | 3     |
    +-----------------------+-------------------+-------+
    | pending_outgoing      | pending_outgoing  | 4     |
    +-----------------------+-------------------+-------+
    | implicit              | implicit          | 5     |
    +-----------------------+-------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    stranger          = NotImplemented
    friend            = NotImplemented
    blocked           = NotImplemented
    pending_incoming  = NotImplemented
    pending_outgoing  = NotImplemented
    implicit          = NotImplemented

RelationshipType.stranger          = RelationshipType(0, 'stranger')
RelationshipType.friend            = RelationshipType(1, 'friend')
RelationshipType.blocked           = RelationshipType(2, 'blocked')
RelationshipType.pending_incoming  = RelationshipType(3, 'pending_incoming')
RelationshipType.pending_outgoing  = RelationshipType(4, 'pending_outgoing')
RelationshipType.implicit          = RelationshipType(5, 'implicit')

class FriendRequestFlag(PreinstancedBase):
    """
    Represents the friend request flags of a user.
    
    Attributes
    ----------
    name : `str`
        The default name of the friend request flag.
    value : `int`
        Internal identifier value of the friend request flag used for lookup.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``FriendRequestFlag``) items
        A container to store the predefined friend request flags. This container is accessed by ``.get`` what
        translates the friend request flags' value to their wrapper side representation.
    VALUE_TYPE : `type` = `int`
        The friend request flags' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the friend request flags.
    
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
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    @classmethod
    def get(cls, data):
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
        
        all_ = data.get('all', False)
        if all_:
            key = 4
        else:
            mutual_guilds = data.get('mutual_guilds', False)
            mutual_friends = data.get('mutual_friends', False)
            
            key = mutual_guilds+(mutual_friends<<1)
        
        return cls.INSTANCES[key]
    
    def __str__(self):
        """Returns the name of the friend request flag."""
        return self.name
    
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
    none                      = NotImplemented
    mutual_guilds             = NotImplemented
    mutual_friends            = NotImplemented
    mutual_guilds_and_friends = NotImplemented
    all                       = NotImplemented

FriendRequestFlag.none                      = FriendRequestFlag(0, 'none')
FriendRequestFlag.mutual_guilds             = FriendRequestFlag(1, 'mutual_guilds')
FriendRequestFlag.mutual_friends            = FriendRequestFlag(2, 'mutual_friends')
FriendRequestFlag.mutual_guilds_and_friends = FriendRequestFlag(3, 'mutual_guilds_and_friends')
FriendRequestFlag.all                       = FriendRequestFlag(4, 'all')

class Theme(PreinstancedBase):
    """
    Represents a user's theme.
    
    Attributes
    ----------
    value : `str`
        The discord side identifier value of the theme.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``Theme``) items
        Stores the predefined themes in `value` - `theme` relation. This container is accessed when converting a theme
        to it's representation.
    VALUE_TYPE : `type` = `str`
        The themes' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the themes.
    
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
    VALUE_TYPE = str
    
    __slots__ = ()
    
    def __init__(self, value):
        """
        Creates a new ``Theme`` object with the given value.
        
        Parameters
        ----------
        value : `str`
            The identifier value of the theme.
        """
        self.value = value
        self.name = value
    
    # predefined
    dark  = NotImplemented
    light = NotImplemented

Theme.dark  = Theme('dark')
Theme.light = Theme('light')


class MessageType(PreinstancedBase):
    """
    Represents a ``Message``'s type.
    
    Attributes
    ----------
    convert : `function`
        The converter function of the message type, what tries to convert the message's content to it's Discord side
        representation.
    name : `str`
        The default name of the message type.
    value : `int`
        The Discord side identifier value of the message type.
    VALUE_TYPE : `type` = `int`
        The message types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the message types.
    DEFAULT_CONVERT : `function`
        The default ``.convert`` attribute of the message types.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``MessageType``) items
        Stores the predefined ``MessageType`` instances. These can be accessed with their `value` as key.
    
    Every predefined message type can be accessed as class attribute as well:
    
    +-------------------------------------------+---------------------------------------------------+-------+
    | Class attribute name & name               | convert                                           | value |
    +===========================================+===================================================+=======+
    | default                                   | DEFAULT_CONVERT                                   | 0     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | add_user                                  | convert_add_user                                  | 1     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | remove_user                               | convert_remove_user                               | 2     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | call                                      | convert_call                                      | 3     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | channel_name_change                       | convert_channel_name_change                       | 4     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | channel_icon_change                       | convert_channel_icon_change                       | 5     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | new_pin                                   | convert_new_pin                                   | 6     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | welcome                                   | convert_welcome                                   | 7     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | new_guild_sub                             | convert_new_guild_sub                             | 8     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | new_guild_sub_t1                          | convert_new_guild_sub_t1                          | 9     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | new_guild_sub_t2                          | convert_new_guild_sub_t2                          | 10    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | new_guild_sub_t3                          | convert_new_guild_sub_t3                          | 11    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | new_follower_channel                      | convert_new_follower_channel                      | 12    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | stream                                    | convert_stream                                    | 13    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | discovery_disqualified                    | convert_discovery_disqualified                    | 14    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | discovery_requalified                     | convert_discovery_requalified                     | 15    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | discovery_grace_period_initial_warning    | convert_discovery_grace_period_initial_warning    | 16    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | discovery_grace_period_final_warning      | convert_discovery_grace_period_final_warning      | 17    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | thread_created                            | convert_thread_created                            | 18    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | inline_reply                              | DEFAULT_CONVERT                                   | 19    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | application_command                       | DEFAULT_CONVERT                                   | 20    |
    +-------------------------------------------+---------------------------------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    def DEFAULT_CONVERT(self):
        """
        Default message content converter.
        
        Parameters
        ----------
        self : ``Message``
            The message, what's content will be converted.
        
        Returns
        -------
        content : `str`
            The converted content if applicable. Might be empty string.
        """
        content = self.content
        if content:
            content = sanitize_mentions(content, self.guild)
        
        return content
    
    __slots__ = ('convert',)
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new message type with the given value.
        
        Parameters
        ----------
        value : `int`
            The message type's identifier value.
        
        Returns
        -------
        self : ``MessageType``
            The created instance.
        """
        self = object.__new__(cls)
        self.name = cls.DEFAULT_NAME
        self.value = value
        self.convert = cls.DEFAULT_CONVERT
        
        return self
    
    def __init__(self, value, name, convert):
        """
        Creates an ``MessageType`` and stores it at the class's `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the message type.
        name : `str`
            The default name of the message type.
        convert : `function`
            The converter function of the message type.
        """
        self.value = value
        self.name = name
        self.convert = convert
        
        self.INSTANCES[value] = self
    
    def __repr__(self):
        """Returns the representation of the message type."""
        return f'{self.__class__.__name__}(value={self.value!r}, name={self.name!r}, covert={self.convert!r})'
    
    # predefined
    default = NotImplemented
    add_user = NotImplemented
    remove_user = NotImplemented
    call = NotImplemented
    channel_name_change = NotImplemented
    channel_icon_change = NotImplemented
    new_pin = NotImplemented
    welcome = NotImplemented
    new_guild_sub = NotImplemented
    new_guild_sub_t1 = NotImplemented
    new_guild_sub_t2 = NotImplemented
    new_guild_sub_t3 = NotImplemented
    new_follower_channel = NotImplemented
    stream = NotImplemented
    discovery_disqualified = NotImplemented
    discovery_requalified = NotImplemented
    discovery_grace_period_initial_warning = NotImplemented
    discovery_grace_period_final_warning = NotImplemented
    inline_reply = NotImplemented
    application_command = NotImplemented

def convert_add_user(self):
    return f'{self.author.name} added {self.user_mentions[0].name} to the group.'

def convert_remove_user(self):
    return f'{self.author.name} removed {self.user_mentions[0].name} from the group.'

def convert_call(self):
    if any_to_any(self.channel.clients, self.call.users):
        return f'{self.author.name} started a call.'
    if self.call.ended_timestamp is None:
        return f'{self.author.name} started a call \N{EM DASH} Join the call.'
    return f'You missed a call from {self.author.name}'

def convert_channel_name_change(self):
    return f'{self.author.name} changed the channel name: {self.content}'

def convert_channel_icon_change(self):
    return f'{self.author.name} changed the channel icon.'

def convert_new_pin(self):
    return f'{self.author.name} pinned a message to this channel.'

# TODO: this system changed, just pulled out the new texts from the js client source, but the calculation is bad
def convert_welcome(self):
    # tuples with immutable elements are stored directly
    join_messages = (
        '{0} just joined the server - glhf!',
        '{0} just joined. Everyone, look busy!',
        '{0} just joined. Can I get a heal?',
        '{0} joined your party.',
        '{0} joined. You must construct additional pylons.',
        'Ermagherd. {0} is here.',
        'Welcome, {0}. Stay awhile and listen.',
        'Welcome, {0}. We were expecting you ( ͡° ͜ʖ ͡°)',
        'Welcome, {0}. We hope you brought pizza.',
        'Welcome {0}. Leave your weapons by the door.',
        'A wild {0} appeared.',
        'Swoooosh. {0} just landed.',
        'Brace yourselves. {0} just joined the server.',
        '{0} just joined... or did they?',
        '{0} just arrived. Seems OP - please nerf.',
        '{0} just slid into the server.',
        'A {0} has spawned in the server.',
        'Big {0} showed up!',
        'Where’s {0}? In the server!',
        '{0} hopped into the server. Kangaroo!!',
        '{0} just showed up. Hold my beer.',
        'Challenger approaching - {0} has appeared!',
        'It\'s a bird! It\'s a plane! Nevermind, it\'s just {0}.',
        'It\'s {0}! Praise the sun! [T]/',
        'Never gonna give {0} up. Never gonna let {0} down.',
        '{0} has joined the battle bus.',
        'Cheers, love! {0}\'s here!',
        'Hey! Listen! {0} has joined!',
        'We\'ve been expecting you {0}',
        'It\'s dangerous to go alone, take {0}!',
        '{0} has joined the server! It\'s super effective!',
        'Cheers, love! {0} is here!',
        '{0} is here, as the prophecy foretold.',
        '{0} has arrived. Party\'s over.',
        'Ready player {0}',
        '{0} is here to kick butt and chew bubblegum. And {0} is all out of gum.',
        'Hello. Is it {0} you\'re looking for?',
        '{0} has joined. Stay a while and listen!',
        'Roses are red, violets are blue, {0} joined this server with you',
            )

    return join_messages[int(self.created_at.timestamp())%len(join_messages)].format(self.author.name)

def convert_new_guild_sub(self):
    guild = self.channel.guild
    if guild is None:
        guild_name = 'None'
    else:
        guild_name = guild.name
    return f'{self.author.name} boosted {guild_name} with Nitro!'

def convert_new_guild_sub_t1(self):
    guild = self.channel.guild
    if guild is None:
        guild_name = 'None'
    else:
        guild_name = guild.name
        
    return f'{self.author.name} boosted {guild_name} with Nitro! {guild_name} has achieved level 1!'

def convert_new_guild_sub_t2(self):
    guild = self.channel.guild
    if guild is None:
        guild_name = 'None'
    else:
        guild_name = guild.name
    
    return f'{self.author.name} boosted {guild_name} with Nitro! {guild_name} has achieved level 2!'

def convert_new_guild_sub_t3(self):
    guild = self.channel.guild
    if guild is None:
        guild_name = 'None'
    else:
        guild_name = guild.name
        
    return f'{self.author.name} boosted {guild_name} with Nitro! {guild_name} has achieved level 3!'

def convert_new_follower_channel(self):
    channel = self.channel
    guild = channel.guild
    if guild is None:
        guild_name = 'None'
    else:
        guild_name = guild.name
    
    user_name = self.author.name_at(guild)
    
    return (f'{user_name} has added {guild_name} #{channel.name} to this channel. Its most important updates '
        'will show up here.')

def convert_stream(self):
    user = self.author
    for activity in user.activities:
        if activity.type == ActivityTypes.stream:
            activity_name = activity.name
            break
    else:
        activity_name = 'Unknown'
    
    user_name = user.name_at(self.guild)
    
    return f'{user_name} is live! Now streaming {activity_name}'

def convert_discovery_disqualified(self):
    return ('This server has been removed from Server Discovery because it no longer passes all the requirements. '
        'Check `Server Settings` for more details.')

def convert_discovery_requalified(self):
    return 'This server is eligible for Server Discovery again and has been automatically relisted!'

def convert_discovery_grace_period_initial_warning(self):
    return ('This server has failed Discovery activity requirements for 1 week. If this server fails for 4 weeks in '
        'a row, it will be automatically removed from Discovery.')

def convert_discovery_grace_period_final_warning(self):
    return ('This server has failed Discovery activity requirements for 3 weeks in a row. If this server fails for 1 '
        'more week, it will be removed from Discovery.')

def convert_thread_created(self):
    user_name = self.author.name_at(self.guild)
    return f'{user_name} started a thread'

MessageType.default = MessageType(0, 'default', MessageType.DEFAULT_CONVERT)
MessageType.add_user = MessageType(1, 'add_user', convert_add_user)
MessageType.remove_user = MessageType(2, 'remove_user', convert_remove_user)
MessageType.call = MessageType(3, 'call', convert_call)
MessageType.channel_name_change = MessageType(4, 'channel_name_change', convert_channel_name_change)
MessageType.channel_icon_change = MessageType(5, 'channel_icon_change', convert_channel_icon_change)
MessageType.new_pin = MessageType(6, 'new_pin', convert_new_pin)
MessageType.welcome = MessageType(7, 'welcome', convert_welcome)
MessageType.new_guild_sub = MessageType(8, 'new_guild_sub', convert_new_guild_sub)
MessageType.new_guild_sub_t1 = MessageType(9, 'new_guild_sub_t1', convert_new_guild_sub_t1)
MessageType.new_guild_sub_t2 = MessageType(1, 'new_guild_sub_t2', convert_new_guild_sub_t2)
MessageType.new_guild_sub_t3 = MessageType(11, 'new_guild_sub_t3', convert_new_guild_sub_t3)
MessageType.new_follower_channel = MessageType(12, 'new_follower_channel', convert_new_follower_channel)
MessageType.stream = MessageType(13, 'stream', convert_stream)
MessageType.discovery_disqualified = MessageType(14, 'discovery_disqualified', convert_discovery_disqualified)
MessageType.discovery_requalified = MessageType(15, 'discovery_requalified', convert_discovery_requalified)
MessageType.discovery_grace_period_initial_warning = MessageType(16, 'discovery_grace_period_initial_warning',
    convert_discovery_grace_period_initial_warning)
MessageType.discovery_grace_period_final_warning = MessageType(17, 'discovery_grace_period_final_warning',
    convert_discovery_grace_period_final_warning)
MessageType.thread_created = MessageType(18, 'thread_created', convert_thread_created)
MessageType.inline_reply = MessageType(19, 'inline_reply', MessageType.DEFAULT_CONVERT)
MessageType.application_command = MessageType(20, 'application_command', MessageType.DEFAULT_CONVERT)


del convert_add_user
del convert_remove_user
del convert_call
del convert_channel_name_change
del convert_channel_icon_change
del convert_new_pin
del convert_welcome
del convert_new_guild_sub
del convert_new_guild_sub_t1
del convert_new_guild_sub_t2
del convert_new_guild_sub_t3
del convert_new_follower_channel
del convert_stream
del convert_discovery_disqualified
del convert_discovery_requalified
del convert_discovery_grace_period_initial_warning
del convert_discovery_grace_period_final_warning
del convert_thread_created


class MessageActivityType(PreinstancedBase):
    """
    Represents a ``MessageActivity``'s type.
    
    Attributes
    ----------
    name : `str`
        The default name of the message activity type.
    value : `int`
        The Discord side identifier value of the message activity type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``MessageActivityType``) items
        Stores the predefined ``MessageActivityType`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The message activity types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the verification levels.
    
    Every predefined message activity type can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | name          | value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | join                  | join          | 1     |
    +-----------------------+---------------+-------+
    | spectate              | spectate      | 2     |
    +-----------------------+---------------+-------+
    | listen                | listen        | 3     |
    +-----------------------+---------------+-------+
    | watch                 | watch         | 4     |
    +-----------------------+---------------+-------+
    | join_request          | join_request  | 5     |
    +-----------------------+---------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none         = NotImplemented
    join         = NotImplemented
    spectate     = NotImplemented
    listen       = NotImplemented
    watch        = NotImplemented
    join_request = NotImplemented

MessageActivityType.none         = MessageActivityType(0, 'none')
MessageActivityType.join         = MessageActivityType(1, 'join')
MessageActivityType.spectate     = MessageActivityType(2, 'spectate')
MessageActivityType.listen       = MessageActivityType(3, 'listen')
MessageActivityType.watch        = MessageActivityType(4, 'watch')
MessageActivityType.join_request = MessageActivityType(5, 'join_request')


class TeamMembershipState(PreinstancedBase):
    """
    Represents a ``TeamMember``'s state at a ``Team``.
    
    Attributes
    ----------
    name : `str`
        The name of state.
    value : `int`
        The Discord side identifier value of the team membership state.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``TeamMembershipState``) items
        Stores the created team membership state instances. This container is accessed when translating a Discord
        team membership state's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The team membership states' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the team membership states.
    
    Every predefined team membership state can be accessed as class attribute as well:
    +-----------------------+-----------+-------+
    | Class attribute name  | name      | value |
    +=======================+===========+=======+
    | none                  | none      | 0     |
    +-----------------------+-----------+-------+
    | invited               | invited   | 1     |
    +-----------------------+-----------+-------+
    | accepted              | accepted  | 2     |
    +-----------------------+-----------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none     = None
    invited  = None
    accepted = None

TeamMembershipState.none     = TeamMembershipState(0, 'none')
TeamMembershipState.invited  = TeamMembershipState(1, 'invited')
TeamMembershipState.accepted = TeamMembershipState(2, 'accepted')



class GuildFeature(PreinstancedBase):
    """
    Represents a ``Guild``'s feature.

    Attributes
    ----------
    value : `str`
        The Discord side identifier value of the guild feature.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``GuildFeature``) items
        Stores the predefined ``GuildFeature`` instances.
    VALUE_TYPE : `type` = `str`
        The guild features' values' type.
    DEFAULT_NAME : `str` = `''`
        The default name of the guild features. Guild features have the same value as name, so at their case it is not
        applicable.
    
    Every predefined guild feature can be accessed as class attribute as well:
    
    +-------------------------------+-----------------------------------+
    | Class attribute names         | Value                             |
    +===============================+===================================+
    | animated_icon                 | ANIMATED_ICON                     |
    +-------------------------------+-----------------------------------+
    | banner                        | BANNER                            |
    +-------------------------------+-----------------------------------+
    | commerce                      | COMMERCE                          |
    +-------------------------------+-----------------------------------+
    | community                     | COMMUNITY                         |
    +-------------------------------+-----------------------------------+
    | discoverable                  | DISCOVERABLE                      |
    +-------------------------------+-----------------------------------+
    | enabled_discoverable_before   | ENABLED_DISCOVERABLE_BEFORE       |
    +-------------------------------+-----------------------------------+
    | featurable                    | FEATURABLE                        |
    +-------------------------------+-----------------------------------+
    | member_list_disabled          | MEMBER_LIST_DISABLED              |
    +-------------------------------+-----------------------------------+
    | more_emoji                    | MORE_EMOJI                        |
    +-------------------------------+-----------------------------------+
    | news                          | NEWS                              |
    +-------------------------------+-----------------------------------+
    | partnered                     | PARTNERED                         |
    +-------------------------------+-----------------------------------+
    | public                        | PUBLIC                            |
    +-------------------------------+-----------------------------------+
    | public_disabled               | PUBLIC_DISABLED                   |
    +-------------------------------+-----------------------------------+
    | relay_enabled                 | RELAY_ENABLED                     |
    +-------------------------------+-----------------------------------+
    | invite_splash                 | INVITE_SPLASH                     |
    +-------------------------------+-----------------------------------+
    | vanity                        | VANITY_URL                        |
    +-------------------------------+-----------------------------------+
    | verified                      | VERIFIED                          |
    +-------------------------------+-----------------------------------+
    | vip                           | VIP_REGIONS                       |
    +-------------------------------+-----------------------------------+
    | welcome_screen                | WELCOME_SCREEN_ENABLED            |
    +-------------------------------+-----------------------------------+
    | verification_screen           | MEMBER_VERIFICATION_GATE_ENABLED  |
    +-------------------------------+-----------------------------------+
    | preview_enabled               | PREVIEW_ENABLED                   |
    +-------------------------------+-----------------------------------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    DEFAULT_NAME = ''
    
    __slots__ = ()
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new guild feature with the given value.
        
        Parameters
        ----------
        value : `str`
            The guild feature's identifier value.
        
        Returns
        -------
        self : ``GuildFeature``
            The created guild feature.
        """
        self = object.__new__(cls)
        self.value = value
        self.name = value
        self.INSTANCES[value] = self
        return self
    
    def __init__(self, value):
        """
        Creates a new guild feature and stores it at ``.INSTANCES``.
        
        Parameters
        ----------
        value : `str`
            The identifier value of the guild feature.
        """
        self.value = value
        self.name = value
        self.INSTANCES[value] = self
    
    def __repr__(self):
        """Returns the representation of the guild feature."""
        return f'{self.__class__.__name__}(value={self.value!r})'
    
    # predefined
    animated_icon               = NotImplemented
    banner                      = NotImplemented
    commerce                    = NotImplemented
    community                   = NotImplemented
    discoverable                = NotImplemented
    enabled_discoverable_before = NotImplemented
    featurable                  = NotImplemented
    member_list_disabled        = NotImplemented
    more_emoji                  = NotImplemented
    news                        = NotImplemented
    partnered                   = NotImplemented
    public                      = NotImplemented
    public_disabled             = NotImplemented
    relay_enabled               = NotImplemented
    invite_splash               = NotImplemented
    vanity                      = NotImplemented
    verified                    = NotImplemented
    vip                         = NotImplemented
    welcome_screen              = NotImplemented
    verification_screen         = NotImplemented
    preview_enabled              = NotImplemented

GuildFeature.animated_icon              = GuildFeature('ANIMATED_ICON')
GuildFeature.banner                     = GuildFeature('BANNER')
GuildFeature.commerce                   = GuildFeature('COMMERCE')
GuildFeature.community                  = GuildFeature('COMMUNITY')
GuildFeature.discoverable               = GuildFeature('DISCOVERABLE')
GuildFeature.enabled_discoverable_before= GuildFeature('ENABLED_DISCOVERABLE_BEFORE')
GuildFeature.featurable                 = GuildFeature('FEATURABLE')
GuildFeature.member_list_disabled       = GuildFeature('MEMBER_LIST_DISABLED')
GuildFeature.more_emoji                 = GuildFeature('MORE_EMOJI')
GuildFeature.news                       = GuildFeature('NEWS')
GuildFeature.partnered                  = GuildFeature('PARTNERED')
GuildFeature.public                     = GuildFeature('PUBLIC')
GuildFeature.public_disabled            = GuildFeature('PUBLIC_DISABLED')
GuildFeature.relay_enabled              = GuildFeature('RELAY_ENABLED')
GuildFeature.invite_splash              = GuildFeature('INVITE_SPLASH')
GuildFeature.vanity                     = GuildFeature('VANITY_URL')
GuildFeature.verified                   = GuildFeature('VERIFIED')
GuildFeature.vip                        = GuildFeature('VIP_REGIONS')
GuildFeature.welcome_screen             = GuildFeature('WELCOME_SCREEN_ENABLED')
GuildFeature.verification_screen        = GuildFeature('MEMBER_VERIFICATION_GATE_ENABLED')
GuildFeature.preview_enabled            = GuildFeature('PREVIEW_ENABLED')

class AuditLogEvent(PreinstancedBase):
    """
    Represents the event type of an ``AuditLogEntry``.
    
    Attributes
    ----------
    name : `str`
        The name of audit log event.
    value : `int`
        The Discord side identifier value of the audit log event.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``AuditLogEvent``) items
        Stores the predefined ``AuditLogEvent`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The audit log events' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the audit log events
    
    Every predefined audit log event can be accessed as class attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Class attribute name      | name                      | value |
    +===========================+===========================+=======+
    | guild_update              | guild_update              |  1    |
    +---------------------------+---------------------------+-------+
    | channel_create            | channel_create            | 10    |
    +---------------------------+---------------------------+-------+
    | channel_update            | channel_update            | 11    |
    +---------------------------+---------------------------+-------+
    | channel_delete            | channel_delete            | 12    |
    +---------------------------+---------------------------+-------+
    | channel_overwrite_create  | channel_overwrite_create  | 13    |
    +---------------------------+---------------------------+-------+
    | channel_overwrite_update  | channel_overwrite_update  | 14    |
    +---------------------------+---------------------------+-------+
    | channel_overwrite_delete  | channel_overwrite_delete  | 15    |
    +---------------------------+---------------------------+-------+
    | member_kick               | member_kick               | 20    |
    +---------------------------+---------------------------+-------+
    | member_prune              | member_prune              | 21    |
    +---------------------------+---------------------------+-------+
    | member_ban_add            | member_ban_add            | 22    |
    +---------------------------+---------------------------+-------+
    | member_ban_remove         | member_ban_remove         | 23    |
    +---------------------------+---------------------------+-------+
    | member_update             | member_update             | 24    |
    +---------------------------+---------------------------+-------+
    | member_role_update        | member_role_update        | 25    |
    +---------------------------+---------------------------+-------+
    | member_move               | member_move               | 26    |
    +---------------------------+---------------------------+-------+
    | member_disconnect         | member_disconnect         | 27    |
    +---------------------------+---------------------------+-------+
    | bot_add                   | bot_add                   | 28    |
    +---------------------------+---------------------------+-------+
    | role_create               | role_create               | 30    |
    +---------------------------+---------------------------+-------+
    | role_update               | role_update               | 31    |
    +---------------------------+---------------------------+-------+
    | role_delete               | role_delete               | 32    |
    +---------------------------+---------------------------+-------+
    | invite_create             | invite_create             | 40    |
    +---------------------------+---------------------------+-------+
    | invite_update             | invite_update             | 41    |
    +---------------------------+---------------------------+-------+
    | INVITE_delete             | INVITE_delete             | 42    |
    +---------------------------+---------------------------+-------+
    | webhook_create            | webhook_create            | 50    |
    +---------------------------+---------------------------+-------+
    | webhook_update            | webhook_update            | 51    |
    +---------------------------+---------------------------+-------+
    | webhook_delete            | webhook_delete            | 52    |
    +---------------------------+---------------------------+-------+
    | emoji_create              | emoji_create              | 60    |
    +---------------------------+---------------------------+-------+
    | emoji_update              | emoji_update              | 61    |
    +---------------------------+---------------------------+-------+
    | emoji_delete              | emoji_delete              | 62    |
    +---------------------------+---------------------------+-------+
    | message_delete            | message_delete            | 72    |
    +---------------------------+---------------------------+-------+
    | message_bulk_delete       | message_bulk_delete       | 73    |
    +---------------------------+---------------------------+-------+
    | message_pin               | message_pin               | 74    |
    +---------------------------+---------------------------+-------+
    | message_unpin             | message_unpin             | 75    |
    +---------------------------+---------------------------+-------+
    | integration_create        | integration_create        | 80    |
    +---------------------------+---------------------------+-------+
    | integration_update        | integration_update        | 81    |
    +---------------------------+---------------------------+-------+
    | integration_delete        | integration_delete        | 82    |
    +---------------------------+---------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    # predefined
    guild_update             = NotImplemented
    
    channel_create           = NotImplemented
    channel_update           = NotImplemented
    channel_delete           = NotImplemented
    channel_overwrite_create = NotImplemented
    channel_overwrite_update = NotImplemented
    channel_overwrite_delete = NotImplemented
    
    member_kick              = NotImplemented
    member_prune             = NotImplemented
    member_ban_add           = NotImplemented
    member_ban_remove        = NotImplemented
    member_update            = NotImplemented
    member_role_update       = NotImplemented
    member_move              = NotImplemented
    member_disconnect        = NotImplemented
    bot_add                  = NotImplemented
    
    role_create              = NotImplemented
    role_update              = NotImplemented
    role_delete              = NotImplemented
    
    invite_create            = NotImplemented
    invite_update            = NotImplemented
    INVITE_delete            = NotImplemented
    
    webhook_create           = NotImplemented
    webhook_update           = NotImplemented
    webhook_delete           = NotImplemented
    
    emoji_create             = NotImplemented
    emoji_update             = NotImplemented
    emoji_delete             = NotImplemented
    
    message_delete           = NotImplemented
    message_bulk_delete      = NotImplemented
    message_pin              = NotImplemented
    message_unpin            = NotImplemented
    
    integration_create       = NotImplemented
    integration_update       = NotImplemented
    integration_delete       = NotImplemented

AuditLogEvent.guild_update             = AuditLogEvent( 1, 'guild_update')

AuditLogEvent.channel_create           = AuditLogEvent(10, 'channel_create')
AuditLogEvent.channel_update           = AuditLogEvent(11, 'channel_update')
AuditLogEvent.channel_delete           = AuditLogEvent(12, 'channel_delete')
AuditLogEvent.channel_overwrite_create = AuditLogEvent(13, 'channel_overwrite_create')
AuditLogEvent.channel_overwrite_update = AuditLogEvent(14, 'channel_overwrite_update')
AuditLogEvent.channel_overwrite_delete = AuditLogEvent(15, 'channel_overwrite_delete')

AuditLogEvent.member_kick              = AuditLogEvent(20, 'member_kick')
AuditLogEvent.member_prune             = AuditLogEvent(21, 'member_prune')
AuditLogEvent.member_ban_add           = AuditLogEvent(22, 'member_ban_add')
AuditLogEvent.member_ban_remove        = AuditLogEvent(23, 'member_ban_remove')
AuditLogEvent.member_update            = AuditLogEvent(24, 'member_update')
AuditLogEvent.member_role_update       = AuditLogEvent(25, 'member_role_update')
AuditLogEvent.member_move              = AuditLogEvent(26, 'member_move')
AuditLogEvent.member_disconnect        = AuditLogEvent(27, 'member_disconnect')
AuditLogEvent.bot_add                  = AuditLogEvent(28, 'member_role_update')

AuditLogEvent.role_create              = AuditLogEvent(30, 'role_create')
AuditLogEvent.role_update              = AuditLogEvent(31, 'role_update')
AuditLogEvent.role_delete              = AuditLogEvent(32, 'role_delete')

AuditLogEvent.invite_create            = AuditLogEvent(40, 'invite_create')
AuditLogEvent.invite_update            = AuditLogEvent(41, 'invite_update')
AuditLogEvent.INVITE_delete            = AuditLogEvent(42, 'INVITE_delete')

AuditLogEvent.webhook_create           = AuditLogEvent(50, 'webhook_create')
AuditLogEvent.webhook_update           = AuditLogEvent(51, 'webhook_update')
AuditLogEvent.webhook_delete           = AuditLogEvent(52, 'webhook_delete')

AuditLogEvent.emoji_create             = AuditLogEvent(60, 'emoji_create')
AuditLogEvent.emoji_update             = AuditLogEvent(61, 'emoji_update')
AuditLogEvent.emoji_delete             = AuditLogEvent(62, 'emoji_delete')

AuditLogEvent.message_delete           = AuditLogEvent(72, 'message_delete')
AuditLogEvent.message_bulk_delete      = AuditLogEvent(73, 'message_bulk_delete')
AuditLogEvent.message_pin              = AuditLogEvent(74, 'message_pin')
AuditLogEvent.message_unpin            = AuditLogEvent(75, 'message_unpin')

AuditLogEvent.integration_create       = AuditLogEvent(80, 'integration_create')
AuditLogEvent.integration_update       = AuditLogEvent(81, 'integration_update')
AuditLogEvent.integration_delete       = AuditLogEvent(82, 'integration_delete')


class DefaultAvatar(PreinstancedBase):
    """
    Represents a default avatar of a user. Default avatar is used, when the user has no avatar set.
    
    There are some predefined default avatars and there should be no more instances created.
    
    +-----------+-----------+-----------+
    | name      | value     | color     |
    +===========+===========+===========+
    | blue      | 0         | 0x7289da  |
    +-----------+-----------+-----------+
    | gray      | 1         | 0x747f8d  |
    +-----------+-----------+-----------+
    | green     | 2         | 0x43b581  |
    +-----------+-----------+-----------+
    | orange    | 3         | 0xfaa61a  |
    +-----------+-----------+-----------+
    | red       | 4         | 0xf04747  |
    +-----------+-----------+-----------+
    
    Attributes
    ----------
    color : ``Color``
        The color of the default avatar.
    name : `str`
        The name of the default avatar's color.
    value : ``int`
        The identifier value of the default avatar.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``DefaultAvatar``) objects
        The predefined default avatar instances stored for lookup.
    VALUE_TYPE : `type` = `int`
        The default avatars' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the default avatars.
    DEFAULT_COLOR : ``Color`` = `Color()`
        The default color of the default avatars.
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_COLOR = Color()
    
    __slots__ = ('color',)
    
    @classmethod
    def for_(cls, user):
        """
        Returns the default avatar for the given user.
        
        Parameters
        ----------
        user : ``UserBase`` instance
            The user, who's default avatar will be looked up.

        Returns
        -------
        default_avatar : ``DefaultAvatar``
        """
        INSTANCES = cls.INSTANCES
        return INSTANCES[user.discriminator%len(INSTANCES)]
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new default avatar with the given value.
        
        Parameters
        ----------
        value : `int`
            The identifier value of the default avatar.
        
        Returns
        -------
        self : ``DefaultAvatar``
            The created default avatar.
        """
        self = object.__new__(cls)
        self.value = value
        self.name = cls.DEFAULT_NAME
        self.color = self.DEFAULT_COLOR
        return self
    
    def __init__(self, value, name, color):
        """
        Creates a default avatar and puts it into the class's `.INSTANCES`.
        
        Parameters
        ----------
        color : ``Color``
            The color of the default avatar.
        name : `str`
            The name of the default avatar's color.
        value : ``int`
            The identifier value of the default avatar.
        """
        self.value = value
        self.name = name
        self.color = color
        self.INSTANCES[value] = self
    
    def __repr__(self):
        """Returns the default's avatar's representation."""
        return f'<{self.__class__.__name__} name={self.name}, value={self.value}, color={self.color!r}>'
    
    url = property(URLS.default_avatar_url)
    
    @property
    def colour(self):
        """Alias of ``.color_at``."""
        return self.color
    
    # predefined
    blue   = NotImplemented
    gray   = NotImplemented
    green  = NotImplemented
    orange = NotImplemented
    red    = NotImplemented

DefaultAvatar.blue   = DefaultAvatar(0 ,   'blue' , Color(0x7289da))
DefaultAvatar.gray   = DefaultAvatar(1 ,   'gray' , Color(0x747f8d))
DefaultAvatar.green  = DefaultAvatar(2 ,  'green' , Color(0x43b581))
DefaultAvatar.orange = DefaultAvatar(3 , 'orange' , Color(0xfaa61a))
DefaultAvatar.red    = DefaultAvatar(4 ,    'red' , Color(0xf04747))


class WebhookType(PreinstancedBase):
    """
    Represents a webhook's type.
    
    Attributes
    ----------
    name : `str`
        The name of the webhook type.
    value : `int`
        The discord side identifier value of the webhook type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``WebhookType``) items
        Stores the predefined ``WebhookType`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The webhook types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the webhook types.
    
    Every predefined webhook type can be accessed as class attribute as well:
    
    +-----------------------+-----------+-------+
    | Class attribute name  | name      | value |
    +=======================+===========+=======+
    | none                  | NONE      | 0     |
    +-----------------------+-----------+-------+
    | bot                   | BOT       | 1     |
    +-----------------------+-----------+-------+
    | server                | SERVER    | 2     |
    +-----------------------+-----------+-------+
    | system_dm             | SYSTEM_DM | 3     |
    +-----------------------+-----------+-------+
    | official              | OFFICIAL  | 4     |
    +-----------------------+-----------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none      = NotImplemented
    bot       = NotImplemented
    server    = NotImplemented
    system_dm = NotImplemented
    official  = NotImplemented

WebhookType.none      = WebhookType(0, 'NONE')
WebhookType.bot       = WebhookType(1, 'BOT')
WebhookType.server    = WebhookType(2, 'SERVER')
WebhookType.system_dm = WebhookType(3, 'SYSTEM_DM')
WebhookType.official  = WebhookType(4, 'OFFICIAL')


class InviteTargetType(PreinstancedBase):
    """
    Represents an ``Invite``'s target's type.
    
    Attributes
    ----------
    name : `str`
        The name of the target type.
    value : `int`
        The Discord side identifier value of the target type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``InviteTargetType``) items
        Stores the predefined ``InviteTargetType`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The invite target types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the invite target types.
    
    Every predefined invite target type can be accessed as class attribute as well:
    
    +-----------------------+-----------------------+-------+
    | Class attribute name  | name                  | value |
    +=======================+=======================+=======+
    | none                  | none                  | 0     |
    +-----------------------+-----------------------+-------+
    | stream                | stream                | 1     |
    +-----------------------+-----------------------+-------+
    | embedded_application  | embedded_application  | 2     |
    +-----------------------+-----------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none                 = NotImplemented
    stream               = NotImplemented
    embedded_application = NotImplemented

InviteTargetType.none                 = InviteTargetType(0, 'none'                , )
InviteTargetType.stream               = InviteTargetType(1, 'stream'              , )
InviteTargetType.embedded_application = InviteTargetType(2, 'embedded_application', )


class StickerType(PreinstancedBase):
    """
    Represents a message sticker's format's type.
    
    Attributes
    ----------
    name : `str`
        The name of the message sticker format type.
    value : `int`
        The Discord side identifier value of the message sticker format type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``StickerType``) items
        Stores the predefined ``StickerType`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The message sticker format types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the message sticker types.
    
    Every predefined sticker format type can be accessed as class attribute as well:
    
    +-----------------------+-----------+-------+
    | Class attribute name  | name      | value |
    +=======================+===========+=======+
    | none                  | none      | 0     |
    +-----------------------+-----------+-------+
    | png                   | png       | 1     |
    +-----------------------+-----------+-------+
    | apng                  | apng      | 2     |
    +-----------------------+-----------+-------+
    | lottie                | lottie    | 3     |
    +-----------------------+-----------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    # predefined
    none   = NotImplemented
    png    = NotImplemented
    apng   = NotImplemented
    lottie = NotImplemented

StickerType.none   = StickerType(0, 'none')
StickerType.png    = StickerType(1, 'png')
StickerType.apng   = StickerType(2, 'apng')
StickerType.lottie = StickerType(3, 'lottie')


class RoleManagerType(PreinstancedBase):
    """
    Represents a managed role's manager type.
    
    Attributes
    ----------
    name : `str`
        The name of the role manager type.
    value : `int`
        The identifier value the role manager type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``RoleManagerType``) items
        Stores the predefined ``RoleManagerType`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The role manager types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the role manager types.
    
    Every predefined role manager type can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | name          | value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | unset                 | unset         | 1     |
    +-----------------------+---------------+-------+
    | unknown               | unknown       | 2     |
    +-----------------------+---------------+-------+
    | bot                   | bot           | 3     |
    +-----------------------+---------------+-------+
    | booster               | booster       | 4     |
    +-----------------------+---------------+-------+
    | integration           | integration   | 5     |
    +-----------------------+---------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    def __bool__(self):
        """Returns whether the role manager's type is set."""
        if self.value:
            boolean = True
        else:
            boolean = False
        
        return boolean
    
    none        = NotImplemented
    unset       = NotImplemented
    unknown     = NotImplemented
    bot         = NotImplemented
    booster     = NotImplemented
    integration = NotImplemented

RoleManagerType.none        = RoleManagerType(0 , 'none'        ,)
RoleManagerType.unset       = RoleManagerType(1 , 'unset'       ,)
RoleManagerType.unknown     = RoleManagerType(2 , 'unknown'     ,)
RoleManagerType.bot         = RoleManagerType(3 , 'bot'         ,)
RoleManagerType.booster     = RoleManagerType(4 , 'booster'     ,)
RoleManagerType.integration = RoleManagerType(5 , 'integration' ,)


class ApplicationCommandOptionType(PreinstancedBase):
    """
    Represents an application command options' type.
    
    Attributes
    ----------
    name : `str`
        The name of the application command option type.
    value : `int`
        The identifier value the application command option type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationCommandOptionType``) items
        Stores the predefined ``ApplicationCommandOptionType`` instances. These can be accessed with their `value` as
        key.
    VALUE_TYPE : `type` = `int`
        The application command option types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the application command option types.
    
    Every predefined application command option type. can be accessed as class attribute as well:
    
    +-----------------------+-------------------+-------+
    | Class attribute name  | Name              | Value |
    +=======================+===================+=======+
    | none                  | none              | 0     |
    +-----------------------+-------------------+-------+
    | sub_command           | sub_command       | 1     |
    +-----------------------+-------------------+-------+
    | sub_command_group     | sub_command_group | 2     |
    +-----------------------+-------------------+-------+
    | string                | string            | 3     |
    +-----------------------+-------------------+-------+
    | integer               | integer           | 4     |
    +-----------------------+-------------------+-------+
    | boolean               | boolean           | 5     |
    +-----------------------+-------------------+-------+
    | user                  | user              | 6     |
    +-----------------------+-------------------+-------+
    | channel               | channel           | 7     |
    +-----------------------+-------------------+-------+
    | role                  | role              | 8     |
    +-----------------------+-------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none              = NotImplemented
    sub_command       = NotImplemented
    sub_command_group = NotImplemented
    string            = NotImplemented
    integer           = NotImplemented
    boolean           = NotImplemented
    user              = NotImplemented
    channel           = NotImplemented
    role              = NotImplemented

ApplicationCommandOptionType.none              = ApplicationCommandOptionType(0 , 'none'              ,)
ApplicationCommandOptionType.sub_command       = ApplicationCommandOptionType(1 , 'sub_command'       ,)
ApplicationCommandOptionType.sub_command_group = ApplicationCommandOptionType(2 , 'sub_command_group' ,)
ApplicationCommandOptionType.string            = ApplicationCommandOptionType(3 , 'string'            ,)
ApplicationCommandOptionType.integer           = ApplicationCommandOptionType(4 , 'integer'           ,)
ApplicationCommandOptionType.boolean           = ApplicationCommandOptionType(5 , 'boolean'           ,)
ApplicationCommandOptionType.user              = ApplicationCommandOptionType(6 , 'user'              ,)
ApplicationCommandOptionType.channel           = ApplicationCommandOptionType(7 , 'channel'           ,)
ApplicationCommandOptionType.role              = ApplicationCommandOptionType(8 , 'role'              ,)


class InteractionType(PreinstancedBase):
    """
    The type of an interaction.
    
    Attributes
    ----------
    name : `str`
        The name of the interaction type.
    value : `int`
        The identifier value the interaction type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``InteractionType``) items
        Stores the predefined ``InteractionType`` instances. These can be accessed with their `value` as
        key.
    VALUE_TYPE : `type` = `int`
        The application command option types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the interaction types.
    
    Every predefined interaction type. can be accessed as class attribute as well:
    
    +-----------------------+-----------------------+-------+
    | Class attribute name  | Name                  | Value |
    +=======================+=======================+=======+
    | none                  | none                  | 0     |
    +-----------------------+-----------------------+-------+
    | ping                  | ping                  | 1     |
    +-----------------------+-----------------------+-------+
    | application_command   | application_command   | 2     |
    +-----------------------+-----------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none                = NotImplemented
    ping                = NotImplemented
    application_command = NotImplemented

InteractionType.none                = InteractionType(0, 'none')
InteractionType.ping                = InteractionType(1, 'ping')
InteractionType.application_command = InteractionType(2, 'application_command')


class VerificationScreenStepType(PreinstancedBase):
    """
    Represents a type of a ``VerificationScreenStep``.

    Attributes
    ----------
    value : `str`
        The Discord side identifier value of the verification step types.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``VerificationScreenStepType``) items
        Stores the predefined ``VerificationScreenStepType`` instances.
    VALUE_TYPE : `type` = `str`
        The verification screen steps' values' type.
    DEFAULT_NAME : `str` = `''`
        The default name of the verification screen step types.Verification screen step types have the
        same value as name, so at their case it is not applicable.
    
    Every predefined verification screen step type can be accessed as class attribute as well:
    
    +-----------------------+-------+
    | Class attribute names | Value |
    +=======================+=======+
    | rules                 | TERMS |
    +-----------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    DEFAULT_NAME = ''
    
    __slots__ = ()
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new verification screen type with the given value.
        
        Parameters
        ----------
        value : `str`
            The verification screen type's identifier value.
        
        Returns
        -------
        self : ``VerificationScreenStepType``
            The verification screen type.
        """
        self = object.__new__(cls)
        self.value = value
        self.name = value
        self.INSTANCES[value] = self
        return self
    
    def __init__(self, value):
        """
        Creates a new verification screen type and stores it at ``.INSTANCES``.
        
        Parameters
        ----------
        value : `str`
            The identifier value of the verification screen types.
        """
        self.value = value
        self.name = value
        self.INSTANCES[value] = self
    
    def __repr__(self):
        """Returns the representation of the verification screen type."""
        return f'{self.__class__.__name__}(value={self.value!r})'
    
    rules = NotImplemented

VerificationScreenStepType.rules = VerificationScreenStepType('TERMS')


class ApplicationCommandPermissionOverwriteType(PreinstancedBase):
    """
    Represents an application command's permission's type.
    
    Attributes
    ----------
    name : `str`
        The name of the application command permission overwrite type.
    value : `int`
        The identifier value the application command permission overwrite type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationCommandPermissionOverwriteType``) items
        Stores the predefined ``ApplicationCommandPermissionOverwriteType`` instances. These can be accessed with their
        `value` as key.
    VALUE_TYPE : `type` = `int`
        The application command permission overwrite types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the application command permission overwrite types.
    
    Every predefined application command permission overwrite type can be accessed as class attribute as well:
    
    +-----------------------+-------+-------+
    | Class attribute name  | Name  | Value |
    +=======================+=======+=======+
    | none                  | none  | 0     |
    +-----------------------+-------+-------+
    | role                  | role  | 1     |
    +-----------------------+-------+-------+
    | user                  | user  | 2     |
    +-----------------------+-------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none    = NotImplemented
    role    = NotImplemented
    user    = NotImplemented

ApplicationCommandPermissionOverwriteType.none = ApplicationCommandPermissionOverwriteType(0 , 'none' ,)
ApplicationCommandPermissionOverwriteType.role = ApplicationCommandPermissionOverwriteType(1 , 'role' ,)
ApplicationCommandPermissionOverwriteType.user = ApplicationCommandPermissionOverwriteType(2 , 'user' ,)


class VideoQualityMode(PreinstancedBase):
    """
    Represents a voice channel's video quality mode.
    
    Attributes
    ----------
    name : `str`
        The name of the video quality mode.
    value : `int`
        The identifier value the video quality mode.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``VideoQualityMode``) items
        Stores the predefined ``VideoQualityMode`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The video quality modes' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the video quality modes.
    
    Every predefined video quality mode can be accessed as class attribute as well:
    
    +-----------------------+-------+-------+-------------------------------------------------------+
    | Class attribute name  | Name  | Value | Description                                           |
    +=======================+=======+=======+=======================================================+
    | none                  | none  | 0     | N/A                                                   |
    +-----------------------+-------+-------+-------------------------------------------------------+
    | auto                  | auto  | 1     | Discord chooses the quality for optimal performance.  |
    +-----------------------+-------+-------+-------------------------------------------------------+
    | full                  | full  | 2     | 720p                                                  |
    +-----------------------+-------+-------+-------------------------------------------------------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none    = NotImplemented
    auto    = NotImplemented
    full    = NotImplemented
    
VideoQualityMode.none = VideoQualityMode(0, 'none')
VideoQualityMode.auto = VideoQualityMode(1, 'auto')
VideoQualityMode.full = VideoQualityMode(2, 'full')


module_utils.RelationshipType = RelationshipType

del module_utils

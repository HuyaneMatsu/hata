__all__ = ('AuditLogEvent', 'ContentFilterLevel', 'DefaultAvatar', 'FriendRequestFlag', 'GuildFeature',
    'HypesquadHouse', 'InviteTargetType', 'MFA', 'MessageActivityType', 'MessageNotificationLevel', 'MessageType',
    'PremiumType', 'RelationshipType', 'RoleManagerType', 'StagePrivacyLevel', 'Status', 'StickerType',
    'TeamMembershipState', 'Theme', 'VerificationLevel', 'VerificationScreenStepType', 'VideoQualityMode',
    'VoiceRegion', 'WebhookType')

from ..backend.utils import any_to_any
from ..backend.export import export, include

from .bases import PreinstancedBase, Preinstance as P
from .color import Color
from .utils import sanitize_mentions

from . import urls as module_urls

ActivityTypes = include('ActivityTypes')

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
    none = P(0, 'none')
    low = P(1, 'low')
    medium = P(2, 'medium')
    high = P(3, 'high')
    extreme = P(4, 'extreme')


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
    brazil = P('Brazil', 'brazil', False, False)
    dubai = P('Dubai', 'dubai', False, False)
    eu_central = P('Central Europe', 'eu-central', False, False)
    eu_west = P('Western Europe', 'eu-west', False, False)
    europe = P('Europe', 'europe', False, False)
    hongkong = P('Hong Kong', 'hongkong', False, False)
    india = P('India', 'india', False, False)
    japan = P('Japan', 'japan', False, False)
    russia = P('Russia', 'russia', False, False)
    singapore = P('Singapore', 'singapore', False, False)
    africa_south = P('South Africa', 'southafrica', False, False)
    sydney = P('Sydney', 'sydney', False, False)
    us_central = P('US Central', 'us-central', False, False)
    us_east = P('US East', 'us-east', False, False)
    us_south = P('US South', 'us-south', False, False)
    us_west = P('US West', 'us-west', False, False)
    # deprecated
    amsterdam = P('Amsterdam', 'amsterdam', True, False)
    frankfurt = P('Frankfurt', 'frankfurt', True, False)
    london = P('London', 'london', True, False)
    # vip
    vip_us_east = P('VIP US West', 'vip-us-west', False, True)
    vip_us_west = P('VIP US East', 'vip-us-east', False, True)
    # vip + deprecated
    vip_amsterdam = P('VIP Amsterdam', 'vip-amsterdam',True, True)


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
    disabled = P(0, 'disabled')
    no_role = P(1, 'no_role')
    everyone = P(2, 'everyone')


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
    none = P(0, 'none')
    bravery = P(1, 'bravery')
    brilliance = P(2, 'brilliance')
    balance = P(3, 'balance')


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
    
    def __init__(self, value, name, position):
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
        self.name = name
        self.position = position
        self.INSTANCES[value] = self
    
    @classmethod
    def _from_value(cls, value,):
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
                return P
        else:
            return P
        
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
                return P
        else:
            return P
        
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
                return P
        else:
            return P
    
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
                return P
        else:
            return P
        
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
                return P
        else:
            return P
        
        self_position = self.position
        other_position = other.position
        if self_position < other_position:
            return True
        
        if self_position > other_position:
            return False
        
        if self.value == other.value:
            return True
        
        return False
    
    def __lt__(self,other):
        """Returns whether this status's position is less than the other's."""
        other_type = other.__class__
        self_type = self.__class__
        if other_type is other_type:
            pass
        elif issubclass(other_type, self_type.VALUE_TYPE):
            try:
                other = self_type.INSTANCES[other]
            except KeyError:
                return P
        else:
            return P
        
        if self.position < other.position:
            return True
        
        return False
    
    # predefined
    online = P('online', 'online', 0)
    idle = P('idle', 'idle', 1)
    dnd = P('dnd', 'dnd', 2)
    offline = P('offline', 'offline', 3)
    invisible = P('invisible', 'invisible', 3)


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
    all_messages = P(0, 'all_messages')
    only_mentions = P(1, 'only_mentions')
    no_messages = P(2, 'no_messages')
    null = P(3, 'null')


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
    none = P(0, 'none')
    elevated = P(1, 'elevated')


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
    none = P(0, 'none')
    nitro_classic = P(1, 'nitro_classic')
    nitro = P(2, 'nitro')


@export
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
    stranger = P(0, 'stranger')
    friend = P(1, 'friend')
    blocked = P(2, 'blocked')
    pending_incoming = P(3, 'pending_incoming')
    pending_outgoing = P(4, 'pending_outgoing')
    implicit = P(5, 'implicit')


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
    none = P(0, 'none')
    mutual_guilds = P(1, 'mutual_guilds')
    mutual_friends = P(2, 'mutual_friends')
    mutual_guilds_and_friends = P(3, 'mutual_guilds_and_friends')
    all = P(4, 'all')


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
    
    # predefined
    dark = P('dark', 'dark')
    light = P('light', 'light')


def MESSAGE_DEFAULT_CONVERTER(self):
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

def convert_invite_reminder(self):
    return 'Wondering who to invite?\nStart by inviting anyone who can help you build the server!'

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
    | default                                   | MESSAGE_DEFAULT_CONVERTER                         | 0     |
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
    | inline_reply                              | MESSAGE_DEFAULT_CONVERTER                         | 19    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | application_command                       | MESSAGE_DEFAULT_CONVERTER                         | 20    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | thread_started                            | MESSAGE_DEFAULT_CONVERTER                         | 21    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | invite_reminder                           | convert_invite_reminder                           | 22    |
    +-------------------------------------------+---------------------------------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
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
        self.convert = MESSAGE_DEFAULT_CONVERTER
        
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
    default = P(0, 'default', MESSAGE_DEFAULT_CONVERTER)
    add_user = P(1, 'add_user', convert_add_user)
    remove_user = P(2, 'remove_user', convert_remove_user)
    call = P(3, 'call', convert_call)
    channel_name_change = P(4, 'channel_name_change', convert_channel_name_change)
    channel_icon_change = P(5, 'channel_icon_change', convert_channel_icon_change)
    new_pin = P(6, 'new_pin', convert_new_pin)
    welcome = P(7, 'welcome', convert_welcome)
    new_guild_sub = P(8, 'new_guild_sub', convert_new_guild_sub)
    new_guild_sub_t1 = P(9, 'new_guild_sub_t1', convert_new_guild_sub_t1)
    new_guild_sub_t2 = P(10, 'new_guild_sub_t2', convert_new_guild_sub_t2)
    new_guild_sub_t3 = P(11, 'new_guild_sub_t3', convert_new_guild_sub_t3)
    new_follower_channel = P(12, 'new_follower_channel', convert_new_follower_channel)
    stream = P(13, 'stream', convert_stream)
    discovery_disqualified = P(14, 'discovery_disqualified', convert_discovery_disqualified)
    discovery_requalified = P(15, 'discovery_requalified', convert_discovery_requalified)
    discovery_grace_period_initial_warning = P(16, 'discovery_grace_period_initial_warning',
        convert_discovery_grace_period_initial_warning)
    discovery_grace_period_final_warning = P(17, 'discovery_grace_period_final_warning',
        convert_discovery_grace_period_final_warning)
    thread_created = P(18, 'thread_created', convert_thread_created)
    inline_reply = P(19, 'inline_reply', MESSAGE_DEFAULT_CONVERTER)
    application_command = P(20, 'application_command', MESSAGE_DEFAULT_CONVERTER)
    thread_started = P(21, 'thread_started', MESSAGE_DEFAULT_CONVERTER)
    invite_reminder = P(22, 'invite_reminder', convert_invite_reminder)

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
del convert_invite_reminder


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
    none = P(0, 'none')
    join = P(1, 'join')
    spectate = P(2, 'spectate')
    listen = P(3, 'listen')
    watch = P(4, 'watch')
    join_request = P(5, 'join_request')


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
    none = P(0, 'none')
    invited = P(1, 'invited')
    accepted = P(2, 'accepted')


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
    | discoverable_disabled         | DISCOVERABLE_DISABLED             |
    +-------------------------------+-----------------------------------+
    | discoverable_enabled_before   | ENABLED_DISCOVERABLE_BEFORE       |
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
    
    # predefined
    animated_icon = P('ANIMATED_ICON', 'animated_icon')
    banner = P('BANNER', 'banner')
    commerce = P('COMMERCE', 'commerce')
    community = P('COMMUNITY', 'community')
    discoverable = P('DISCOVERABLE', 'discoverable')
    discoverable_disabled = P('DISCOVERABLE_DISABLED', 'discoverable_disabled')
    discoverable_enabled_before = P('ENABLED_DISCOVERABLE_BEFORE', 'discoverable_enabled_before')
    featurable = P('FEATURABLE', 'featurable')
    member_list_disabled = P('MEMBER_LIST_DISABLED', 'member_list_disabled')
    more_emoji = P('MORE_EMOJI', 'more_emoji')
    news = P('NEWS', 'news')
    partnered = P('PARTNERED', 'partnered')
    public = P('PUBLIC', 'public')
    public_disabled = P('PUBLIC_DISABLED', 'public_disabled')
    relay_enabled = P('RELAY_ENABLED', 'relay_enabled')
    invite_splash = P('INVITE_SPLASH', 'invite_splash')
    vanity = P('VANITY_URL', 'vanity')
    verified = P('VERIFIED', 'verified')
    vip = P('VIP_REGIONS', 'vip')
    welcome_screen = P('WELCOME_SCREEN_ENABLED', 'welcome_screen')
    verification_screen = P('MEMBER_VERIFICATION_GATE_ENABLED', 'verification_screen')
    preview_enabled = P('PREVIEW_ENABLED', 'preview_enabled')


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
    guild_update = P(1, 'guild_update')
    
    channel_create = P(10, 'channel_create')
    channel_update = P(11, 'channel_update')
    channel_delete = P(12, 'channel_delete')
    channel_overwrite_create = P(13, 'channel_overwrite_create')
    channel_overwrite_update = P(14, 'channel_overwrite_update')
    channel_overwrite_delete = P(15, 'channel_overwrite_delete')
    
    member_kick = P(20, 'member_kick')
    member_prune = P(21, 'member_prune')
    member_ban_add = P(22, 'member_ban_add')
    member_ban_remove = P(23, 'member_ban_remove')
    member_update = P(24, 'member_update')
    member_role_update = P(25, 'member_role_update')
    member_move = P(26, 'member_move')
    member_disconnect = P(27, 'member_disconnect')
    bot_add = P(28, 'member_role_update')
    
    role_create = P(30, 'role_create')
    role_update = P(31, 'role_update')
    role_delete = P(32, 'role_delete')
    
    invite_create = P(40, 'invite_create')
    invite_update = P(41, 'invite_update')
    invite_delete = P(42, 'INVITE_delete')
    
    webhook_create = P(50, 'webhook_create')
    webhook_update = P(51, 'webhook_update')
    webhook_delete = P(52, 'webhook_delete')
    
    emoji_create = P(60, 'emoji_create')
    emoji_update = P(61, 'emoji_update')
    emoji_delete = P(62, 'emoji_delete')
    
    message_delete = P(72, 'message_delete')
    message_bulk_delete = P(73, 'message_bulk_delete')
    message_pin = P(74, 'message_pin')
    message_unpin = P(75, 'message_unpin')
    
    integration_create = P(80, 'integration_create')
    integration_update = P(81, 'integration_update')
    integration_delete = P(82, 'integration_delete')


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
    
    url = property(module_urls.default_avatar_url)
    
    
    # predefined
    blue = P(0, 'blue', Color(0x7289da))
    gray = P(1, 'gray', Color(0x747f8d))
    green = P(2, 'green', Color(0x43b581))
    orange = P(3, 'orange', Color(0xfaa61a))
    red = P(4, 'red', Color(0xf04747))


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
    
    +-----------------------+---------------+-------+
    | Class attribute name  | name          | value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | bot                   | bot           | 1     |
    +-----------------------+---------------+-------+
    | server                | server        | 2     |
    +-----------------------+---------------+-------+
    | application           | application   | 3     |
    +-----------------------+---------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    bot = P(1, 'bot')
    server = P(2, 'server')
    application = P(3, 'application')


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
    none = P(0, 'none', )
    stream = P(1, 'stream', )
    embedded_application = P(2, 'embedded_application', )


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
    none = P(0, 'none')
    png = P(1, 'png')
    apng = P(2, 'apng')
    lottie = P(3, 'lottie')


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
    
    none = P(0, 'none',)
    unset = P(1, 'unset',)
    unknown = P(2, 'unknown',)
    bot = P(3, 'bot',)
    booster = P(4, 'booster',)
    integration = P(5, 'integration',)


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
    
    def __repr__(self):
        """Returns the representation of the verification screen type."""
        return f'{self.__class__.__name__}(value={self.value!r})'
    
    rules = P('TERMS', 'rules')


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
    
    none = P(0, 'none')
    auto = P(1, 'auto')
    full = P(2, 'full')


class StagePrivacyLevel(PreinstancedBase):
    """
    Represents a stage channel's privacy level.
    
    Attributes
    ----------
    name : `str`
        The name of the stage privacy level.
    value : `int`
        The identifier value the stage privacy level.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``StagePrivacyLevel``) items
        Stores the predefined ``StagePrivacyLevel`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The stage privacy level' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the stage privacy levels.
    
    Every predefined stage privacy level can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | Name          | Value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | public                | public        | 1     |
    +-----------------------+---------------+-------+
    | guild_only            | guild_only    | 2     |
    +-----------------------+---------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    public = P(1, 'public')
    guild_only = P(2, 'guild_only')

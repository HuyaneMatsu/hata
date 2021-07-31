__all__ = ('DefaultAvatar', 'FriendRequestFlag', 'HypesquadHouse', 'PremiumType', 'RelationshipType', 'Status',
    'Theme', )

from ...backend.export import export

from ..bases import PreinstancedBase, Preinstance as P
from ..color import Color

from ..http import urls as module_urls


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

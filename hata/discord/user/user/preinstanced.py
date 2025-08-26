__all__ = (
    'DefaultAvatar', 'FriendRequestFlag', 'HypesquadHouse', 'PremiumType', 'RelationshipType', 'Theme'
)

from warnings import warn

from scarletio import copy_docs, export

from ...bases import Preinstance as P, PreinstancedBase
from ...color import Color
from ...http.urls import build_default_avatar_url


class DefaultAvatar(PreinstancedBase, value_type = int):
    """
    Represents a default avatar of a user. Default avatar is used, when the user has no avatar set.
    
    There are some predefined default avatars and there should be no more instances created.
    
    Attributes
    ----------
    color : ``Color``
        The color of the default avatar.
    
    name : `str`
        The name of the default avatar's color.
    
    value : ``int`
        The identifier value of the default avatar.
    
    Type Attributes
    ---------------
    Every predefined instance can be accessed as a type attribute.
    
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
    | pink      | 5         | 0xff00a0  |
    +-----------+-----------+-----------+
    """
    __slots__ = ('color',)
    
    
    def __new__(cls, value, name = None, color = None):
        """
        Creates a default avatar.
        
        Parameters
        ----------
        value : `int`
            The identifier value of the default avatar.
        
        name : `None | str` = `None`, Optional
            The name of the default avatar's color.
        
        color : `None | Color` = `None`, Optional
            The color of the default avatar.
        """
        if color is None:
            color = Color()
        
        self = PreinstancedBase.__new__(cls, value, name)
        self.color = color
        return self
    
    
    @classmethod
    def for_(cls, user):
        """
        Returns the default avatar for the given user.
        
        Parameters
        ----------
        user : ``UserBase``
            The user, who's default avatar will be looked up.

        Returns
        -------
        default_avatar : ``DefaultAvatar``
        """
        warn(
            'Deprecated and will be removed in 2025 December. Please use `UserBase.default_avatar` instead.',
            FutureWarning,
            stacklevel = 2,
        )
        
        INSTANCES = cls.INSTANCES
        
        discriminator = user.discriminator
        if discriminator:
            key = discriminator
        else:
            key = user.id >> 22
        
        return INSTANCES[key % len(INSTANCES)]
    
    
    @copy_docs(PreinstancedBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        repr_parts.append(', color = ')
        repr_parts.append(repr(self.color))
    
    
    @property
    def url(self):
        """
        Returns the default avatar's url.
        
        Returns
        -------
        url : `str`
        """ 
        return build_default_avatar_url(self.value)
    
    
    # predefined
    blue = P(0, 'blue', Color(0x7289da))
    gray = P(1, 'gray', Color(0x747f8d))
    green = P(2, 'green', Color(0x43b581))
    orange = P(3, 'orange', Color(0xfaa61a))
    red = P(4, 'red', Color(0xf04747))
    pink = P(5, 'pink', Color(0xff00a0))


class HypesquadHouse(PreinstancedBase, value_type = int):
    """
    Represents Discord's hypesquad house.
    
    Attributes
    ----------
    value : `int`
        The Discord side identifier value of the hypesquad house.
    
    name : `str`
        The name of the hypesquad house.
    
    Type Attributes
    ---------------
    Every predefined hypesquad house can also be accessed as type attribute:
    
    +-----------------------+---------------+-------+
    | Type attribute name   | name          | value |
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
    __slots__ = ()

    # predefined
    none = P(0, 'none')
    bravery = P(1, 'bravery')
    brilliance = P(2, 'brilliance')
    balance = P(3, 'balance')


class PremiumType(PreinstancedBase, value_type = int):
    """
    Represents Discord's premium types.
    
    Attributes
    ----------
    name : `str`
        The default name of the premium type.
    
    value : `int`
        The Discord side identifier value of the premium type.
    
    Type Attributes
    ---------------
    Each predefined premium type can also be accessed as type attribute:
    
    +-----------------------+---------------+-------+
    | Type attribute name   | name          | value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | nitro_classic         | nitro classic | 1     |
    +-----------------------+---------------+-------+
    | nitro                 | nitro         | 2     |
    +-----------------------+---------------+-------+
    | nitro_basic           | nitro basic   | 3     |
    +-----------------------+---------------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    nitro_classic = P(1, 'nitro classic')
    nitro = P(2, 'nitro')
    nitro_basic = P(3, 'nitro basic')


@export
class RelationshipType(PreinstancedBase, value_type = int):
    """
    Represents a ``Relationship``'s type.
    
    Attributes
    ----------
    name : `str`
        The relationship type's name.
    
    value : `int`
        The Discord side identifier value of the relationship type.
    
    Type Attributes
    ---------------
    Each predefined relationship type can also be accessed as type attribute:
    
    +-----------------------+-------------------+-------+
    | Type attribute name   | name              | value |
    +=======================+===================+=======+
    | stranger              | stranger          | 0     |
    +-----------------------+-------------------+-------+
    | friend                | friend            | 1     |
    +-----------------------+-------------------+-------+
    | blocked               | blocked           | 2     |
    +-----------------------+-------------------+-------+
    | pending_incoming      | pending incoming  | 3     |
    +-----------------------+-------------------+-------+
    | pending_outgoing      | pending outgoing  | 4     |
    +-----------------------+-------------------+-------+
    | implicit              | implicit          | 5     |
    +-----------------------+-------------------+-------+
    | suggestion            | suggestion        | 6     |
    +-----------------------+-------------------+-------+
    """
    __slots__ = ()
    
    # predefined
    stranger = P(0, 'stranger')
    friend = P(1, 'friend')
    blocked = P(2, 'blocked')
    pending_incoming = P(3, 'pending incoming')
    pending_outgoing = P(4, 'pending outgoing')
    implicit = P(5, 'implicit')
    suggestion = P(6, 'suggestion')


class FriendRequestFlag(PreinstancedBase, value_type = int):
    """
    Represents the friend request flags of a user.
    
    Attributes
    ----------
    name : `str`
        The default name of the friend request flag.
    
    value : `int`
        Internal identifier value of the friend request flag used for lookup.
    
    Type Attributes
    ---------------
    Every predefined friend request flag can also be accessed as type attribute:
    
    +---------------------------+---------------------------+-------+
    | Type attribute name       | name                      | value |
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
    __slots__ = ()
    
    
    @classmethod
    def decode(cls, data):
        """
        Converts the friend request flag data sent by Discord to it's wrapper side representation.
        
        Parameters
        ----------
        data : `None | dict<str, object>`
            Received friend request flag data.
        
        Returns
        -------
        friend_request_flag : `instance<type<cls>>`
        """
        if data is None:
            return cls.none
        
        all_ = data.get('all', False)
        if all_:
            key = 4
        else:
            mutual_guilds = data.get('mutual_guilds', False)
            mutual_friends = data.get('mutual_friends', False)
            
            key = mutual_guilds + (mutual_friends << 1)
        
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
        if (value >> 2) & 1:
            result['all'] = True
        else:
            if (value >> 1) & 1:
                result['mutual_friends'] = True
            if value & 1:
                result['mutual_guilds'] = True
        
        return result
    
    # predefined
    none = P(0, 'none')
    mutual_guilds = P(1, 'mutual guilds')
    mutual_friends = P(2, 'mutual friends')
    mutual_guilds_and_friends = P(3, 'mutual guilds and friends')
    all = P(4, 'all')


class Theme(PreinstancedBase, value_type = str):
    """
    Represents a user's theme.
    
    Attributes
    ----------
    name : `str`
        the theme's name.
    
    value : `str`
        The discord side identifier value of the theme.
    
    Type Attributes
    ---------------
    Each predefined theme instance can also be accessed as type attribute:
    
    +-----------------------+-----------+
    | Type attribute name   | value     |
    +=======================+===========+
    | dark                  | dark      |
    +-----------------------+-----------+
    | light                 | light     |
    +-----------------------+-----------+
    """
    __slots__ = ()
    
    # predefined
    dark = P('dark', 'dark')
    light = P('light', 'light')

__all__ = ('ForumLayout', 'SortOrder', 'VideoQualityMode', 'VoiceRegion',)

from ...bases import Preinstance as P, PreinstancedBase


class ForumLayout(PreinstancedBase):
    """
    Represents the default forum layout propagated by forum channels.
    
    Attributes
    ----------
    name : `str`
        The name of the forum layout.
    value : `int`
        The identifier value the forum layout.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ForumLayout``) items
        Stores the predefined ``ForumLayout``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The forum layouts' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the forum layouts.
    
    Every predefined forum layout can be accessed as class attribute as well:
    
    +-----------------------+-------------------+-------+
    | Class attribute name  | Name              | Value |
    +=======================+===================+=======+
    | none                  | none              | 0     |
    +-----------------------+-------------------+-------+
    | list                  | list              | 1     |
    +-----------------------+-------------------+-------+
    | gallery               | gallery           | 2     |
    +-----------------------+-------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    list = P(1, 'list')
    gallery = P(2, 'gallery')


class SortOrder(PreinstancedBase):
    """
    Represents the default sort order propagated by forum channels.
    
    Attributes
    ----------
    name : `str`
        The name of the sort order.
    value : `int`
        The identifier value the sort order.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``SortOrder``) items
        Stores the predefined ``SortOrder``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The sort orders' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the sort orders.
    
    Every predefined sort order can be accessed as class attribute as well:
    
    +-----------------------+-------------------+-------+
    | Class attribute name  | Name              | Value |
    +=======================+===================+=======+
    | latest_activity       | latest activity   | 0     |
    +-----------------------+-------------------+-------+
    | creation_date         | creation date     | 1     |
    +-----------------------+-------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    latest_activity = P(0, 'latest activity')
    creation_date = P(1, 'creation date')


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
        Stores the predefined ``VideoQualityMode``-s. These can be accessed with their `value` as key.
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
        The name of the voice region.
    vip : `bool`
        Whether the voice region can be used only by guilds with `VIP_REGIONS` feature.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``VoiceRegion``) items
        Stores the created ``VoiceRegion``-s.
    VALUE_TYPE : `type` = `str`
        The voice regions' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the voice regions.
    
    Each predefined voice region is also stored as a class attribute:
    
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | Class attribute name  | value         | name              | deprecated    | vip       | custom    |
    +=======================+===============+===================+===============+===========+===========+
    | _deprecated           | deprecated    | deprecated        | True          | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | unknown               | ''            | 'unknown'         | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
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
        self : ``VoiceRegion``
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
    
    
    def __init__(self, value, name, deprecated, vip):
        """
        Creates a new voice region with the given parameters and stores it at the class's `.INSTANCES`.
        
        Parameters
        ----------
        value : `str`
            The unique identifier of the voice region.
        name : `str`
            The voice region's name.
        deprecated : `bool`
            Whether the voice region is deprecated.
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
    
    
    _deprecated = P('deprecated', 'deprecated', True, False)
    unknown = P('', 'unknown', False, False)
    
    # normal
    brazil = P('brazil', 'Brazil', False, False)
    dubai = P('dubai', 'Dubai', False, False)
    eu_central = P('eu-central', 'Central Europe', False, False)
    eu_west = P('eu-west', 'Western Europe', False, False)
    europe = P('europe', 'Europe', False, False)
    hongkong = P('hongkong', 'Hong Kong', False, False)
    india = P('india', 'India', False, False)
    japan = P('japan', 'Japan', False, False)
    russia = P('russia', 'Russia', False, False)
    singapore = P('singapore', 'Singapore', False, False)
    africa_south = P('southafrica', 'South Africa', False, False)
    sydney = P('sydney', 'Sydney', False, False)
    us_central = P('us-central', 'US Central', False, False)
    us_east = P('us-east', 'US East', False, False)
    us_south = P('us-south', 'US South', False, False)
    us_west = P('us-west', 'US West', False, False)
    # deprecated
    amsterdam = P('amsterdam', 'Amsterdam', True, False)
    frankfurt = P('frankfurt', 'Frankfurt', True, False)
    london = P('london', 'London', True, False)
    # vip
    vip_us_east = P('vip-us-west', 'VIP US West', False, True)
    vip_us_west = P('vip-us-east', 'VIP US East', False, True)
    # vip + deprecated
    vip_amsterdam = P('vip-amsterdam', 'VIP Amsterdam', True, True)

__all__ = ('ForumLayout', 'SortOrder', 'VideoQualityMode', 'VoiceRegion',)

from ...bases import Preinstance as P, PreinstancedBase


class ForumLayout(PreinstancedBase, value_type = int):
    """
    Represents the default forum layout propagated by forum channels.
    
    Attributes
    ----------
    name : `str`
        The name of the forum layout.
    
    value : `int`
        The identifier value the forum layout.
    
    Type Attributes
    ---------------
    Every predefined forum layout can be accessed as type attribute as well:
    
    +-----------------------+-------------------+-------+
    | Type attribute name   | Name              | Value |
    +=======================+===================+=======+
    | none                  | none              | 0     |
    +-----------------------+-------------------+-------+
    | list                  | list              | 1     |
    +-----------------------+-------------------+-------+
    | gallery               | gallery           | 2     |
    +-----------------------+-------------------+-------+
    """
    __slots__ = ()
    
    none = P(0, 'none')
    list = P(1, 'list')
    gallery = P(2, 'gallery')


class SortOrder(PreinstancedBase, value_type = int):
    """
    Represents the default sort order propagated by forum channels.
    
    Attributes
    ----------
    name : `str`
        The name of the sort order.
    
    value : `int`
        The identifier value the sort order.
    
    Type Attributes
    ---------------
    Every predefined sort order can be accessed as type attribute as well:
    
    +-----------------------+-------------------+-------+
    | Type attribute name   | Name              | Value |
    +=======================+===================+=======+
    | latest_activity       | latest activity   | 0     |
    +-----------------------+-------------------+-------+
    | creation_date         | creation date     | 1     |
    +-----------------------+-------------------+-------+
    """
    __slots__ = ()
    
    latest_activity = P(0, 'latest activity')
    creation_date = P(1, 'creation date')


class VideoQualityMode(PreinstancedBase, value_type = int):
    """
    Represents a voice channel's video quality mode.
    
    Attributes
    ----------
    name : `str`
        The name of the video quality mode.
    
    value : `int`
        The identifier value the video quality mode.
    
    Type Attributes
    ---------------
    Every predefined video quality mode can be accessed as type attribute as well:
    
    +-----------------------+-------+-------+-------------------------------------------------------+
    | Type attribute name   | Name  | Value | Description                                           |
    +=======================+=======+=======+=======================================================+
    | none                  | none  | 0     | N/A                                                   |
    +-----------------------+-------+-------+-------------------------------------------------------+
    | auto                  | auto  | 1     | Discord chooses the quality for optimal performance.  |
    +-----------------------+-------+-------+-------------------------------------------------------+
    | full                  | full  | 2     | 720p                                                  |
    +-----------------------+-------+-------+-------------------------------------------------------+
    """
    __slots__ = ()
    
    none = P(0, 'none')
    auto = P(1, 'auto')
    full = P(2, 'full')


class VoiceRegion(PreinstancedBase, value_type = str):
    """
    Represents Discord's voice regions.
    
    Attributes
    ----------
    custom : `bool`
        Whether the voice region is custom (used for events, etc.).
    
    deprecated : `bool`
        Whether the voice region is deprecated.
    
    name : `str`
        The name of the voice region.
    
    value : `str`
        The unique identifier of the voice region.
    
    vip : `bool`
        Whether the voice region can be used only by guilds with `VIP_REGIONS` feature.
    
    Type Attributes
    ---------------
    Each predefined voice region is also stored as a type attribute:
    
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | Type attribute name   | value         | name              | deprecated    | vip       | custom    |
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
    __slots__ = ('custom', 'deprecated', 'vip',)
    
    
    def __new__(cls, value, name = None, custom = True, deprecated = False, vip = ...):
        """
        Creates a new voice region.
        
        Parameters
        ----------
        value : `str`
            The unique identifier of the voice region.
        
        name : `None | str` = `None`, Optional
            The voice region's name.
        
        custom : `bool` = `True`, Optional
            Whether the voice region is custom (used for events, etc.).
        
        deprecated : `bool` = `False`, Optional
            Whether the voice region is deprecated.
        
        vip : `bool`, Optional
            Whether the voice region can be used only by guilds with `VIP_REGIONS` feature.
        """
        if vip is ...:
            vip = value.startswith('vip-')
        
        if name is None:
            name_parts = value.split('-')
            for index in range(len(name_parts)):
                name_part = name_parts[index]
                if len(name_part) < 4:
                    name_part = name_part.upper()
                else:
                    name_part = name_part.capitalize()
                name_parts[index] = name_part
            
            name = ' '.join(name_parts)
        
        self = PreinstancedBase.__new__(cls, value, name)
        self.deprecated = deprecated
        self.vip = vip
        self.custom = custom
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a voice region.
        
        If the voice region already exists returns that instead.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received voice region data.

        Returns
        -------
        self : `instance<cls>`
        """
        value = data['id']
        try:
            return cls.INSTANCES[value]
        except KeyError:
            pass
        
        return cls(
            value,
            data['name'],
            data['custom'],
            data['deprecated'],
            data['vip'],
        )
    
    # predefined
    _deprecated = P('deprecated', 'deprecated', False, True, False)
    unknown = P('', 'unknown', False, False, False)
    
    # normal
    brazil = P('brazil', 'Brazil', False, False, False)
    dubai = P('dubai', 'Dubai', False, False, False)
    eu_central = P('eu-central', 'Central Europe', False, False, False)
    eu_west = P('eu-west', 'Western Europe', False, False, False)
    europe = P('europe', 'Europe', False, False, False)
    hongkong = P('hongkong', 'Hong Kong', False, False, False)
    india = P('india', 'India', False, False, False)
    japan = P('japan', 'Japan', False, False, False)
    russia = P('russia', 'Russia', False, False, False)
    singapore = P('singapore', 'Singapore', False, False, False)
    africa_south = P('southafrica', 'South Africa', False, False, False)
    sydney = P('sydney', 'Sydney', False, False, False)
    us_central = P('us-central', 'US Central', False, False, False)
    us_east = P('us-east', 'US East', False, False, False)
    us_south = P('us-south', 'US South', False, False, False)
    us_west = P('us-west', 'US West', False, False, False)
    # deprecated
    amsterdam = P('amsterdam', 'Amsterdam', False, True, False)
    frankfurt = P('frankfurt', 'Frankfurt', False, True, False)
    london = P('london', 'London', False, True, False)
    # vip
    vip_us_east = P('vip-us-west', 'VIP US West', False, False, True)
    vip_us_west = P('vip-us-east', 'VIP US East', False, False, True)
    # vip + deprecated
    vip_amsterdam = P('vip-amsterdam', 'VIP Amsterdam', False, True, True)

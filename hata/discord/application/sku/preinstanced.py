__all__ = ('SKUAccessType', 'SKUFeature', 'SKUGenre', 'SKUProductFamily', 'SKUType',)

from ...bases import Preinstance as P, PreinstancedBase



class SKUAccessType(PreinstancedBase, value_type = int):
    """
    Represents an SKU's access type.
    
    Attributes
    ----------
    name : `str`
        The name of the type.
    
    value : `int`
        The Discord side identifier value of the SKU access type.
        
    Type Attributes
    ---------------
    Every predefined SKU access type can be accessed as type attribute as well:
    
    +-----------------------+---------------+-------+
    | Type attribute name   | name          | Value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | full                  | full          | 1     |
    +-----------------------+---------------+-------+
    | early_access          | early access  | 2     |
    +-----------------------+---------------+-------+
    | vip_access            | vip access    | 3     |
    +-----------------------+---------------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    full = P(1, 'full')
    early_access = P(2, 'early access')
    vip_access = P(3, 'vip access')


class SKUFeature(PreinstancedBase, value_type = int):
    """
    Represents an SKU's feature type.
    
    Attributes
    ----------
    name : `str`
        The name of the SKU feature type.
    
    value : `int`
        The Discord side identifier value of the SKU feature type.
        
    Type Attributes
    ---------------
    Every predefined SKU feature type can be accessed as type attribute as well:
    
    +-----------------------+-----------------------+-------+
    | Type attribute name   | name                  | value |
    +=======================+=======================+=======+
    | none                  | none                  | 0     |
    +-----------------------+-----------------------+-------+
    | single_player         | single player         | 1     |
    +-----------------------+-----------------------+-------+
    | online_multiplayer    | online multiplayer    | 2     |
    +-----------------------+-----------------------+-------+
    | local_multiplayer     | local multiplayer     | 3     |
    +-----------------------+-----------------------+-------+
    | pvp                   | pvp                   | 4     |
    +-----------------------+-----------------------+-------+
    | local_coop            | local coop            | 5     |
    +-----------------------+-----------------------+-------+
    | cross_platform        | cross platform        | 6     |
    +-----------------------+-----------------------+-------+
    | rich_presence         | rich presence         | 7     |
    +-----------------------+-----------------------+-------+
    | discord_game_invites  | discord game invites  | 8     |
    +-----------------------+-----------------------+-------+
    | spectator_mode        | spectator mode        | 9     |
    +-----------------------+-----------------------+-------+
    | controller_support    | controller support    | 10    |
    +-----------------------+-----------------------+-------+
    | cloud_saves           | cloud saves           | 11    |
    +-----------------------+-----------------------+-------+
    | online_coop           | online coop           | 12    |
    +-----------------------+-----------------------+-------+
    | secure_networking     | secure networking     | 13    |
    +-----------------------+-----------------------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    single_player = P(1, 'single player')
    online_multiplayer = P(2, 'online multiplayer')
    local_multiplayer = P(3, 'local multiplayer')
    pvp = P(4, 'pvp')
    local_coop = P(5, 'local coop')
    cross_platform = P(6, 'cross platform')
    rich_presence = P(7, 'rich presence')
    discord_game_invites = P(8, 'discord game invites')
    spectator_mode = P(9, 'spectator mode')
    controller_support = P(10, 'controller support')
    cloud_saves = P(11, 'cloud saves')
    online_coop = P(12, 'online coop')
    secure_networking = P(13, 'secure networking')


class SKUGenre(PreinstancedBase, value_type = int):
    """
    Represents an SKU's feature type.
    
    Attributes
    ----------
    name : `str`
        The name of the SKU genre type.
    
    value : `int`
        The Discord side identifier value of the SKU genre.
        
    Type Attributes
    ---------------
    Every predefined SKU genre can be accessed as type attribute as well:
    
    +-----------------------+-----------------------+-------+
    | Type attribute name   | Name                  | Value |
    +=======================+=======================+=======+
    | none                  | none                  | 0     |
    +-----------------------+-----------------------+-------+
    | action                | action                | 1     |
    +-----------------------+-----------------------+-------+
    | action_rpg            | action rpg            | 2     |
    +-----------------------+-----------------------+-------+
    | brawler               | brawler               | 3     |
    +-----------------------+-----------------------+-------+
    | hack_and_slash        | hack and slash        | 4     |
    +-----------------------+-----------------------+-------+
    | platformer            | platformer            | 5     |
    +-----------------------+-----------------------+-------+
    | stealth               | stealth               | 6     |
    +-----------------------+-----------------------+-------+
    | survival              | survival              | 7     |
    +-----------------------+-----------------------+-------+
    | adventure             | adventure             | 8     |
    +-----------------------+-----------------------+-------+
    | action_adventure      | action adventure      | 9     |
    +-----------------------+-----------------------+-------+
    | metroidvania          | metroidvania          | 10    |
    +-----------------------+-----------------------+-------+
    | open_world            | open world            | 11    |
    +-----------------------+-----------------------+-------+
    | psychological_horror  | psychological horror  | 12    |
    +-----------------------+-----------------------+-------+
    | sandbox               | sandbox               | 13    |
    +-----------------------+-----------------------+-------+
    | survival_horror       | survival horror       | 14    |
    +-----------------------+-----------------------+-------+
    | visual_novel          | visual novel          | 15    |
    +-----------------------+-----------------------+-------+
    | driving_racing        | driving racing        | 16    |
    +-----------------------+-----------------------+-------+
    | vehicular_combat      | vehicular combat      | 17    |
    +-----------------------+-----------------------+-------+
    | massively_multiplayer | massively multiplayer | 18    |
    +-----------------------+-----------------------+-------+
    | mmorpg                | mmorpg                | 19    |
    +-----------------------+-----------------------+-------+
    | role_playing          | role playing          | 20    |
    +-----------------------+-----------------------+-------+
    | dungeon_crawler       | dungeon crawler       | 21    |
    +-----------------------+-----------------------+-------+
    | roguelike             | roguelike             | 22    |
    +-----------------------+-----------------------+-------+
    | shooter               | shooter               | 23    |
    +-----------------------+-----------------------+-------+
    | light_gun             | light gun             | 24    |
    +-----------------------+-----------------------+-------+
    | shoot_em_up           | shoot em up           | 25    |
    +-----------------------+-----------------------+-------+
    | fps                   | fps                   | 26    |
    +-----------------------+-----------------------+-------+
    | dual_joystick_shooter | dual joystick shooter | 27    |
    +-----------------------+-----------------------+-------+
    | simulation            | simulation            | 28    |
    +-----------------------+-----------------------+-------+
    | flight_simulation     | flight simulation     | 29    |
    +-----------------------+-----------------------+-------+
    | train_simulation      | train simulation      | 30    |
    +-----------------------+-----------------------+-------+
    | life_simulation       | life simulation       | 31    |
    +-----------------------+-----------------------+-------+
    | fishing               | fishing               | 32    |
    +-----------------------+-----------------------+-------+
    | sports                | sports                | 33    |
    +-----------------------+-----------------------+-------+
    | baseball              | baseball              | 34    |
    +-----------------------+-----------------------+-------+
    | basketball            | basketball            | 35    |
    +-----------------------+-----------------------+-------+
    | billiards             | billiards             | 36    |
    +-----------------------+-----------------------+-------+
    | bowling               | bowling               | 37    |
    +-----------------------+-----------------------+-------+
    | boxing                | boxing                | 38    |
    +-----------------------+-----------------------+-------+
    | football              | football              | 39    |
    +-----------------------+-----------------------+-------+
    | golf                  | golf                  | 40    |
    +-----------------------+-----------------------+-------+
    | hockey                | hockey                | 41    |
    +-----------------------+-----------------------+-------+
    | skateboarding_skating | skateboarding skating | 42    |
    +-----------------------+-----------------------+-------+
    | snowboarding_skiing   | snowboarding skiing   | 43    |
    +-----------------------+-----------------------+-------+
    | soccer                | soccer                | 44    |
    +-----------------------+-----------------------+-------+
    | track_field           | track field           | 45    |
    +-----------------------+-----------------------+-------+
    | surfing_wakeboarding  | surfing wakeboarding  | 46    |
    +-----------------------+-----------------------+-------+
    | wrestling             | wrestling             | 47    |
    +-----------------------+-----------------------+-------+
    | strategy              | strategy              | 48    |
    +-----------------------+-----------------------+-------+
    | four_x                | four x                | 49    |
    +-----------------------+-----------------------+-------+
    | artillery             | artillery             | 50    |
    +-----------------------+-----------------------+-------+
    | rts                   | rts                   | 51    |
    +-----------------------+-----------------------+-------+
    | tower_defense         | tower defense         | 52    |
    +-----------------------+-----------------------+-------+
    | turn_based_strategy   | turn based strategy   | 53    |
    +-----------------------+-----------------------+-------+
    | wargame               | wargame               | 54    |
    +-----------------------+-----------------------+-------+
    | moba                  | moba                  | 55    |
    +-----------------------+-----------------------+-------+
    | fighting              | fighting              | 56    |
    +-----------------------+-----------------------+-------+
    | puzzle                | puzzle                | 57    |
    +-----------------------+-----------------------+-------+
    | card_game             | card game             | 58    |
    +-----------------------+-----------------------+-------+
    | education             | education             | 59    |
    +-----------------------+-----------------------+-------+
    | fitness               | fitness               | 60    |
    +-----------------------+-----------------------+-------+
    | gambling              | gambling              | 61    |
    +-----------------------+-----------------------+-------+
    | music_rhythm          | music rhythm          | 62    |
    +-----------------------+-----------------------+-------+
    | party_mini_game       | party mini game       | 63    |
    +-----------------------+-----------------------+-------+
    | pinball               | pinball               | 64    |
    +-----------------------+-----------------------+-------+
    | trivia_board_game     | trivia board game     | 65    |
    +-----------------------+-----------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    none = P(0, 'none')
    action = P(1, 'action')
    action_rpg = P(2, 'action rpg')
    brawler = P(3, 'brawler')
    hack_and_slash = P(4, 'hack and slash')
    platformer = P(5, 'platformer')
    stealth = P(6, 'stealth')
    survival = P(7, 'survival')
    adventure = P(8, 'adventure')
    action_adventure = P(9, 'action adventure')
    metroidvania = P(10, 'metroidvania')
    open_world = P(11, 'open world')
    psychological_horror = P(12, 'psychological horror')
    sandbox = P(13, 'sandbox')
    survival_horror = P(14, 'survival horror')
    visual_novel = P(15, 'visual novel')
    driving_racing = P(16, 'driving racing')
    vehicular_combat = P(17, 'vehicular combat')
    massively_multiplayer = P(18, 'massively multiplayer')
    mmorpg = P(19, 'mmorpg')
    role_playing = P(20, 'role playing')
    dungeon_crawler = P(21, 'dungeon crawler')
    roguelike = P(22, 'roguelike')
    shooter = P(23, 'shooter')
    light_gun = P(24, 'light gun')
    shoot_em_up = P(25, 'shoot em up')
    fps = P(26, 'fps')
    dual_joystick_shooter = P(27, 'dual joystick shooter')
    simulation = P(28, 'simulation')
    flight_simulation = P(29, 'flight simulation')
    train_simulation = P(30, 'train simulation')
    life_simulation = P(31, 'life simulation')
    fishing = P(32, 'fishing')
    sports = P(33, 'sports')
    baseball = P(34, 'baseball')
    basketball = P(35, 'basketball')
    billiards = P(36, 'billiards')
    bowling = P(37, 'bowling')
    boxing = P(38, 'boxing')
    football = P(39, 'football')
    golf = P(40, 'golf')
    hockey = P(41, 'hockey')
    skateboarding_skating = P(42, 'skateboarding skating')
    snowboarding_skiing = P(43, 'snowboarding skiing')
    soccer = P(44, 'soccer')
    track_field = P(45, 'track field')
    surfing_wakeboarding = P(46, 'surfing wakeboarding')
    wrestling = P(47, 'wrestling')
    strategy = P(48, 'strategy')
    four_x = P(49, 'four x')
    artillery = P(50, 'artillery')
    rts = P(51, 'rts')
    tower_defense = P(52, 'tower defense')
    turn_based_strategy = P(53, 'turn based strategy')
    wargame = P(54, 'wargame')
    moba = P(55, 'moba')
    fighting = P(56, 'fighting')
    puzzle = P(57, 'puzzle')
    card_game = P(58, 'card game')
    education = P(59, 'education')
    fitness = P(60, 'fitness')
    gambling = P(61, 'gambling')
    music_rhythm = P(62, 'music rhythm')
    party_mini_game = P(63, 'party mini game')
    pinball = P(64, 'pinball')
    trivia_board_game = P(65, 'trivia board game')


class SKUProductFamily(PreinstancedBase, value_type = int):
    """
    Represents an SKU's product family.
    
    Attributes
    ----------
    name : `str`
        The name of the type.
    
    value : `int`
        The Discord side identifier value of the SKU product family.
        
    Type Attributes
    ---------------
    Every predefined SKU product family can be accessed as type attribute as well:
    
    +-----------------------+---------------+-------+
    | Type attribute name   | name          | Value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | premium               | premium       | 1     |
    +-----------------------+---------------+-------+
    | boost                 | boost         | 2     |
    +-----------------------+---------------+-------+
    | activity_iap          | activity_iap  | 3     |
    +-----------------------+---------------+-------+
    | guild_role            | guild_role    | 4     |
    +-----------------------+---------------+-------+
    | guild_product         | guild_product | 5     |
    +-----------------------+---------------+-------+
    | application           | application   | 6     |
    +-----------------------+---------------+-------+
    | collectibles          | collectibles  | 7     |
    +-----------------------+---------------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    premium = P(1, 'premium')
    boost = P(2, 'boost')
    activity_iap = P(2, 'activity iap')
    guild_role = P(3, 'guild role')
    guild_product = P(4, 'guild product')
    application = P(5, 'application')
    collectibles = P(6, 'collectibles')


class SKUType(PreinstancedBase, value_type = int):
    """
    Represents an SKU's type.
    
    Attributes
    ----------
    giftable : `bool`
        Whether the stock keeping unit is giftable.
    
    name : `str`
        The name of the type.
    
    package : `bool`
        Whether the stock keeping unit is a package (or bundle).
    
    value : `int`
        The Discord side identifier value of the SKU type.
    
    Type Attributes
    ---------------
    Every predefined SKU type can be accessed as type attribute as well:
    
    +-----------------------+-----------------------+-------+-----------+-----------+
    | Type attribute name   | Name                  | Value | Giftable  | Package   |
    +=======================+=======================+=======+===========+===========+
    | none                  | none                  | 0     | `False`   | `False`   |
    +-----------------------+-----------------------+-------+-----------+-----------+
    | durable_primary       | durable primary       | 1     | `True`    | `False`   |
    +-----------------------+-----------------------+-------+-----------+-----------+
    | durable               | durable               | 2     | `True`    | `False`   |
    +-----------------------+-----------------------+-------+-----------+-----------+
    | consumable            | consumable            | 3     | `False`   | `False`   |
    +-----------------------+-----------------------+-------+-----------+-----------+
    | bundle                | bundle                | 4     | `False`   | `True`    |
    +-----------------------+-----------------------+-------+-----------+-----------+
    | subscription          | subscription          | 5     | `True`    | `False`   |
    +-----------------------+-----------------------+-------+-----------+-----------+
    | subscription_group    | subscription group    | 6     | `False`   | `True`    |
    +-----------------------+-----------------------+-------+-----------+-----------+
    """
    __slots__ = ('giftable', 'package')
    
    def __new__(cls, value, name = None, giftable = False, package = False):
        """
        Creates a stock keeping unit type.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the stock keeping unit type.
        
        name : `None | str` = `None˙, Optional
            The default name of the stock keeping unit type.
        
        giftable : `bool` = `False`, Optional
            Whether the stock keeping unit is giftable.
        
        package : `bool` = `False`, Optional
            Whether the stock keeping unit is a package (or bundle).
        """
        self = PreinstancedBase.__new__(cls, value, name)
        self.giftable = giftable
        self.package = package
        return self
    
    
    # predefined
    none = P(0, 'none', False, False)
    durable_primary = P(1, 'durable primary', True, False)
    durable = P(2, 'durable', True, False)
    consumable = P(3, 'consumable', False, False)
    bundle = P(4, 'bundle', False, True)
    subscription = P(5, 'subscription', True, False)
    subscription_group = P(6, 'subscription group', False, True)

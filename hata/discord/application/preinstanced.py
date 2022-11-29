__all__ = ('EntitlementType', 'SKUAccessType', 'SKUFeatureType', 'SKUGenre', 'SKUType',)

from ..bases import Preinstance as P, PreinstancedBase


class SKUFeatureType(PreinstancedBase):
    """
    Represents an SKU's feature type.
    
    Attributes
    ----------
    name : `str`
        The name of the feature type.
    value : `int`
        The Discord side identifier value of the SKU feature type.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``SKUFeatureType``) items
        Stores the created SKU feature type instances. This container is accessed when translating a Discord
        SKU feature type's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The SKU feature types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the SKU feature types.
    
    Every predefined SKU feature type can be accessed as class attribute as well:
    +-----------------------+-----------------------+-------+
    | Class attribute name  | name                  | value |
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
    INSTANCES = {}
    VALUE_TYPE = int
    
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



class SKUGenre(PreinstancedBase):
    """
    Represents an SKU's feature type.
    
    Attributes
    ----------
    name : `str`
        The name of the feature type.
    value : `int`
        The Discord side identifier value of the SKU genre.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``SKUGenre``) items
        Stores the created SKU genre instances. This container is accessed when translating a Discord
        SKU genre's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The SKU genres' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the SKU genres.
    
    Every predefined SKU genre can be accessed as class attribute as well:
    +-----------------------+-----------------------+-------+
    | Class attribute name  | Name                  | Value |
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


class SKUAccessType(PreinstancedBase):
    """
    Represents an SKU's access type.
    
    Attributes
    ----------
    name : `str`
        The name of state.
    value : `int`
        The Discord side identifier value of the SKU access type.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``SKUAccessType``) items
        Stores the created SKU access type instances. This container is accessed when translating a Discord
        SKU access type's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The SKU access types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the SKU access types.
    
    Every predefined SKU access type can be accessed as class attribute as well:
    +-----------------------+---------------+-------+
    | Class attribute name  | name          | Value |
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
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    full = P(1, 'full')
    early_access = P(2, 'early access')
    vip_access = P(3, 'vip access')


class SKUType(PreinstancedBase):
    """
    Represents an SKU's type.
    
    Attributes
    ----------
    name : `str`
        The name of state.
    value : `int`
        The Discord side identifier value of the SKU type.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``SKUType``) items
        Stores the created SKU type instances. This container is accessed when translating a Discord
        SKU type's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The SKU types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the SKU types.
    
    Every predefined SKU type can be accessed as class attribute as well:
    +-----------------------+-------------------+-------+
    | Class attribute name  | Name              | Value |
    +=======================+===================+=======+
    | none                  | none              | 0     |
    +-----------------------+-------------------+-------+
    | durable_primary       | durable primary   | 1     |
    +-----------------------+-------------------+-------+
    | durable               | durable           | 2     |
    +-----------------------+-------------------+-------+
    | consumable            | consumable        | 3     |
    +-----------------------+-------------------+-------+
    | bundle                | bundle            | 4     |
    +-----------------------+-------------------+-------+
    | subscription          | subscription      | 5     |
    +-----------------------+-------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    durable_primary = P(1, 'durable primary')
    durable = P(2, 'durable')
    consumable = P(3, 'consumable')
    bundle = P(4, 'bundle')
    subscription = P(5, 'subscription')


class EntitlementType(PreinstancedBase):
    """
    Represents an entitlement's type.
    
    Attributes
    ----------
    name : `str`
        The name of state.
    value : `int`
        The Discord side identifier value of the entitlement type.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``EntitlementType``) items
        Stores the created entitlement type instances. This container is accessed when translating a Discord
        entitlement type's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The entitlement types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the entitlement types.
    
    Every predefined entitlement type can be accessed as class attribute as well:
    +---------------------------+---------------------------+-------+
    | Class attribute name      | Name                      | Value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | purchase                  | purchase                  | 1     |
    +---------------------------+---------------------------+-------+
    | premium_subscription      | premium subscription      | 2     |
    +---------------------------+---------------------------+-------+
    | developer_gift            | developer gift            | 3     |
    +---------------------------+---------------------------+-------+
    | test_mode_purchase        | test mode purchase        | 4     |
    +---------------------------+---------------------------+-------+
    | free_purchase             | free purchase             | 5     |
    +---------------------------+---------------------------+-------+
    | user_gift                 | user gift                 | 6     |
    +---------------------------+---------------------------+-------+
    | premium_purchase          | premium purchase          | 7     |
    +---------------------------+---------------------------+-------+
    | application_subscription  | application subscription  | 8     |
    +---------------------------+---------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    purchase = P(1, 'purchase')
    premium_subscription = P(2, 'premium subscription')
    developer_gift = P(3, 'developer gift')
    test_mode_purchase = P(4, 'test mode purchase')
    free_purchase = P(5, 'free purchase')
    user_gift = P(6, 'user gift')
    premium_purchase = P(7, 'premium purchase')
    application_subscription = P(8, 'application subscription')

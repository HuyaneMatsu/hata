__all__ = ('EntitlementType', 'SKUAccessType', 'SKUFeatureType', 'SKUGenre', 'SKUType', 'TeamMembershipState', )

from ..bases import PreinstancedBase, Preinstance as P

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
    | single_player         | single_player         | 1     |
    +-----------------------+-----------------------+-------+
    | online_multiplayer    | online_multiplayer    | 2     |
    +-----------------------+-----------------------+-------+
    | local_multiplayer     | local_multiplayer     | 3     |
    +-----------------------+-----------------------+-------+
    | pvp                   | pvp                   | 4     |
    +-----------------------+-----------------------+-------+
    | local_coop            | local_coop            | 5     |
    +-----------------------+-----------------------+-------+
    | cross_platform        | cross_platform        | 6     |
    +-----------------------+-----------------------+-------+
    | rich_presence         | rich_presence         | 7     |
    +-----------------------+-----------------------+-------+
    | discord_game_invites  | discord_game_invites  | 8     |
    +-----------------------+-----------------------+-------+
    | spectator_mode        | spectator_mode        | 9     |
    +-----------------------+-----------------------+-------+
    | controller_support    | controller_support    | 10    |
    +-----------------------+-----------------------+-------+
    | cloud_saves           | cloud_saves           | 11    |
    +-----------------------+-----------------------+-------+
    | online_coop           | online_coop           | 12    |
    +-----------------------+-----------------------+-------+
    | secure_networking     | secure_networking     | 13    |
    +-----------------------+-----------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    single_player = P(1, 'single_player')
    online_multiplayer = P(2, 'online_multiplayer')
    local_multiplayer = P(3, 'local_multiplayer')
    pvp = P(4, 'pvp')
    local_coop = P(5, 'local_coop')
    cross_platform = P(6, 'cross_platform')
    rich_presence = P(7, 'rich_presence')
    discord_game_invites = P(8, 'discord_game_invites')
    spectator_mode = P(9, 'spectator_mode')
    controller_support = P(10, 'controller_support')
    cloud_saves = P(11, 'cloud_saves')
    online_coop = P(12, 'online_coop')
    secure_networking = P(13, 'secure_networking')



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
    | Class attribute name  | name                  | value |
    +=======================+=======================+=======+
    | none                  | none                  | 0     |
    +-----------------------+-----------------------+-------+
    | action                | action                | 1     |
    +-----------------------+-----------------------+-------+
    | action_rpg            | action_rpg            | 2     |
    +-----------------------+-----------------------+-------+
    | brawler               | brawler               | 3     |
    +-----------------------+-----------------------+-------+
    | hack_and_slash        | hack_and_slash        | 4     |
    +-----------------------+-----------------------+-------+
    | platformer            | platformer            | 5     |
    +-----------------------+-----------------------+-------+
    | stealth               | stealth               | 6     |
    +-----------------------+-----------------------+-------+
    | survival              | survival              | 7     |
    +-----------------------+-----------------------+-------+
    | adventure             | adventure             | 8     |
    +-----------------------+-----------------------+-------+
    | action_adventure      | action_adventure      | 9     |
    +-----------------------+-----------------------+-------+
    | metroidvania          | metroidvania          | 10    |
    +-----------------------+-----------------------+-------+
    | open_world            | open_world            | 11    |
    +-----------------------+-----------------------+-------+
    | psychological_horror  | psychological_horror  | 12    |
    +-----------------------+-----------------------+-------+
    | sandbox               | sandbox               | 13    |
    +-----------------------+-----------------------+-------+
    | survival_horror       | survival_horror       | 14    |
    +-----------------------+-----------------------+-------+
    | visual_novel          | visual_novel          | 15    |
    +-----------------------+-----------------------+-------+
    | driving_racing        | driving_racing        | 16    |
    +-----------------------+-----------------------+-------+
    | vehicular_combat      | vehicular_combat      | 17    |
    +-----------------------+-----------------------+-------+
    | massively_multiplayer | massively_multiplayer | 18    |
    +-----------------------+-----------------------+-------+
    | mmorpg                | mmorpg                | 19    |
    +-----------------------+-----------------------+-------+
    | role_playing          | role_playing          | 20    |
    +-----------------------+-----------------------+-------+
    | dungeon_crawler       | dungeon_crawler       | 21    |
    +-----------------------+-----------------------+-------+
    | roguelike             | roguelike             | 22    |
    +-----------------------+-----------------------+-------+
    | shooter               | shooter               | 23    |
    +-----------------------+-----------------------+-------+
    | light_gun             | light_gun             | 24    |
    +-----------------------+-----------------------+-------+
    | shoot_em_up           | shoot_em_up           | 25    |
    +-----------------------+-----------------------+-------+
    | fps                   | fps                   | 26    |
    +-----------------------+-----------------------+-------+
    | dual_joystick_shooter | dual_joystick_shooter | 27    |
    +-----------------------+-----------------------+-------+
    | simulation            | simulation            | 28    |
    +-----------------------+-----------------------+-------+
    | flight_simulation     | flight_simulation     | 29    |
    +-----------------------+-----------------------+-------+
    | train_simulation      | train_simulation      | 30    |
    +-----------------------+-----------------------+-------+
    | life_simulation       | life_simulation       | 31    |
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
    | skateboarding_skating | skateboarding_skating | 42    |
    +-----------------------+-----------------------+-------+
    | snowboarding_skiing   | snowboarding_skiing   | 43    |
    +-----------------------+-----------------------+-------+
    | soccer                | soccer                | 44    |
    +-----------------------+-----------------------+-------+
    | track_field           | track_field           | 45    |
    +-----------------------+-----------------------+-------+
    | surfing_wakeboarding  | surfing_wakeboarding  | 46    |
    +-----------------------+-----------------------+-------+
    | wrestling             | wrestling             | 47    |
    +-----------------------+-----------------------+-------+
    | strategy              | strategy              | 48    |
    +-----------------------+-----------------------+-------+
    | four_x                | four_x                | 49    |
    +-----------------------+-----------------------+-------+
    | artillery             | artillery             | 50    |
    +-----------------------+-----------------------+-------+
    | rts                   | rts                   | 51    |
    +-----------------------+-----------------------+-------+
    | tower_defense         | tower_defense         | 52    |
    +-----------------------+-----------------------+-------+
    | turn_based_strategy   | turn_based_strategy   | 53    |
    +-----------------------+-----------------------+-------+
    | wargame               | wargame               | 54    |
    +-----------------------+-----------------------+-------+
    | moba                  | moba                  | 55    |
    +-----------------------+-----------------------+-------+
    | fighting              | fighting              | 56    |
    +-----------------------+-----------------------+-------+
    | puzzle                | puzzle                | 57    |
    +-----------------------+-----------------------+-------+
    | card_game             | card_game             | 58    |
    +-----------------------+-----------------------+-------+
    | education             | education             | 59    |
    +-----------------------+-----------------------+-------+
    | fitness               | fitness               | 60    |
    +-----------------------+-----------------------+-------+
    | gambling              | gambling              | 61    |
    +-----------------------+-----------------------+-------+
    | music_rhythm          | music_rhythm          | 62    |
    +-----------------------+-----------------------+-------+
    | party_mini_game       | party_mini_game       | 63    |
    +-----------------------+-----------------------+-------+
    | pinball               | pinball               | 64    |
    +-----------------------+-----------------------+-------+
    | trivia_board_game     | trivia_board_game     | 65    |
    +-----------------------+-----------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    none = P(0, 'none')
    action = P(1, 'action')
    action_rpg = P(2, 'action_rpg')
    brawler = P(3, 'brawler')
    hack_and_slash = P(4, 'hack_and_slash')
    platformer = P(5, 'platformer')
    stealth = P(6, 'stealth')
    survival = P(7, 'survival')
    adventure = P(8, 'adventure')
    action_adventure = P(9, 'action_adventure')
    metroidvania = P(10, 'metroidvania')
    open_world = P(11, 'open_world')
    psychological_horror = P(12, 'psychological_horror')
    sandbox = P(13, 'sandbox')
    survival_horror = P(14, 'survival_horror')
    visual_novel = P(15, 'visual_novel')
    driving_racing = P(16, 'driving_racing')
    vehicular_combat = P(17, 'vehicular_combat')
    massively_multiplayer = P(18, 'massively_multiplayer')
    mmorpg = P(19, 'mmorpg')
    role_playing = P(20, 'role_playing')
    dungeon_crawler = P(21, 'dungeon_crawler')
    roguelike = P(22, 'roguelike')
    shooter = P(23, 'shooter')
    light_gun = P(24, 'light_gun')
    shoot_em_up = P(25, 'shoot_em_up')
    fps = P(26, 'fps')
    dual_joystick_shooter = P(27, 'dual_joystick_shooter')
    simulation = P(28, 'simulation')
    flight_simulation = P(29, 'flight_simulation')
    train_simulation = P(30, 'train_simulation')
    life_simulation = P(31, 'life_simulation')
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
    skateboarding_skating = P(42, 'skateboarding_skating')
    snowboarding_skiing = P(43, 'snowboarding_skiing')
    soccer = P(44, 'soccer')
    track_field = P(45, 'track_field')
    surfing_wakeboarding = P(46, 'surfing_wakeboarding')
    wrestling = P(47, 'wrestling')
    strategy = P(48, 'strategy')
    four_x = P(49, 'four_x')
    artillery = P(50, 'artillery')
    rts = P(51, 'rts')
    tower_defense = P(52, 'tower_defense')
    turn_based_strategy = P(53, 'turn_based_strategy')
    wargame = P(54, 'wargame')
    moba = P(55, 'moba')
    fighting = P(56, 'fighting')
    puzzle = P(57, 'puzzle')
    card_game = P(58, 'card_game')
    education = P(59, 'education')
    fitness = P(60, 'fitness')
    gambling = P(61, 'gambling')
    music_rhythm = P(62, 'music_rhythm')
    party_mini_game = P(63, 'party_mini_game')
    pinball = P(64, 'pinball')
    trivia_board_game = P(65, 'trivia_board_game')


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
    | Class attribute name  | name          | value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | full                  | full          | 1     |
    +-----------------------+---------------+-------+
    | early_access          | early_access  | 2     |
    +-----------------------+---------------+-------+
    | vip_access            | vip_access    | 3     |
    +-----------------------+---------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    full = P(1, 'full')
    early_access = P(2, 'early_access')
    vip_access = P(3, 'vip_access')


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
    | Class attribute name  | name              | value |
    +=======================+===================+=======+
    | none                  | none              | 0     |
    +-----------------------+-------------------+-------+
    | durable_primary       | durable_primary   | 1     |
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
    durable_primary = P(1, 'durable_primary')
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
    +-----------------------+-----------------------+-------+
    | Class attribute name  | name                  | value |
    +=======================+=======================+=======+
    | none                  | none                  | 0     |
    +-----------------------+-----------------------+-------+
    | purchase              | purchase              | 1     |
    +-----------------------+-----------------------+-------+
    | premium_subscription  | premium_subscription  | 2     |
    +-----------------------+-----------------------+-------+
    | developer_gift        | developer_gift        | 3     |
    +-----------------------+-----------------------+-------+
    | test_mode_purchase    | test_mode_purchase    | 4     |
    +-----------------------+-----------------------+-------+
    | free_purchase         | free_purchase         | 5     |
    +-----------------------+-----------------------+-------+
    | user_gift             | user_gift             | 6     |
    +-----------------------+-----------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    purchase = P(1, 'purchase')
    premium_subscription = P(2, 'premium_subscription')
    developer_gift = P(3, 'developer_gift')
    test_mode_purchase = P(4, 'test_mode_purchase')
    free_purchase = P(5, 'free_purchase')
    user_gift = P(6, 'user_gift')

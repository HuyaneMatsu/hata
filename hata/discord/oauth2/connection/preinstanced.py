__all__ = ('ConnectionType', 'ConnectionVisibility',)

from warnings import warn

from scarletio import class_property

from ...bases import Preinstance as P, PreinstancedBase


class ConnectionType(PreinstancedBase):
    """
    Represents a connection's type.
    
    Attributes
    ----------
    name : `str`
        The name of the connection type.
    value : `str`
        The identifier value the connection type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``ConnectionType``) items
        Stores the predefined ``ConnectionType``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `str`
        The connection types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the connection types.
    
    Every predefined connection type can be accessed as class attribute as well:
    
    +-----------------------+-----------------------+-------------------+
    | Class attribute name  | Name                  | Value             |
    +=======================+=======================+===================+
    | battlenet             | Battle.net            | battlenet         |
    +-----------------------+-----------------------+-------------------+
    | crunchyroll           | Crunchyroll           | crunchyroll       |
    +-----------------------+-----------------------+-------------------+
    | domain                | Domain                | domain            |
    +-----------------------+-----------------------+-------------------+
    | ebay                  | eBay                  | ebay              |
    +-----------------------+-----------------------+-------------------+
    | epic_games            | Epic Games            | epicgames         |
    +-----------------------+-----------------------+-------------------+
    | facebook              | Facebook              | facebook          |
    +-----------------------+-----------------------+-------------------+
    | github                | GitHub                | github            |
    +-----------------------+-----------------------+-------------------+
    | instagram             | Instagram             | instagram         |
    +-----------------------+-----------------------+-------------------+
    | league_of_legends     | League of Legends     | leagueoflegends   |
    +-----------------------+-----------------------+-------------------+
    | none                  | none                  |                   |
    +-----------------------+-----------------------+-------------------+
    | paypal                | PayPal                | paypal            |
    +-----------------------+-----------------------+-------------------+
    | playstation           | PlayStation Network   | playstation       |
    +-----------------------+-----------------------+-------------------+
    | reddit                | Reddit                | reddit            |
    +-----------------------+-----------------------+-------------------+
    | riot_games            | Riot Games            | riotgames         |
    +-----------------------+-----------------------+-------------------+
    | samsung_galaxy        | Samsung Galaxy        | samsunggalaxy     |
    +-----------------------+-----------------------+-------------------+
    | spotify               | Spotify               | spotify           |
    +-----------------------+-----------------------+-------------------+
    | skype                 | Skype                 | skype             |
    +-----------------------+-----------------------+-------------------+
    | steam                 | Steam                 | steam             |
    +-----------------------+-----------------------+-------------------+
    | tiktok                | TikTok                | tiktok            |
    +-----------------------+-----------------------+-------------------+
    | twitch                | Twitch                | twitch            |
    +-----------------------+-----------------------+-------------------+
    | twitter               | X (Twitter)           | twitter           |
    +-----------------------+-----------------------+-------------------+
    | xbox                  | Xbox                  | xbox              |
    +-----------------------+-----------------------+-------------------+
    | youtube               | YouTube               | youtube           |
    +-----------------------+-----------------------+-------------------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    battlenet = P('battlenet', 'Battle.net')
    crunchyroll = P('crunchyroll', 'Crunchyroll')
    domain = P('domain', 'Domain')
    ebay = P('ebay', 'eBay')
    epic_games = P('epicgames', 'Epic Games')
    facebook = P('facebook', 'Facebook')
    github = P('github', 'GitHub')
    instagram = P('instagram', 'Instagram')
    league_of_legends = P('leagueoflegends', 'League of Legends')
    none = P('', 'none')
    paypal = P('paypal', 'PayPal')
    playstation = P('playstation', 'PlayStation Network')
    reddit = P('reddit', 'Reddit')
    riot_games = P('riotgames', 'Riot Games')
    samsung_galaxy = P('samsunggalaxy', 'Samsung Galaxy')
    spotify = P('spotify', 'Spotify')
    skype = P('skype', 'Skype')
    steam = P('steam', 'Steam')
    tiktok = P('tiktok', 'TikTok')
    twitch = P('twitch', 'Twitch')
    twitter = P('twitter', 'X (Twitter)')
    xbox = P('xbox', 'Xbox')
    youtube = P('youtube', 'YouTube')
    
    
    @class_property
    def unknown(cls):
        """
        Deprecated and will be removed in 2024 February. Please use `.none` instead.
        """
        warn(
            (
                f'`{cls.__name__}.unknown` is deprecated and will be removed in 2024 February. '
                f'Please use `.none` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return cls.none


class ConnectionVisibility(PreinstancedBase):
    """
    Represents a connection visibility.
    
    Attributes
    ----------
    name : `str`
        The name of the connection visibility.
    value : `str`
        The identifier value the connection visibility.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``ConnectionVisibility``) items
        Stores the predefined ``ConnectionVisibility``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `str`
        The connection visibilities' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the connection visibilities.
    
    Every predefined connection visibility can be accessed as class attribute as well:
    
    +-----------------------+-----------------------+-------------------+
    | Class attribute name  | Name                  | Value             |
    +=======================+=======================+===================+
    | user_only             | user only             | 0                 |
    +-----------------------+-----------------------+-------------------+
    | everyone              | everyone              | 1                 |
    +-----------------------+-----------------------+-------------------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    user_only = P(0, 'user only')
    everyone = P(1, 'everyone')

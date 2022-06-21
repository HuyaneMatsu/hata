__all__ = ('ConnectionType',)

from ..bases import Preinstance as P, PreinstancedBase


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
    | Class attribute name  | name                  | value             |
    +=======================+=======================+===================+
    | battlenet             | Battle.net            | battlenet         |
    +-----------------------+-----------------------+-------------------+
    | epic_games            | Epic Games            | epicgames         |
    +-----------------------+-----------------------+-------------------+
    | facebook              | Facebook              | facebook          |
    +-----------------------+-----------------------+-------------------+
    | github                | GitHub                | github            |
    +-----------------------+-----------------------+-------------------+
    | league_of_legends     | League of Legends     | leagueoflegends   |
    +-----------------------+-----------------------+-------------------+
    | playstation           | PlayStation Network   | playstation       |
    +-----------------------+-----------------------+-------------------+
    | reddit                | Reddit                | reddit            |
    +-----------------------+-----------------------+-------------------+
    | samsung_galaxy        | Samsung Galaxy        | samsunggalaxy     |
    +-----------------------+-----------------------+-------------------+
    | spotify               | Spotify               | spotify           |
    +-----------------------+-----------------------+-------------------+
    | skype                 | Skype                 | skype             |
    +-----------------------+-----------------------+-------------------+
    | steam                 | Steam                 | steam             |
    +-----------------------+-----------------------+-------------------+
    | twitch                | Twitch                | twitch            |
    +-----------------------+-----------------------+-------------------+
    | twitter               | Twitter               | twitter           |
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
    epic_games = P('epicgames', 'Epic Games')
    facebook = P('facebook', 'Facebook')
    github = P('github', 'GitHub')
    league_of_legends = P('leagueoflegends', 'League of Legends')
    playstation = P('playstation', 'PlayStation Network')
    reddit = P('reddit', 'Reddit')
    samsung_galaxy = P('samsunggalaxy', 'Samsung Galaxy')
    spotify = P('spotify', 'Spotify')
    skype = P('skype', 'Skype')
    steam = P('steam', 'Steam')
    twitch = P('twitch', 'Twitch')
    twitter = P('twitter', 'Twitter')
    xbox = P('xbox', 'Xbox')
    youtube = P('youtube', 'YouTube')

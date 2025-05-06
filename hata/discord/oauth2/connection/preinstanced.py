__all__ = ('ConnectionType', 'ConnectionVisibility',)

from ...bases import Preinstance as P, PreinstancedBase


class ConnectionType(PreinstancedBase, value_type = str):
    """
    Represents a connection's type.
    
    Attributes
    ----------
    name : `str`
        The name of the connection type.
    
    value : `str`
        The identifier value the connection type.
    
    Type Attributes
    ---------------
    Every predefined connection type can be accessed as type attribute as well:
    
    +-----------------------+-----------------------+-------------------+
    | Type attribute name   | Name                  | Value             |
    +=======================+=======================+===================+
    | amazon_music          | Amazon Music          | amazon-music      |
    +-----------------------+-----------------------+-------------------+
    | battlenet             | Battle.net            | battlenet         |
    +-----------------------+-----------------------+-------------------+
    | bluesky               | Bluesky               | bluesky           |
    +-----------------------+-----------------------+-------------------+
    | bungie                | Bungie.net            | bungie            |
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
    | mastodon              | Mastodon              | mastodon          |
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
    | roblox                | Roblox                | roblox            |
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
    __slots__ = ()
    
    amazon_music = P('amazon-music', 'Amazon Music')
    battlenet = P('battlenet', 'Battle.net')
    bluesky = P('bluesky', 'Bluesky')
    bungie = P('bungie', 'Bungie.net')
    crunchyroll = P('crunchyroll', 'Crunchyroll')
    domain = P('domain', 'Domain')
    ebay = P('ebay', 'eBay')
    epic_games = P('epicgames', 'Epic Games')
    facebook = P('facebook', 'Facebook')
    github = P('github', 'GitHub')
    instagram = P('instagram', 'Instagram')
    league_of_legends = P('leagueoflegends', 'League of Legends')
    mastodon = P('mastodon', 'Mastodon')
    none = P('', 'none')
    paypal = P('paypal', 'PayPal')
    playstation = P('playstation', 'PlayStation Network')
    reddit = P('reddit', 'Reddit')
    riot_games = P('riotgames', 'Riot Games')
    roblox = P('roblox', 'Roblox') # Only kids play roblox
    samsung_galaxy = P('samsunggalaxy', 'Samsung Galaxy')
    spotify = P('spotify', 'Spotify')
    skype = P('skype', 'Skype')
    steam = P('steam', 'Steam')
    tiktok = P('tiktok', 'TikTok')
    twitch = P('twitch', 'Twitch')
    twitter = P('twitter', 'X (Twitter)')
    xbox = P('xbox', 'Xbox')
    youtube = P('youtube', 'YouTube')


class ConnectionVisibility(PreinstancedBase, value_type = int):
    """
    Represents a connection visibility.
    
    Attributes
    ----------
    name : `str`
        The name of the connection visibility.
    
    value : `int`
        The identifier value the connection visibility.
    
    Type Attributes
    ---------------
    Every predefined connection visibility can be accessed as type attribute as well:
    
    +-----------------------+-----------------------+-------------------+
    | Type attribute name   | Name                  | Value             |
    +=======================+=======================+===================+
    | user_only             | user only             | 0                 |
    +-----------------------+-----------------------+-------------------+
    | everyone              | everyone              | 1                 |
    +-----------------------+-----------------------+-------------------+
    """
    __slots__ = ()
    
    user_only = P(0, 'user only')
    everyone = P(1, 'everyone')

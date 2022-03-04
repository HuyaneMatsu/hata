__all__ = (
    'BotInfo', 'BotStats', 'BotVote', 'BotsQueryResult', 'BriefUserInfo', 'GuildVote', 'UserConnections', 'UserInfo',
    'VoteBase'
)

from scarletio import copy_docs

from ...discord.bases import IconSlot, Slotted
from ...discord.color import Color
from ...discord.http import urls as module_urls
from ...discord.utils import timestamp_to_datetime

from .constants import (
    JSON_KEY_BOTS_QUERY_RESULT_COUNT, JSON_KEY_BOTS_QUERY_RESULT_LIMIT, JSON_KEY_BOTS_QUERY_RESULT_OFFSET,
    JSON_KEY_BOTS_QUERY_RESULT_RESULTS, JSON_KEY_BOTS_QUERY_RESULT_TOTAL, JSON_KEY_BOT_INFO_AVATAR_BASE64,
    JSON_KEY_BOT_INFO_BANNER_URL, JSON_KEY_BOT_INFO_CERTIFIED_AT, JSON_KEY_BOT_INFO_DISCRIMINATOR_STRING,
    JSON_KEY_BOT_INFO_DONATE_BOT_GUILD_ID, JSON_KEY_BOT_INFO_FEATURED_GUILD_ID_ARRAY, JSON_KEY_BOT_INFO_GITHUB_URL,
    JSON_KEY_BOT_INFO_ID, JSON_KEY_BOT_INFO_INVITE_URL, JSON_KEY_BOT_INFO_IS_CERTIFIED,
    JSON_KEY_BOT_INFO_LONG_DESCRIPTION, JSON_KEY_BOT_INFO_NAME, JSON_KEY_BOT_INFO_OWNER_ID_ARRAY,
    JSON_KEY_BOT_INFO_PREFIX, JSON_KEY_BOT_INFO_SHORT_DESCRIPTION, JSON_KEY_BOT_INFO_SUPPORT_SERVER_INVITE_URL,
    JSON_KEY_BOT_INFO_TAG_ARRAY, JSON_KEY_BOT_INFO_UPVOTES, JSON_KEY_BOT_INFO_UPVOTES_MONTHLY,
    JSON_KEY_BOT_INFO_VANITY_URL, JSON_KEY_BOT_INFO_WEBSITE_URL, JSON_KEY_BOT_STATS_GUILD_COUNT,
    JSON_KEY_BOT_STATS_GUILD_COUNT_PER_SHARD_ARRAY, JSON_KEY_BOT_STATS_SHARD_COUNT, JSON_KEY_BOT_STATS_SHARD_ID,
    JSON_KEY_BOT_VOTE_BOT_ID, JSON_KEY_BOT_VOTE_IS_WEEKEND, JSON_KEY_GUILD_VOTE_GUILD_ID,
    JSON_KEY_USER_INFO_AVATAR_BASE64, JSON_KEY_USER_INFO_BANNER_URL, JSON_KEY_USER_INFO_BIO, JSON_KEY_USER_INFO_COLOR,
    JSON_KEY_USER_INFO_CONNECTIONS, JSON_KEY_USER_INFO_CONNECTION_GITHUB, JSON_KEY_USER_INFO_CONNECTION_INSTAGRAM,
    JSON_KEY_USER_INFO_CONNECTION_REDDIT, JSON_KEY_USER_INFO_CONNECTION_TWITTER, JSON_KEY_USER_INFO_CONNECTION_YOUTUBE,
    JSON_KEY_USER_INFO_DISCRIMINATOR_STRING, JSON_KEY_USER_INFO_ID, JSON_KEY_USER_INFO_IS_ADMIN,
    JSON_KEY_USER_INFO_IS_CERTIFIED_DEVELOPER, JSON_KEY_USER_INFO_IS_MODERATOR, JSON_KEY_USER_INFO_IS_SUPPORTER,
    JSON_KEY_USER_INFO_IS_WEBSITE_MODERATOR, JSON_KEY_USER_INFO_NAME, JSON_KEY_VOTE_BASE_QUERY, JSON_KEY_VOTE_BASE_TYPE,
    JSON_KEY_VOTE_BASE_USER_ID
)


class BotInfo(metaclass=Slotted):
    """
    Representing information about a bot.
    
    Attributes
    ----------
    avatar_hash : `int`
        The bot's avatar hash.
    avatar_type : ``IconType``
        The bot's avatar's type.
    banner_url : `None`, `str`
        Url for the bot's banner image.
    certified_at : `None`, `datetime`
        When the bot was approved. Set as `None` if was not yet.
    discriminator : `int`
        The bot's discriminator.
    donate_bot_guild_id : `int`
        The guild id for the donate bot setup(?).
    featured_guild_ids : `None`, `tuple` of `int`
        The featured guild's identifiers on the bot's page.
    github_url : `None`, `str`
        Link to the github repo of the bot.
    id : `int`
        The bot's identifier.
    invite_url : `None`, `str`
        Custom bot invite url.
    long_description : `str`
        The long description of the bot.
    name : `str`
        The name of the bot.
    owner_id : `int
        The bot's main owner's identifier.
    owner_ids : `tuple` of `int`
        The bot's owners' identifiers.
    prefix : `str`
        Prefix of the bot.
    short_description : `str`
        The short description of the bot.
    support_server_invite_url : `None`, `str`
        Url to the bot's support server.
    tags : `None`, `tuple` of `str`
        The tags of the bot.
    upvotes : `int`
        The amount of upvotes the bot has.
    upvotes_monthly : `int`
        The amount of upvotes the bot has this month.
    vanity_url : `None`, `str`
        Vanity url of the bot.
    website_url : `None`, `str`
        The website url of the bot.
    """
    __slots__ = (
        'banner_url', 'certified_at', 'discriminator', 'donate_bot_guild_id', 'featured_guild_ids', 'github_url', 'id',
        'invite_url', 'long_description', 'name', 'owner_id', 'owner_ids', 'prefix', 'short_description',
        'support_server_invite_url', 'tags', 'upvotes', 'upvotes_monthly', 'vanity_url', 'website_url'
    )
    
    avatar = IconSlot(
        'avatar',
        JSON_KEY_BOT_INFO_AVATAR_BASE64,
        module_urls.user_avatar_url,
        module_urls.user_avatar_url_as,
    )
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new bot info instance.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Deserialized bot info data.
        
        Returns
        -------
        self : ``BotInfo``
        """
        self = object.__new__(cls)
        
        # avatar_hash & avatar_type
        self._set_avatar(data)
        
        # banner_url
        self.banner_url = data.get(JSON_KEY_BOT_INFO_BANNER_URL, None)
        
        # certified_at
        if data.get(JSON_KEY_BOT_INFO_IS_CERTIFIED, False):
            certified_at = timestamp_to_datetime(data[JSON_KEY_BOT_INFO_CERTIFIED_AT])
        else:
            certified_at = None
        self.certified_at = certified_at
        
        # discriminator
        self.discriminator = int(data[JSON_KEY_BOT_INFO_DISCRIMINATOR_STRING])
        
        # donate_bot_guild_id
        donate_bot_guild_id = data[JSON_KEY_BOT_INFO_DONATE_BOT_GUILD_ID]
        if donate_bot_guild_id:
            donate_bot_guild_id = int(donate_bot_guild_id)
        else:
            donate_bot_guild_id = 0
        self.donate_bot_guild_id = donate_bot_guild_id
        
        # featured_guild_ids
        featured_guild_ids = data.get(JSON_KEY_BOT_INFO_FEATURED_GUILD_ID_ARRAY, None)
        if (featured_guild_ids is None) or (not featured_guild_ids):
            featured_guild_ids = None
        else:
            featured_guild_ids = tuple(sorted(int(guild_id) for guild_id in featured_guild_ids))
        self.featured_guild_ids = featured_guild_ids
        
        # github_url
        self.github_url = data.get(JSON_KEY_BOT_INFO_GITHUB_URL, None)
        
        # id
        self.id = int(data[JSON_KEY_BOT_INFO_ID])
        
        # invite_url
        self.invite_url = data.get(JSON_KEY_BOT_INFO_INVITE_URL, None)
        
        # long_description
        self.long_description = data[JSON_KEY_BOT_INFO_LONG_DESCRIPTION]
        
        # name
        self.name = data[JSON_KEY_BOT_INFO_NAME]
        
        # owner_id & owner_ids
        owner_ids = data[JSON_KEY_BOT_INFO_OWNER_ID_ARRAY]
        self.owner_id = int(owner_ids[0])
        self.owner_ids = tuple(sorted(int(owner_id) for owner_id in owner_ids))
        
        # prefix
        self.prefix = data[JSON_KEY_BOT_INFO_PREFIX]
        
        # short_description
        self.short_description = data[JSON_KEY_BOT_INFO_SHORT_DESCRIPTION]
        
        # support_server_invite_url
        self.support_server_invite_url = data.get(JSON_KEY_BOT_INFO_SUPPORT_SERVER_INVITE_URL, None)
        
        # tags
        self.tags = tuple(sorted(data[JSON_KEY_BOT_INFO_TAG_ARRAY]))
        
        # upvotes
        self.upvotes = data[JSON_KEY_BOT_INFO_UPVOTES]
        
        # upvotes_monthly
        self.upvotes_monthly = data[JSON_KEY_BOT_INFO_UPVOTES_MONTHLY]
        
        # vanity_url
        self.vanity_url = data.get(JSON_KEY_BOT_INFO_VANITY_URL, None)
        
        # website_url
        self.website_url = data.get(JSON_KEY_BOT_INFO_WEBSITE_URL, None)
        
        return self
    
    
    def __repr__(self):
        """Returns the bot info's representation."""
        return f'<{self.__class__.__name__} id={self.id} name={self.name}>'


class BotStats:
    """
    Contains a listed bot's stats.
    
    Attributes
    ----------
    guild_count : `int`
        The amount of guilds the bot is in. Defaults to `-1`.
    guild_count_per_shard : `tuple` of `int`
        The amount of guilds per shards. Can be empty.
    shard_count : `int`
        The amount of shards the bot has. Defaults to `-1`.
    shard_id : `int`
        The shard ID to post as (?). Defaults to `-1`.
    """
    __slots__ = ('guild_count', 'guild_count_per_shard', 'shard_count', 'shard_id')
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new bot stats instance.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Deserialized bot stats data.
        
        Returns
        -------
        self : ``BotStats``
        """
        self = object.__new__(cls)
        
        # guild_count
        self.guild_count = data.get(JSON_KEY_BOT_STATS_GUILD_COUNT, -1)
        
        # guild_count_per_shard
        try:
            guild_count_per_shard = data[JSON_KEY_BOT_STATS_GUILD_COUNT_PER_SHARD_ARRAY]
        except KeyError:
            guild_count_per_shard = ()
        self.guild_count_per_shard = guild_count_per_shard
        
        # shard_count
        self.shard_count = data.get(JSON_KEY_BOT_STATS_SHARD_COUNT, -1)
        
        # shard_id
        self.shard_id = data.get(JSON_KEY_BOT_STATS_SHARD_ID, -1)
        
        return self
    
    
    def __repr__(self):
        """Returns the bot stats' representation."""
        return f'<{self.__class__.__name__}>'


class UserInfo(metaclass=Slotted):
    """
    Represents a user.
    
    Attributes
    ----------
    avatar_hash : `int`
        The bot's avatar hash.
    avatar_type : ``IconType``
        The bot's avatar's type.
    banner_url : `None`, `str`
        Url for the user's banner image.
    bio : `None`, `str`
        The user's bio.
    color : ``Color``
        The custom color of the user.
    connections : ``UserConnections``
        Connections of the users to social networks.
    discriminator : `int`
        The user's discriminator.
    id : `int`
        The user's identifier.
    is_admin : `bool`
        Whether the user is an admin.
    is_certified_developer : `bool`
        Whether the user is a certified developer.
    is_moderator : `bool`
        Whether the user is moderator.
    is_supporter : `bool`
        Whether the user is a supporter.
    is_website_moderator : `bool`
        Whether the user is a website moderator.
    name : `str`
        The user's name.
    """
    __slots__ = (
        'banner_url', 'bio', 'color', 'connections', 'discriminator', 'id', 'is_admin', 'is_certified_developer',
        'is_moderator', 'is_supporter', 'is_website_moderator', 'name'
    )

    avatar = IconSlot(
        'avatar',
        JSON_KEY_USER_INFO_AVATAR_BASE64,
        module_urls.user_avatar_url,
        module_urls.user_avatar_url_as,
    )
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new user info instance.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Deserialized user info data.
        
        Returns
        -------
        self : ``UserInfo``
        """
        self = object.__new__(cls)
        
        # avatar_hash & avatar_type
        self._set_avatar(data)
        
        # banner_url
        self.banner_url = data.get(JSON_KEY_USER_INFO_BANNER_URL, None)
        
        # bio
        self.bio = data.get(JSON_KEY_USER_INFO_BIO, None)
        
        # color
        try:
            color = Color(data[JSON_KEY_USER_INFO_COLOR], base=16)
        except ValueError:
            color = Color()
        self.color = color
        
        # connections
        self.connections = UserConnections.from_data(data[JSON_KEY_USER_INFO_CONNECTIONS])
        
        # discriminator
        self.discriminator = int(data[JSON_KEY_USER_INFO_DISCRIMINATOR_STRING])
        
        # id
        self.id = int(data[JSON_KEY_USER_INFO_ID])
        
        # is_admin
        self.is_admin = data[JSON_KEY_USER_INFO_IS_ADMIN]
        
        # is_certified_developer
        self.is_certified_developer = data[JSON_KEY_USER_INFO_IS_CERTIFIED_DEVELOPER]
        
        # is_moderator
        self.is_moderator = data[JSON_KEY_USER_INFO_IS_MODERATOR]
        
        # is_supporter
        self.is_supporter = data[JSON_KEY_USER_INFO_IS_SUPPORTER]
        
        # is_website_moderator
        self.is_website_moderator = data[JSON_KEY_USER_INFO_IS_WEBSITE_MODERATOR]
        
        # name
        self.name = data[JSON_KEY_USER_INFO_NAME]
        
        return self
    
    
    def __repr__(self):
        """Returns the bot info's representation."""
        return f'<{self.__class__.__name__} id={self.id} name={self.name}>'


class UserConnections:
    """
    Represents an user's connections.
    
    Attributes
    ----------
    github : `None`, `str`
        The github user name of the user.
    instagram : `None`, `str`
        The instagram user name of the user.
    reddit : `None`, `str`
        The reddit user name of the user.
    twitter : `None`, `str`
        The twitter user name of the user.
    youtube : `None`, `str`
        The youtube user name of the user.
    """
    __slots__ = ('github', 'instagram', 'reddit', 'twitter', 'youtube')
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new user info instance.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Deserialized user info data.
        
        Returns
        -------
        self : ``UserInfo``
        """
        self = object.__new__(cls)
        
        # github
        self.github = data.get(JSON_KEY_USER_INFO_CONNECTION_GITHUB, None)
        
        # instagram
        self.instagram = data.get(JSON_KEY_USER_INFO_CONNECTION_INSTAGRAM, None)
        
        # reddit
        self.reddit = data.get(JSON_KEY_USER_INFO_CONNECTION_REDDIT, None)
        
        # twitter
        self.twitter = data.get(JSON_KEY_USER_INFO_CONNECTION_TWITTER, None)
        
        # youtube
        self.youtube = data.get(JSON_KEY_USER_INFO_CONNECTION_YOUTUBE, None)
        
        return self
    
    
    def __repr__(self):
        """Returns the bot info's representation."""
        return f'<{self.__class__.__name__}>'


class BriefUserInfo(metaclass=Slotted):
    """
    Represents a user, containing only brief fields.
    
    Attributes
    ----------
    avatar_hash : `int`
        The bot's avatar hash.
    avatar_type : ``IconType``
        The bot's avatar's type.
    discriminator : `int`
        The user's discriminator.
    id : `int`
        The user's identifier.
    name : `str`
        The user's name.
    """
    __slots__ = ('discriminator', 'id', 'name')

    avatar = IconSlot(
        'avatar',
        JSON_KEY_USER_INFO_AVATAR_BASE64,
        module_urls.user_avatar_url,
        module_urls.user_avatar_url_as,
    )
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new user info instance.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Deserialized user info data.
        
        Returns
        -------
        self : ``UserInfo``
        """
        self = object.__new__(cls)
        
        # avatar_hash & avatar_type
        self._set_avatar(data)
        
        # discriminator
        self.discriminator = int(data[JSON_KEY_USER_INFO_DISCRIMINATOR_STRING])
        
        # id
        self.id = int(data[JSON_KEY_USER_INFO_ID])
        
        # name
        self.name = data[JSON_KEY_USER_INFO_NAME]
        
        return self
    
    
    def __repr__(self):
        """Returns the bot info's representation."""
        return f'<{self.__class__.__name__} id={self.id} name={self.name}>'


class BotsQueryResult:
    """
    Represents a get bots query's result.
    
    Attributes
    ----------
    count : `int`
        The number of received bots.
    limit : `int`
        The limit used.
    offset : `int`
        The off set used.
    results : `None`, `tuple` of ``BotInfo``
        The matched bots.
    total : `int`
        The total number of bots matching the query.
    """
    __slots__ = ('count', 'limit', 'offset', 'results', 'total')
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new bots query result instance.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Deserialized bots query result data.
        
        Returns
        -------
        self : ``BotsQueryResult``
        """
        self = object.__new__(cls)
        
        # count
        self.count = data[JSON_KEY_BOTS_QUERY_RESULT_COUNT]
        
        # limit
        self.limit = data[JSON_KEY_BOTS_QUERY_RESULT_LIMIT]
        
        # offset
        self.offset = data[JSON_KEY_BOTS_QUERY_RESULT_OFFSET]
        
        # results
        bot_info_datas = data[JSON_KEY_BOTS_QUERY_RESULT_RESULTS]
        if bot_info_datas:
            results = tuple(BotInfo.from_data(bot_info_data) for bot_info_data in bot_info_datas)
        else:
            results = None
        self.results = results
        
        # total
        self.total = data[JSON_KEY_BOTS_QUERY_RESULT_TOTAL]
        
        return self
    
    def __repr__(self):
        """Returns the bot info's representation."""
        return f'<{self.__class__.__name__} count={self.count} total={self.total}>'
    
    def __len__(self):
        """Returns the length of the query result"""
        return self.count
    
    def __iter__(self):
        """Iterates over the query result."""
        results = self.results
        if (results is not None):
            yield from results
    
    def __reversed__(self):
        """Reversed iterates over the query result."""
        results = self.results
        if (results is not None):
            yield from reversed(results)
    
    def __getitem__(self, index):
        """Gets the elements of the query result."""
        results = self.results
        if results is None:
            if isinstance(index, slice):
                return ()
            
            raise IndexError(index)
        
        return results[index]


class VoteBase:
    """
    Base class for vote instances received with webhook.
    
    Attributes
    ----------
    query : `str`
        Query used to redirect to vote.
    type : `str`
        The vote's type. Can be either `'upvote'`, `'test'`.
    user_id : `int`
        The user's identifier, who voted.
    """
    __slots__ = ('query', 'type', 'user_id')
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new vote instance.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Deserialized vote webhook data.
        
        Returns
        -------
        self : ``VoteBase``
        """
        self = object.__new__(cls)
        
        # query
        self.query = data[JSON_KEY_VOTE_BASE_QUERY]
        
        # type
        self.type = data[JSON_KEY_VOTE_BASE_TYPE]
        
        # user_id
        self.user_id = int(data[JSON_KEY_VOTE_BASE_USER_ID])
        
        return self
    
    def __repr__(self):
        """Returns the vote's representation."""
        return f'<{self.__class__.__name__} user_id={self.user_id!r}>'


class BotVote(VoteBase):
    """
    Bot vote received with webhook.
    
    Attributes
    ----------
    query : `str`
        Query used to redirect to vote.
    type : `str`
        The vote's type. Can be either `'upvote'`, `'test'`.
    user_id : `int`
        The user's identifier, who voted.
    bot_id : `int`
        The bot's identifier.
    is_weekend : `bool`
        Whether the vote was done on a weekend.
    """
    __slots__ = ('bot_id', 'is_weekend')

    @classmethod
    @copy_docs(VoteBase.from_data)
    def from_data(cls, data):
        self = super(BotVote, cls).from_data(data)
        
        self.bot_id = int(data[JSON_KEY_BOT_VOTE_BOT_ID])
        
        self.is_weekend = data.get(JSON_KEY_BOT_VOTE_IS_WEEKEND, False)
        
        return self
    
    @copy_docs(VoteBase.__repr__)
    def __repr__(self):
        return f'<{self.__class__.__name__} user_id={self.user_id!r} bot_id={self.bot_id!r}>'


class GuildVote(VoteBase):
    """
    Guild vote received with webhook.
    
    Attributes
    ----------
    query : `str`
        Query used to redirect to vote.
    type : `str`
        The vote's type. Can be either `'upvote'`, `'test'`.
    user_id : `int`
        The user's identifier, who voted.
    guild_id : `int`
        The guild's identifier.
    """
    __slots__ = ('guild_id',)

    @classmethod
    @copy_docs(VoteBase.from_data)
    def from_data(cls, data):
        self = super(GuildVote, cls).from_data(data)
        
        self.guild_id = int(data[JSON_KEY_GUILD_VOTE_GUILD_ID])
        
        return self
    
    @copy_docs(VoteBase.__repr__)
    def __repr__(self):
        return f'<{self.__class__.__name__} user_id={self.user_id!r} guild_id={self.guild_id!r}>'

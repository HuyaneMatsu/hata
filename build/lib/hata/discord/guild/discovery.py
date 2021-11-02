__all__ = ('DiscoveryCategory', 'GuildDiscovery', )

from ..bases import DiscordEntity
from ..core import DISCOVERY_CATEGORIES
from ..utils import DISCORD_EPOCH_START, timestamp_to_datetime

class GuildDiscovery:
    """
    Represent a guild's Discovery settings.
    
    Attributes
    ----------
    application_actioned : `None` or `datetime`
        When the guild's application was accepted or rejected.
    application_requested : `None` or `datetime`
        When the guild applied to guild discovery. Only set if pending.
    emoji_discovery : `bool`
        Whether guild info is shown when the respective guild's emojis are clicked.
    guild : `Guild`
        The represented guild.
    keywords : `None` or (`set` of `str`)
        The set discovery search keywords for the guild.
    primary_category_id : `int`
        The `id` of the primary discovery category of the guild.
    sub_category_ids : `set` of `int`
        Guild Discovery sub-category id-s. Can be maximum 5.
    """
    __slots__ = ('application_actioned', 'application_requested', 'emoji_discovery', 'guild', 'keywords',
        'primary_category', 'sub_categories')
    def __init__(self, data, guild):
        """
        Creates a new ``GuildDiscovery`` from the requested data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Requested guild discovery data.
        guild : ``Guild``
            The owner guild.
        """
        self.guild = guild
        
        self._update_attributes(data)
    
    def _update_attributes(self, data):
        """
        Updates the guild discovery object from the given data by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Guild discovery data.
        """
        self.sub_categories = set(DiscoveryCategory.from_id(category_id) for category_id in data['category_ids'])
        self.emoji_discovery = data['emoji_discoverability_enabled']
        
        keywords = data['keywords']
        if (keywords is not None):
            if keywords :
                keywords = set(keywords)
            else:
                keywords = None
        self.keywords = keywords
        
        self.primary_category = DiscoveryCategory.from_id(data['primary_category_id'], primary=True)
        
        application_actioned = data.get('partner_actioned_timestamp', None)
        if (application_actioned is not None):
            application_actioned = timestamp_to_datetime(application_actioned)
        
        self.application_actioned = application_actioned
        
        application_requested = data.get('partner_application_timestamp', None)
        if (application_requested is not None):
            application_requested = timestamp_to_datetime(application_requested)
        
        self.application_requested = application_requested
        
    def __eq__(self, other):
        """Returns whether the two guild discoveries are the same."""
        if (type(self) is not type(other)):
            return NotImplemented
        
        if (self.guild is not other.guild):
            return False
        
        if (self.primary_category != other.primary_category_id):
            return False
        
        if (self.emoji_discovery != other.emoji_discovery):
            return False
        
        # Leave the set-s last.
        if (self.sub_categories != other.category_ids):
            return False
        
        # Keywords can be `None`.
        if (self.keywords != other.keywords):
            return False
        
        if (self.application_actioned != other.application_actioned):
            return False
        
        return True
    
    def __hash__(self):
        """Returns the guild discovery's hash value."""
        return self.guild.id
    
    def __repr__(self):
        """Returns the guild discovery's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' of guild ',
        ]
        
        guild = self.guild
        repr_parts.append(repr(guild.name))
        repr_parts.append(' (')
        repr_parts.append(repr(guild.id))
        repr_parts.append(')>')
        
        return ''.join(repr_parts)


class DiscoveryCategory(DiscordEntity, immortal=True):
    """
    Represents a category of a ``GuildDiscovery``.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the discovery category.
    local_names : `None` or `dict` of (`str`, `str`) items
        The category's name in other languages.
    name : `str`
        The category's name.
    primary : `bool`
        Whether this category can be set as a guild's primary category.
    
    Class Attributes
    ----------------
    There are predefined discovery categories, which can be accessed as class attributes as well:
    
    +-------------------------------+-------+-------------------------------+-----------+
    | Class attribute name          | id    | name                          | primary   |
    +===============================+=======+===============================+===========+
    | general                       | `0`   | `'General'`                   | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | gaming                        | `1`   | `'Gaming'`                    | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | music                         | `2`   | `'Music'`                     | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | entertainment                 | `3`   | `'Entertainment'`             | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | creative_arts                 | `4`   | `'Creative Arts'`             | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | science_and_tech              | `5`   | `'Science & Tech'`            | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | education                     | `6`   | `'Education'`                 | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | sports                        | `7`   | `'Sports'`                    | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | fashion_and_beauty            | `8`   | `'Fashion & Beauty'`          | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | relationships_and_identity    | `9`   | `'Relationships & Identity'`  | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | travel_and_food               | `10`  | `'Travel & Food'`             | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | fitness_and_health            | `11`  | `'Fitness & Health'`          | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | finance                       | `12`  | `'Finance'`                   | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | other                         | `13`  | `'Other'`                     | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | general_chatting              | `14`  | `'General Chatting'`          | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | esports                       | `15`  | `'Esports'`                   | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | anime_and_manga               | `16`  | `'Anime & Manga'`             | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | movies_and_tv                 | `17`  | `'Movies & TV'`               | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | books                         | `18`  | `'Books'`                     | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | art                           | `19`  | `'Art'`                       | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | writing                       | `20`  | `'Writing'`                   | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | crafts_diy_and_making         | `21`  | `'Crafts, DIY, & Making'`     | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | programming                   | `22`  | `'Programming'`               | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | podcasts                      | `23`  | `'Podcasts'`                  | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | tabletop_games                | `24`  | `'Tabletop Games'`            | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | memes                         | `25`  | `'Memes'`                     | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | news_and_current_events       | `26`  | `'News & Current Events'`     | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | cryptocurrency                | `27`  | `'Cryptocurrency'`            | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | investing                     | `28`  | `'Investing'`                 | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | studying_and_teaching         | `29`  | `'Studying & Teaching'`       | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | lfg                           | `30`  | `'LFG'`                       | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | customer_support              | `31`  | `'Customer Support'`          | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | theorycraft                   | `32`  | `'Theorycraft'`               | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | events                        | `33`  | `'Events'`                    | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | roleplay                      | `34`  | `'Roleplay'`                  | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | content_creator               | `35`  | `'Content Creator'`           | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | business                      | `36`  | `'Business'`                  | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | local_group                   | `37`  | `'Local Group'`               | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | collaboration                 | `38`  | `'Collaboration'`             | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | fandom                        | `39`  | `'Fandom'`                    | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | wiki_and_guide                | `40`  | `'Wiki & Guide'`              | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | subreddit                     | `42`  | `'Subreddit'`                 | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | emoji                         | `43`  | `'Emoji'`                     | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | comics_and_cartoons           | `44`  | `'Comics & Cartoons'`         | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | mobile                        | `45`  | `'Mobile'`                    | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | console                       | `46`  | `'Console'`                   | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | charity_and_nonprofit         | `47`  | `'Charity & Nonprofit'`       | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    
    Notes
    -----
    Guild discovery objects are weakreferable.
    """
    __slots__ = ('local_names', 'name', 'primary')
    
    @classmethod
    def from_id(cls, category_id, primary=False):
        """
        Tries to find the category by the given id. If exists returns that, else creates a new one.
        
        Parameters
        ----------
        category_id : `int`
            The unique identifier number of the discovery category
        primary : `bool`, Optional
            Whether the category is a primary category.
        
        Returns
        -------
        category : ``DiscoveryCategory``
        """
        try:
            category = DISCOVERY_CATEGORIES[category_id]
        except KeyError:
            category = object.__new__(cls)
            DISCOVERY_CATEGORIES[category_id] = category
            category.id = category_id
            category.name = ''
            category.local_names = None
            category.primary = primary
        
        if primary:
            category.primary = True
        
        return category
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new ``DiscoveryCategory`` object from the given data. if the discovery category already
        exists returns that instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Discovery category data.
        
        Returns
        -------
        category : ``DiscoveryCategory``
        """
        # Note that even tho id is received as integer, but integers over 32 bits are still received as string.
        category_id = int(data['id'])
        
        try:
            category = DISCOVERY_CATEGORIES[category_id]
        except KeyError:
            category = object.__new__(cls)
            DISCOVERY_CATEGORIES[category_id] = category
            category.id = category_id
        
        category.primary = data['is_primary']
        name_data = data['name']
        category.name = name_data['default']
        
        local_names = name_data.get('localizations', None)
        if (local_names is not None) and (not local_names):
            local_names = None
        
        category.local_names = local_names
        
        return category
    
    def __init__(self, category_id, name, primary):
        """
        Creates a new discovery category from the given parameters.
        
        Parameters
        ----------
        category_id : `int`
            The unique identifier number of the discovery category.
        name : `str`
            The category's name.
        primary : `bool`
            Whether this category can be set as a guild's primary category.
        """
        self.id = category_id
        self.name = name
        self.primary = primary
        self.local_names = None
        
        DISCOVERY_CATEGORIES[category_id] = self
    
    def created_at(self):
        """
        Returns when the discovery category was created.
        
        Because discovery category id-s are not snowflakes, this method will return the start of the discord epoch.
        
        Returns
        -------
        created_at : `datetime`
        """
        return DISCORD_EPOCH_START
    
    
    def __repr__(self):
        """Returns the discovery category's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' name=',
            repr(self.name),
            ' id=',
            repr(self.id),
        ]
        
        if self.primary:
            repr_parts.append(' primary')
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    general = NotImplemented
    gaming = NotImplemented
    music = NotImplemented
    entertainment = NotImplemented
    creative_arts = NotImplemented
    science_and_tech = NotImplemented
    education = NotImplemented
    sports = NotImplemented
    fashion_and_beauty = NotImplemented
    relationships_and_identity = NotImplemented
    travel_and_food = NotImplemented
    fitness_and_health = NotImplemented
    finance = NotImplemented
    other = NotImplemented
    general_chatting = NotImplemented
    esports = NotImplemented
    anime_and_manga = NotImplemented
    movies_and_tv = NotImplemented
    books = NotImplemented
    art = NotImplemented
    writing = NotImplemented
    crafts_diy_and_making = NotImplemented
    programming = NotImplemented
    podcasts = NotImplemented
    tabletop_games = NotImplemented
    memes = NotImplemented
    news_and_current_events = NotImplemented
    cryptocurrency = NotImplemented
    investing = NotImplemented
    studying_and_teaching = NotImplemented
    lfg = NotImplemented
    customer_support = NotImplemented
    theorycraft = NotImplemented
    events = NotImplemented
    roleplay = NotImplemented
    content_creator = NotImplemented
    business = NotImplemented
    local_group = NotImplemented
    collaboration = NotImplemented
    fandom = NotImplemented
    wiki_and_guide = NotImplemented
    subreddit = NotImplemented
    emoji = NotImplemented
    comics_and_cartoons = NotImplemented
    mobile = NotImplemented
    console = NotImplemented
    charity_and_nonprofit = NotImplemented

DiscoveryCategory.general = DiscoveryCategory(0, 'General', True)
DiscoveryCategory.gaming = DiscoveryCategory(1, 'Gaming', True)
DiscoveryCategory.music = DiscoveryCategory(2, 'Music', True)
DiscoveryCategory.entertainment = DiscoveryCategory(3, 'Entertainment', True)
DiscoveryCategory.creative_arts = DiscoveryCategory(4, 'Creative Arts', True)
DiscoveryCategory.science_and_tech = DiscoveryCategory(5, 'Science & Tech', True)
DiscoveryCategory.education = DiscoveryCategory(6, 'Education', True)
DiscoveryCategory.sports = DiscoveryCategory(7, 'Sports', True)
DiscoveryCategory.fashion_and_beauty = DiscoveryCategory(8, 'Fashion & Beauty', True)
DiscoveryCategory.relationships_and_identity = DiscoveryCategory(9, 'Relationships & Identity', True)
DiscoveryCategory.travel_and_food = DiscoveryCategory(10, 'Travel & Food', True)
DiscoveryCategory.fitness_and_health = DiscoveryCategory(11, 'Fitness & Health', True)
DiscoveryCategory.finance = DiscoveryCategory(12, 'Finance', True)
DiscoveryCategory.other = DiscoveryCategory(13, 'Other', True)
DiscoveryCategory.general_chatting = DiscoveryCategory(14, 'General Chatting', True)
DiscoveryCategory.esports = DiscoveryCategory(15, 'Esports', False)
DiscoveryCategory.anime_and_manga = DiscoveryCategory(16, 'Anime & Manga', False)
DiscoveryCategory.movies_and_tv = DiscoveryCategory(17, 'Movies & TV', False)
DiscoveryCategory.books = DiscoveryCategory(18, 'Books', False)
DiscoveryCategory.art = DiscoveryCategory(19, 'Art', False)
DiscoveryCategory.writing = DiscoveryCategory(20, 'Writing', False)
DiscoveryCategory.crafts_diy_and_making = DiscoveryCategory(21, 'Crafts, DIY, & Making', False)
DiscoveryCategory.programming = DiscoveryCategory(22, 'Programming', False)
DiscoveryCategory.podcasts = DiscoveryCategory(23, 'Podcasts', False)
DiscoveryCategory.tabletop_games = DiscoveryCategory(24, 'Tabletop Games', False)
DiscoveryCategory.memes = DiscoveryCategory(25, 'Memes', False)
DiscoveryCategory.news_and_current_events = DiscoveryCategory(26, 'News & Current Events', False)
DiscoveryCategory.cryptocurrency = DiscoveryCategory(27, 'Cryptocurrency', False)
DiscoveryCategory.investing = DiscoveryCategory(28, 'Investing', False)
DiscoveryCategory.studying_and_teaching = DiscoveryCategory(29, 'Studying & Teaching', False)
DiscoveryCategory.lfg = DiscoveryCategory(30, 'LFG', False)
DiscoveryCategory.customer_support = DiscoveryCategory(31, 'Customer Support', False)
DiscoveryCategory.theorycraft = DiscoveryCategory(32, 'Theorycraft', False)
DiscoveryCategory.events = DiscoveryCategory(33, 'Events', False)
DiscoveryCategory.roleplay = DiscoveryCategory(34, 'Roleplay', False)
DiscoveryCategory.content_creator = DiscoveryCategory(35, 'Content Creator', False)
DiscoveryCategory.business = DiscoveryCategory(36, 'Business', False)
DiscoveryCategory.local_group = DiscoveryCategory(37, 'Local Group', False)
DiscoveryCategory.collaboration = DiscoveryCategory(38, 'Collaboration', False)
DiscoveryCategory.fandom = DiscoveryCategory(39, 'Fandom', False)
DiscoveryCategory.wiki_and_guide = DiscoveryCategory(40, 'Wiki & Guide', False)
DiscoveryCategory.subreddit = DiscoveryCategory(42, 'Subreddit', False)
DiscoveryCategory.emoji = DiscoveryCategory(43, 'Emoji', False)
DiscoveryCategory.comics_and_cartoons = DiscoveryCategory(44, 'Comics & Cartoons', False)
DiscoveryCategory.mobile = DiscoveryCategory(45, 'Mobile', False)
DiscoveryCategory.console = DiscoveryCategory(46, 'Console', False)
DiscoveryCategory.charity_and_nonprofit = DiscoveryCategory(47, 'Charity & Nonprofit', False)

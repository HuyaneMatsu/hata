__all__ = ('DiscoveryCategory',)

from scarletio import copy_docs

from ...bases import Preinstance as P, PreinstancedBase

from .fields import (
    parse_name, parse_name_localizations, parse_primary, parse_value, put_name, put_name_localizations,
    put_primary, put_value
)


class DiscoveryCategory(PreinstancedBase, value_type = int):
    """
    Represents a category of a ``GuildDiscovery``.
    
    Attributes
    ----------
    name : `str`
        The default name of the discovery category.
    
    name_localizations : ``None | dict<Locale, str>``
        The category's name in other languages.
    
    primary : `bool`
        Whether this category can be set as a guild's primary category.
    
    value : `int`
        The Discord side identifier value of the discovery category.
    
    Type Attributes
    ---------------
    Every predefined discovery category is also stored as a type attribute:
    
    +-------------------------------+-------+-------------------------------+-----------+
    | Type attribute name           | id    | name                          | primary   |
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
    """
    __slots__ = ('name_localizations', 'primary')
    
    def __new__(cls, value, name = None, primary = True):
        """
        Creates a new discovery category from the given parameters.
        
        Parameters
        ----------
        value : `int`
            The unique identifier number of the discovery category.
        
        name : `None | str` = `None`, Optional
            The category's name.
        
        primary : `bool` = `True`, Optional
            Whether this category can be set as a guild's primary category.
        """
        self = PreinstancedBase.__new__(cls, value, name)
        self.name_localizations = None
        self.primary = primary
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new discovery category from the given data. if the discovery category already
        exists returns that instead.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Discovery category data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        # Note that even tho id is received as integer, but integers over 32 bits are still received as string.
        category_id = parse_value(data)
        self = cls(category_id)
        self.primary = parse_primary(data)
        self.name = parse_name(data)
        # Only set `name_localizations` if it is non-`None`
        name_localizations = parse_name_localizations(data)
        if (name_localizations is not None):
            self.name_localizations = name_localizations
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Convert the discovery category to a json serializable dictionary.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_primary(self.primary, data, defaults)
        put_name(self.name, data, defaults)
        put_name_localizations(self.name_localizations, data, defaults)
        if include_internals:
            put_value(self.value, data, defaults)
        
        return data
    
    
    @copy_docs(PreinstancedBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        # primary
        primary = self.primary
        if primary:
            repr_parts.append(', primary = ')
            repr_parts.append(repr(primary))
    
    
    general = P(0, 'General', True)
    gaming = P(1, 'Gaming', True)
    music = P(2, 'Music', True)
    entertainment = P(3, 'Entertainment', True)
    creative_arts = P(4, 'Creative Arts', True)
    science_and_tech = P(5, 'Science & Tech', True)
    education = P(6, 'Education', True)
    sports = P(7, 'Sports', True)
    fashion_and_beauty = P(8, 'Fashion & Beauty', True)
    relationships_and_identity = P(9, 'Relationships & Identity', True)
    travel_and_food = P(10, 'Travel & Food', True)
    fitness_and_health = P(11, 'Fitness & Health', True)
    finance = P(12, 'Finance', True)
    other = P(13, 'Other', True)
    general_chatting = P(14, 'General Chatting', True)
    esports = P(15, 'Esports', False)
    anime_and_manga = P(16, 'Anime & Manga', False)
    movies_and_tv = P(17, 'Movies & TV', False)
    books = P(18, 'Books', False)
    art = P(19, 'Art', False)
    writing = P(20, 'Writing', False)
    crafts_diy_and_making = P(21, 'Crafts, DIY, & Making', False)
    programming = P(22, 'Programming', False)
    podcasts = P(23, 'Podcasts', False)
    tabletop_games = P(24, 'Tabletop Games', False)
    memes = P(25, 'Memes', False)
    news_and_current_events = P(26, 'News & Current Events', False)
    cryptocurrency = P(27, 'Cryptocurrency', False)
    investing = P(28, 'Investing', False)
    studying_and_teaching = P(29, 'Studying & Teaching', False)
    lfg = P(30, 'LFG', False)
    customer_support = P(31, 'Customer Support', False)
    theorycraft = P(32, 'Theorycraft', False)
    events = P(33, 'Events', False)
    roleplay = P(34, 'Roleplay', False)
    content_creator = P(35, 'Content Creator', False)
    business = P(36, 'Business', False)
    local_group = P(37, 'Local Group', False)
    collaboration = P(38, 'Collaboration', False)
    fandom = P(39, 'Fandom', False)
    wiki_and_guide = P(40, 'Wiki & Guide', False)
    subreddit = P(42, 'Subreddit', False)
    emoji = P(43, 'Emoji', False)
    comics_and_cartoons = P(44, 'Comics & Cartoons', False)
    mobile = P(45, 'Mobile', False)
    console = P(46, 'Console', False)
    charity_and_nonprofit = P(47, 'Charity & Nonprofit', False)

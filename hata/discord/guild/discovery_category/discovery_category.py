__all__ = ('DiscoveryCategory',)

import warnings

from ...bases import Preinstance as P, PreinstancedBase

from .fields import (
    parse_name, parse_name_localizations, parse_primary, parse_value, put_name_into, put_name_localizations_into,
    put_primary_into, put_value_into
)


class DiscoveryCategory(PreinstancedBase):
    """
    Represents a category of a ``GuildDiscovery``.
    
    Attributes
    ----------
    value : `int`
        The Discord side identifier value of the discovery category.
    name : `str`
        The default name of the discovery category.
    name_localizations : `None`, `dict` of (``Locale``, `str`) items
        The category's name in other languages.
    primary : `bool`
        Whether this category can be set as a guild's primary category.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``DiscoveryCategory``) items
        Stores the predefined discovery categories. This container is accessed when translating a Discord side
        identifier of a discovery category. The identifier value is used as a key to get it's wrapper side
        representation.
    VALUE_TYPE : `type` = `str`
        The discovery categories' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the discovery categories.
    
    Every predefined discovery category is also stored as a class attribute:
    
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
    """
    __slots__ = ('name_localizations', 'primary')
    
    INSTANCES = {}
    VALUE_TYPE = int
    
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new discovery category with the given value.
        
        Parameters
        ----------
        value : `int`
            The discovery category's identifier value.
        
        Returns
        -------
        self : `instance<cls>`
            The created instance.
        """
        self = object.__new__(cls)
        self.name = cls.DEFAULT_NAME
        self.value = value
        self.name_localizations = None
        self.primary = True
        
        return self
    
    
    def __init__(self, value, name, primary):
        """
        Creates a new discovery category from the given parameters.
        
        Parameters
        ----------
        value : `int`
            The unique identifier number of the discovery category.
        name : `str`
            The category's name.
        primary : `bool`
            Whether this category can be set as a guild's primary category.
        """
        self.value = value
        self.name = name
        self.name_localizations = None
        self.primary = primary
        
        self.INSTANCES[value] = self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new discovery category from the given data. if the discovery category already
        exists returns that instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Discovery category data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        # Note that even tho id is received as integer, but integers over 32 bits are still received as string.
        category_id = parse_value(data)
        self = cls.get(category_id)
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
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_primary_into(self.primary, data, defaults)
        put_name_into(self.name, data, defaults)
        put_name_localizations_into(self.name_localizations, data, defaults)
        if include_internals:
            put_value_into(self.value, data, defaults)
        
        return data
    
    
    def __repr__(self):
        """Returns the discovery category's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' name = ',
            repr(self.name),
            ' value = ',
            repr(self.value),
        ]
        
        if self.primary:
            repr_parts.append(' (primary)')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def id(self):
        """
        Deprecated and will be removed in 2023 Mar. Please use ``.value`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.id` is deprecated and will be removed in 2023 Mar. '
                f'Please use `.value` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
    
    
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

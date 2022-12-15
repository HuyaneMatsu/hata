__all__ = ('GuildDiscovery', )

from scarletio import RichAttributeErrorBaseType

from ..discovery_category import DiscoveryCategory

from .fields import (
    parse_application_actioned, parse_application_requested, parse_emoji_discovery, parse_keywords,
    parse_primary_category, parse_sub_categories, put_application_actioned_into, put_application_requested_into,
    put_emoji_discovery_into, put_keywords_into, put_primary_category_into, put_sub_categories_into,
    validate_application_actioned, validate_application_requested, validate_emoji_discovery, validate_keywords,
    validate_primary_category, validate_sub_categories
)


class GuildDiscovery(RichAttributeErrorBaseType):
    """
    Represent a guild's Discovery settings.
    
    Attributes
    ----------
    application_actioned : `None`, `datetime`
        When the guild's application was accepted or rejected.
    application_requested : `None`, `datetime`
        When the guild applied to guild discovery. Only set if pending.
    emoji_discovery : `bool`
        Whether guild info is shown when the respective guild's emojis are clicked.
    keywords : `None`, `tuple` of `str`
        The set discovery search keywords for the guild.
    primary_category : ``DiscoveryCategory``
        The primary discovery category of the guild.
    sub_categories : `None`, `tuple` of ``DiscoveryCategory``
        Guild Discovery sub-categories. Up to 5.
    """
    __slots__ = (
        'application_actioned', 'application_requested', 'emoji_discovery', 'keywords', 'primary_category',
        'sub_categories'
    )
    
    def __new__(
        cls,
        *,
        application_actioned = ...,
        application_requested = ...,
        emoji_discovery = ...,
        keywords = ...,
        primary_category = ...,
        sub_categories = ...,
    ):
        """
        Creates a new guild discovery from the given fields.
        
        Parameters
        ----------
        application_actioned : `None`, `datetime`, Optional (Keyword only)
            When the guild's application was accepted or rejected.
        application_requested : `None`, `datetime`, Optional (Keyword only)
            When the guild applied to guild discovery. Only set if pending.
        emoji_discovery : `bool`, Optional (Keyword only)
            Whether guild info is shown when the respective guild's emojis are clicked.
        keywords : `None`, `iterable` of `str`, Optional (Keyword only)
            The set discovery search keywords for the guild.
        primary_category : ``DiscoveryCategory``, `int`, Optional (Keyword only)
            The primary discovery category of the guild.
        sub_categories : `None`, `iterable` of (`int`, ``DiscoveryCategory``), Optional (Keyword only)
            Guild Discovery sub-categories.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # application_actioned
        if application_actioned is ...:
            application_actioned = None
        else:
            application_actioned = validate_application_actioned(application_actioned)
        
        # application_requested
        if application_requested is ...:
            application_requested = None
        else:
            application_requested = validate_application_requested(application_requested)
        
        # emoji_discovery
        if emoji_discovery is ...:
            emoji_discovery = False
        else:
            emoji_discovery = validate_emoji_discovery(emoji_discovery)
        
        # keywords
        if keywords is ...:
            keywords = None
        else:
            keywords = validate_keywords(keywords)
        
        # primary_category
        if primary_category is ...:
            primary_category = DiscoveryCategory.general
        else:
            primary_category = validate_primary_category(primary_category)
        
        # sub_categories
        if sub_categories is ...:
            sub_categories = None
        else:
            sub_categories = validate_sub_categories(sub_categories)
        
        # Construct object
        
        self = object.__new__(cls)
        self.application_actioned = application_actioned
        self.application_requested = application_requested
        self.emoji_discovery = emoji_discovery
        self.keywords = keywords
        self.primary_category = primary_category
        self.sub_categories = sub_categories
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new guild discovery object from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Guild discovery data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.application_actioned = parse_application_actioned(data)
        self.application_requested = parse_application_requested(data)
        self.emoji_discovery = parse_emoji_discovery(data)
        self.keywords = parse_keywords(data)
        self.primary_category = parse_primary_category(data)
        self.sub_categories = parse_sub_categories(data)
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the guild discovery to a json serializable object.
        
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
        
        if include_internals:
            put_application_actioned_into(self.application_actioned, data, defaults)
            put_application_requested_into(self.application_requested, data, defaults)
        
        put_emoji_discovery_into(self.emoji_discovery, data, defaults)
        put_keywords_into(self.keywords, data, defaults)
        put_primary_category_into(self.primary_category, data, defaults)
        put_sub_categories_into(self.sub_categories, data, defaults)
        
        return data
    
    
    def __eq__(self, other):
        """Returns whether the two guild discoveries are the same."""
        if (type(self) is not type(other)):
            return NotImplemented
        
        # application_actioned
        if (self.application_actioned != other.application_actioned):
            return False
        
        # application_requested
        if (self.application_requested != other.application_requested):
            return False
        
        # emoji_discovery
        if (self.emoji_discovery != other.emoji_discovery):
            return False
        
        # keywords
        if (self.keywords != other.keywords):
            return False
        
        # primary_category
        if (self.primary_category is not other.primary_category):
            return False
        
        # sub_categories
        if (self.sub_categories != other.sub_categories):
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the guild discovery's hash value."""
        hash_value = 0
        
        # application_actioned
        application_actioned = self.application_actioned
        if (application_actioned is not None):
            hash_value ^= hash(application_actioned)
        
        # application_requested
        application_requested = self.application_requested
        if (application_requested is not None):
            hash_value ^= hash(application_requested)
        
        # emoji_discovery
        emoji_discovery = self.emoji_discovery
        if (emoji_discovery is not None):
            hash_value ^= emoji_discovery
        
        # keywords
        keywords = self.keywords
        if (keywords is not None):
            hash_value ^= len(keywords) << 1
            
            for keyword in keywords:
                hash_value ^= hash(keyword)
        
        # primary_category
        hash_value ^= self.primary_category.value << 5
        
        # sub_categories
        sub_categories = self.sub_categories
        if (sub_categories is not None):
            hash_value ^= len(sub_categories) << 9
            
            shift = 13
            
            for sub_category in sub_categories:
                hash_value ^= sub_category.value << shift
                shift += 4
        
        return hash_value
    
    
    def __repr__(self):
        """Returns the guild discovery's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        field_added = False
        
        # application_actioned
        application_actioned = self.application_actioned
        if (application_actioned is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' application_actioned = ')
            repr_parts.append(repr(application_actioned))
        
        # application_requested
        application_requested = self.application_requested
        if (application_requested is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' application_requested = ')
            repr_parts.append(repr(application_requested))
        
        # emoji_discovery
        emoji_discovery = self.emoji_discovery
        if emoji_discovery:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' emoji_discovery = ')
            repr_parts.append(repr(emoji_discovery))
        
        # keywords
        keywords = self.keywords
        if (keywords is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' keywords = [')
            
            index = 0
            length = len(keywords)
            
            while True:
                keyword = keywords[index]
                repr_parts.append(repr(keyword))
                
                index += 1
                if index == length:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        # primary_category
        primary_category = self.primary_category
        if (primary_category is not DiscoveryCategory.general):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' primary_category = ')
            repr_parts.append(repr(primary_category.name))
            repr_parts.append(' ~ ')
            repr_parts.append(repr(primary_category.value))
        
        # sub_categories
        sub_categories = self.sub_categories
        if (sub_categories is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' sub_categories = [')
            
            index = 0
            length = len(sub_categories)
            
            while True:
                sub_category = sub_categories[index]
                repr_parts.append(repr(sub_category.name))
                repr_parts.append(' ~ ')
                repr_parts.append(repr(sub_category.value))
                
                index += 1
                if index == length:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
            
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def copy(self):
        """
        Copies the guild discovery.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.application_actioned = self.application_actioned
        new.application_requested = self.application_requested
        new.emoji_discovery = self.emoji_discovery
        keywords = self.keywords
        if (keywords is not None):
            keywords = (*keywords,)
        new.keywords = keywords
        new.primary_category = self.primary_category
        sub_categories = self.sub_categories
        if (sub_categories is not None):
            sub_categories = (*sub_categories,)
        new.sub_categories = sub_categories
        return new
    
    
    def copy_with(
        self,
        *,
        application_actioned = ...,
        application_requested = ...,
        emoji_discovery = ...,
        keywords = ...,
        primary_category = ...,
        sub_categories = ...,
    ):
        """
        Copies the guild discovery with the given fields.
        
        Parameters
        ----------
        application_actioned : `None`, `datetime`, Optional (Keyword only)
            When the guild's application was accepted or rejected.
        application_requested : `None`, `datetime`, Optional (Keyword only)
            When the guild applied to guild discovery. Only set if pending.
        emoji_discovery : `bool`, Optional (Keyword only)
            Whether guild info is shown when the respective guild's emojis are clicked.
        keywords : `None`, `iterable` of `str`, Optional (Keyword only)
            The set discovery search keywords for the guild.
        primary_category : ``DiscoveryCategory``, `int`, Optional (Keyword only)
            The primary discovery category of the guild.
        sub_categories : `None`, `iterable` of (`int`, ``DiscoveryCategory``), Optional (Keyword only)
            Guild Discovery sub-categories.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # application_actioned
        if application_actioned is ...:
            application_actioned = self.application_actioned
        else:
            application_actioned = validate_application_actioned(application_actioned)
        
        # application_requested
        if application_requested is ...:
            application_requested = self.application_requested
        else:
            application_requested = validate_application_requested(application_requested)
        
        # emoji_discovery
        if emoji_discovery is ...:
            emoji_discovery = self.emoji_discovery
        else:
            emoji_discovery = validate_emoji_discovery(emoji_discovery)
        
        # keywords
        if keywords is ...:
            keywords = self.keywords
            if (keywords is not None):
                keywords = (*keywords,)
        else:
            keywords = validate_keywords(keywords)
        
        # primary_category
        if primary_category is ...:
            primary_category = self.primary_category
        else:
            primary_category = validate_primary_category(primary_category)
        
        # sub_categories
        if sub_categories is ...:
            sub_categories = self.sub_categories
            if (sub_categories is not None):
                sub_categories = (*sub_categories,)
        else:
            sub_categories = validate_sub_categories(sub_categories)
        
        # Construct object
        
        new = object.__new__(type(self))
        new.application_actioned = application_actioned
        new.application_requested = application_requested
        new.emoji_discovery = emoji_discovery
        new.keywords = keywords
        new.primary_category = primary_category
        new.sub_categories = sub_categories
        return new
    
    
    def iter_keywords(self):
        """
        Iterates over the keywords of the guild discovery.
        
        This method is an iterable generator.
        
        Yields
        ------
        keyword : `str`
        """
        keywords = self.keywords
        if (keywords is not None):
            yield from keywords
    
    
    def iter_sub_categories(self):
        """
        Iterates over the sub-categories of the guild discovery.
        
        This method is an iterable generator.
        
        Yields
        ------
        sub_category : ``DiscoveryCategory``
        """
        sub_categories = self.sub_categories
        if (sub_categories is not None):
            yield from sub_categories

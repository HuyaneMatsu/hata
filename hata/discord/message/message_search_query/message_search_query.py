__all__ = ('MessageSearchQuery',)

from scarletio import RichAttributeErrorBaseType

from ...utils import DATETIME_FORMAT_CODE

from .constants import LIMIT_DEFAULT, OFFSET_DEFAULT, SLOP_DEFAULT
from .fields import (
    parse_after, parse_attachment_extensions, parse_attachment_names, parse_author_ids, parse_author_types,
    parse_before, parse_channel_ids, parse_content, parse_embed_providers, parse_embed_types, parse_has_types,
    parse_include_nsfw_channels, parse_limit, parse_mentioned_everyone, parse_mentioned_user_ids, parse_offset,
    parse_pinned, parse_slop, parse_sort_by, parse_sort_order, parse_url_host_names, put_after,
    put_attachment_extensions, put_attachment_names, put_author_ids, put_author_types, put_before, put_channel_ids,
    put_content, put_embed_providers, put_embed_types, put_has_types, put_include_nsfw_channels, put_limit,
    put_mentioned_everyone, put_mentioned_user_ids, put_offset, put_pinned, put_slop, put_sort_by, put_sort_order,
    put_url_host_names, validate_after, validate_attachment_extensions, validate_attachment_names, validate_author_ids,
    validate_author_types, validate_before, validate_channel_ids, validate_content, validate_embed_providers,
    validate_embed_types, validate_has_types, validate_include_nsfw_channels, validate_limit,
    validate_mentioned_everyone, validate_mentioned_user_ids, validate_offset, validate_pinned, validate_slop,
    validate_sort_by, validate_sort_order, validate_url_host_names
)
from .preinstanced import MessageSearchSortByType, MessageSearchSortOrderType


SERIALISATION_SHIFT_AFTER = 0
SERIALISATION_SHIFT_ATTACHMENT_EXTENSIONS = 1
SERIALISATION_SHIFT_ATTACHMENT_NAMES = 2
SERIALISATION_SHIFT_AUTHOR_IDS = 3
SERIALISATION_SHIFT_AUTHOR_TYPES = 4
SERIALISATION_SHIFT_BEFORE = 5
SERIALISATION_SHIFT_CHANNEL_IDS = 6
SERIALISATION_SHIFT_CONTENT = 7
SERIALISATION_SHIFT_EMBED_PROVIDERS = 8
SERIALISATION_SHIFT_EMBED_TYPES = 9
SERIALISATION_SHIFT_HAS_TYPES = 10
SERIALISATION_SHIFT_INCLUDE_NSFW_CHANNELS = 11
SERIALISATION_SHIFT_LIMIT = 12
SERIALISATION_SHIFT_MENTIONED_EVERYONE = 13
SERIALISATION_SHIFT_MENTIONED_USER_IDS = 14
SERIALISATION_SHIFT_OFFSET = 15
SERIALISATION_SHIFT_PINNED = 16
SERIALISATION_SHIFT_SLOP = 17
SERIALISATION_SHIFT_SORT_BY = 18
SERIALISATION_SHIFT_SORT_ORDER = 19
SERIALISATION_SHIFT_URL_HOST_NAMES = 20


class MessageSearchQuery(RichAttributeErrorBaseType):
    """
    Message search query.
    
    Attributes
    ----------
    _serialisation_flags : `int`
        Flags used internally to know what to force serialise.
    
    after : `None | DateTime`
        Message creation time lower threshold.
    
    attachment_extensions : `None | tuple<str>`
        Whether the returned messages should have attachments with these extensions.
    
    attachment_names : `None | tuple<str>`
        Whether the returned messages should have attachments with these names.
    
    author_ids : `None | tuple<int>`
        Whether the returned messages should be created by these users defined by their identifiers.
    
    author_types : ``None | tuple<MessageSearchAuthorType>``
        Whether the returned messages should be created by these type of users.
    
    before : `None | DateTime`
        Message creation time upper threshold.
    
    channel_ids : `None | tuple<int>`
        Whether the returned messages should be created in these channels defined by their identifiers.
    
    content : `None | str`
        Content to search in the messages.
    
    embed_providers : `None | tuple<str>`
        Whether the returned messages should have embeds with these providers.
    
    embed_types : ``None | tuple<EmbedType>``
        Whether the returned messages should have embeds with these types.
    
    has_types : ``None | tuple<MessageSearchHasType>``
        What type of content should the returned messages have.
    
    include_nsfw_channels : `bool`
        Whether to include nsfw channels in the search.
    
    limit : `int`
        The amount of messages to return.
    
    mentioned_everyone : `bool`
        Whether the returned messages should be mentioning everyone.
    
    mentioned_user_ids : `None | tuple<int>`
        Whether the returned messages should be mentioned these users by their identifiers.
    
    offset : `int`
        Amount to offset the returned messages by.
    
    pinned : `bool`
        Whether the returned messages should be pinned.
    
    slop : `int`
        The maximal amount of words that can be in between each word from `content`.
    
    sort_by : ``MessageSearchSortByType``
        By what to sort the returned messages.
    
    sort_order : ``MessageSearchSortOrderType``
        How to order the returned messages. Depending on the `sort_by`, this field may not be respected.
    
    url_host_names : `None | tuple<str>`
        Whether the returned messages should contain urls with these host names.
    """
    __slots__ = (
        '_serialisation_flags', 'after', 'attachment_extensions', 'attachment_names', 'author_ids', 'author_types',
        'before', 'channel_ids', 'content', 'embed_providers', 'embed_types', 'has_types', 'include_nsfw_channels',
        'limit', 'mentioned_everyone', 'mentioned_user_ids', 'offset', 'pinned', 'slop', 'sort_by', 'sort_order',
        'url_host_names'
    )
    
    
    def __new__(
        cls,
        *,
        after = ...,
        attachment_extensions = ...,
        attachment_names = ...,
        author_ids = ...,
        author_types = ...,
        before = ...,
        channel_ids = ...,
        content = ...,
        embed_providers = ...,
        embed_types = ...,
        has_types = ...,
        include_nsfw_channels = ...,
        limit = ...,
        mentioned_everyone = ...,
        mentioned_user_ids = ...,
        offset = ...,
        pinned = ...,
        slop = ...,
        sort_by = ...,
        sort_order = ...,
        url_host_names = ...,
    ):
        """
        Creates a new messages search query.
        
        Parameters
        ----------
        after : `None | DateTime`, Optional (Keyword only)
            Message creation time lower threshold.
        
        attachment_extensions : `None | str | iterable<str>`, Optional (Keyword only)
            Whether the returned messages should have attachments with these extensions.
        
        attachment_names : `None | str | iterable<str>`, Optional (Keyword only)
            Whether the returned messages should have attachments with these names.
        
        author_ids : ``None | int | iterable<int> | UserBase | iterable<UserBase>``, Optional (Keyword only)
            Whether the returned messages should be created by these users defined by their identifiers.
        
        author_types : ``None | str | iterable<str> | MessageSearchAuthorType | iterable<MessageSearchAuthorType>`` \
                , Optional (Keyword only)
            Whether the returned messages should be created by these type of users.
        
        before : `None | DateTime`, Optional (Keyword only)
            Message creation time upper threshold.
        
        channel_ids : ``None | int | iterable<int> | Channel | iterable<Channel>``, Optional (Keyword only)
            Whether the returned messages should be created in these channels defined by their identifiers.
        
        content : `None | str`, Optional (Keyword only)
            Content to search in the messages.
        
        embed_providers : `None | str | iterable<str>`, Optional (Keyword only)
            Whether the returned messages should have embeds with these providers.
        
        embed_types : ``None | str | iterable<str> | EmbedType | iterable<EmbedType>``, Optional (Keyword only)
            Whether the returned messages should have embeds with these types.
        
        has_types : ``None | str | iterable<str> | MessageSearchHasType | iterable<MessageSearchHasType>`` \
                , Optional (Keyword only)
            What type of content should the returned messages have.
        
        include_nsfw_channels : `None | bool`, Optional (Keyword only)
            Whether to include nsfw channels in the search.
        
        limit : `None | int`, Optional (Keyword only)
            The amount of messages to return.
        
        mentioned_everyone : `None | bool`, Optional (Keyword only)
            Whether the returned messages should be mentioning everyone.
        
        mentioned_user_ids : ``None | int | iterable<int> | ClientUserBase | iterable<ClientUserBase>`` \
                , Optional (Keyword only)
            Whether the returned messages should be mentioned these users by their identifiers.
        
        offset : `None | int`, Optional (Keyword only)
            Amount to offset the returned messages by.
        
        pinned : `None | bool`, Optional (Keyword only)
            Whether the returned messages should be pinned.
        
        slop : `None | int`, Optional (Keyword only)
            The maximal amount of words that can be in between each word from `content`.
        
        sort_by : ``None | str | MessageSearchSortByType``, Optional (Keyword only)
            By what to sort the returned messages.
        
        sort_order : ``None | str | MessageSearchSortOrderType``, Optional (Keyword only)
            How to order the returned messages. Depending on the `sort_by`, this field may not be respected.
        
        url_host_names : `None | str | iterable<str>`, Optional (Keyword only)
            Whether the returned messages should contain urls with these host names.
        
        Raises
        ------
        ValueError
            - If a parameter's value is incorrect.
        TypeError
            - If a parameter's type is incorrect.
        """
        serialisation_flags = 0
        
        # after
        if (after is ...):
            after = None
        else:
            after = validate_after(after)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_AFTER)
        
        # attachment_extensions
        if (attachment_extensions is ...):
            attachment_extensions = None
        else:
            attachment_extensions = validate_attachment_extensions(attachment_extensions)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_ATTACHMENT_EXTENSIONS)
        
        # attachment_names
        if (attachment_names is ...):
            attachment_names = None
        else:
            attachment_names = validate_attachment_names(attachment_names)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_ATTACHMENT_NAMES)
        
        # author_ids
        if (author_ids is ...):
            author_ids = None
        else:
            author_ids = validate_author_ids(author_ids)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_AUTHOR_IDS)
        
        # author_types
        if (author_types is ...):
            author_types = None
        else:
            author_types = validate_author_types(author_types)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_AUTHOR_TYPES)
        
        # before
        if (before is ...):
            before = None
        else:
            before = validate_before(before)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_BEFORE)
        
        # channel_ids
        if (channel_ids is ...):
            channel_ids = None
        else:
            channel_ids = validate_channel_ids(channel_ids)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_CHANNEL_IDS)
        
        # content
        if (content is ...):
            content = None
        else:
            content = validate_content(content)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_CONTENT)
        
        # embed_providers
        if (embed_providers is ...):
            embed_providers = None
        else:
            embed_providers = validate_embed_providers(embed_providers)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_EMBED_PROVIDERS)
        
        # embed_types
        if (embed_types is ...):
            embed_types = None
        else:
            embed_types = validate_embed_types(embed_types)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_EMBED_TYPES)
        
        # has_types
        if (has_types is ...):
            has_types = None
        else:
            has_types = validate_has_types(has_types)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_HAS_TYPES)
        
        # include_nsfw_channels
        if (include_nsfw_channels is ...):
            include_nsfw_channels = False
        else:
            include_nsfw_channels = validate_include_nsfw_channels(include_nsfw_channels)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_INCLUDE_NSFW_CHANNELS)
        
        # limit
        if (limit is ...):
            limit = LIMIT_DEFAULT
        else:
            limit = validate_limit(limit)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_LIMIT)
        
        # mentioned_everyone
        if (mentioned_everyone is ...):
            mentioned_everyone = False
        else:
            mentioned_everyone = validate_mentioned_everyone(mentioned_everyone)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_MENTIONED_EVERYONE)
        
        # mentioned_user_ids
        if (mentioned_user_ids is ...):
            mentioned_user_ids = None
        else:
            mentioned_user_ids = validate_mentioned_user_ids(mentioned_user_ids)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_MENTIONED_USER_IDS)
        
        # offset
        if (offset is ...):
            offset = OFFSET_DEFAULT
        else:
            offset = validate_offset(offset)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_OFFSET)
        
        # pinned
        if (pinned is ...):
            pinned = False
        else:
            pinned = validate_pinned(pinned)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_PINNED)
        
        # slop
        if (slop is ...):
            slop = SLOP_DEFAULT
        else:
            slop = validate_slop(slop)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_SLOP)
        
        # sort_by
        if (sort_by is ...):
            sort_by = MessageSearchSortByType.creation
        else:
            sort_by = validate_sort_by(sort_by)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_SORT_BY)
        
        # sort_order
        if (sort_order is ...):
            sort_order = MessageSearchSortOrderType.descending
        else:
            sort_order = validate_sort_order(sort_order)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_SORT_ORDER)
        
        # url_host_names
        if (url_host_names is ...):
            url_host_names = None
        else:
            url_host_names = validate_url_host_names(url_host_names)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_URL_HOST_NAMES)
        
        # Creation
        self = object.__new__(cls)
        self._serialisation_flags = serialisation_flags
        self.after = after
        self.attachment_extensions = attachment_extensions
        self.attachment_names = attachment_names
        self.author_ids = author_ids
        self.author_types = author_types
        self.before = before
        self.channel_ids = channel_ids
        self.content = content
        self.embed_providers = embed_providers
        self.embed_types = embed_types
        self.has_types = has_types
        self.include_nsfw_channels = include_nsfw_channels
        self.limit = limit
        self.mentioned_everyone = mentioned_everyone
        self.mentioned_user_ids = mentioned_user_ids
        self.offset = offset
        self.pinned = pinned
        self.slop = slop
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.url_host_names = url_host_names
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        serialisation_flags = self._serialisation_flags
        field_added = False
        
        repr_parts = ['<', type(self).__name__]
        
        # after
        if (serialisation_flags >> SERIALISATION_SHIFT_AFTER) & 1:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' after = ')
            after = self.after
            repr_parts.append(repr(None) if after is None else format(after, DATETIME_FORMAT_CODE))
        
        # attachment_extensions
        if (serialisation_flags >> SERIALISATION_SHIFT_ATTACHMENT_EXTENSIONS) & 1:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' attachment_extensions = ')
            repr_parts.append(repr(self.attachment_extensions))
        
        # attachment_names
        if (serialisation_flags >> SERIALISATION_SHIFT_ATTACHMENT_NAMES) & 1:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' attachment_names = ')
            repr_parts.append(repr(self.attachment_names))
        
        # author_ids
        if (serialisation_flags >> SERIALISATION_SHIFT_AUTHOR_IDS) & 1:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' author_ids = ')
            repr_parts.append(repr(self.author_ids))
        
        # author_types
        if (serialisation_flags >> SERIALISATION_SHIFT_AUTHOR_TYPES) & 1:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' author_types = ')
            repr_parts.append(repr(self.author_types))
        
        # before
        if (serialisation_flags >> SERIALISATION_SHIFT_BEFORE) & 1:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' before = ')
            before = self.before
            repr_parts.append(repr(None) if before is None else format(before, DATETIME_FORMAT_CODE))
        
        # channel_ids
        if (serialisation_flags >> SERIALISATION_SHIFT_CHANNEL_IDS) & 1:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' channel_ids = ')
            repr_parts.append(repr(self.channel_ids))
        
        # content
        if (serialisation_flags >> SERIALISATION_SHIFT_CONTENT) & 1:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' content = ')
            repr_parts.append(repr(self.content))
        
        # embed_providers
        if (serialisation_flags >> SERIALISATION_SHIFT_EMBED_PROVIDERS) & 1:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' embed_providers = ')
            repr_parts.append(repr(self.embed_providers))
        
        # embed_types
        if (serialisation_flags >> SERIALISATION_SHIFT_EMBED_TYPES) & 1:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' embed_types = ')
            repr_parts.append(repr(self.embed_types))
        
        # has_types
        if (serialisation_flags >> SERIALISATION_SHIFT_HAS_TYPES) & 1:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' has_types = ')
            repr_parts.append(repr(self.has_types))
        
        # include_nsfw_channels
        if (serialisation_flags >> SERIALISATION_SHIFT_INCLUDE_NSFW_CHANNELS) & 1:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' include_nsfw_channels = ')
            repr_parts.append(repr(self.include_nsfw_channels))
        
        # limit
        if (serialisation_flags >> SERIALISATION_SHIFT_LIMIT) & 1:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' limit = ')
            repr_parts.append(repr(self.limit))
        
        # mentioned_everyone
        if (serialisation_flags >> SERIALISATION_SHIFT_MENTIONED_EVERYONE) & 1:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' mentioned_everyone = ')
            repr_parts.append(repr(self.mentioned_everyone))
        
        # mentioned_user_ids
        if (serialisation_flags >> SERIALISATION_SHIFT_MENTIONED_USER_IDS) & 1:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' mentioned_user_ids = ')
            repr_parts.append(repr(self.mentioned_user_ids))
        
        # offset
        if (serialisation_flags >> SERIALISATION_SHIFT_OFFSET) & 1:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' offset = ')
            repr_parts.append(repr(self.offset))
        
        # pinned
        if (serialisation_flags >> SERIALISATION_SHIFT_PINNED) & 1:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' pinned = ')
            repr_parts.append(repr(self.pinned))
        
        # slop
        if (serialisation_flags >> SERIALISATION_SHIFT_SLOP) & 1:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' slop = ')
            repr_parts.append(repr(self.slop))
        
        # sort_by
        if (serialisation_flags >> SERIALISATION_SHIFT_SORT_BY) & 1:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' sort_by = ')
            repr_parts.append(repr(self.sort_by))
        
        # sort_order
        if (serialisation_flags >> SERIALISATION_SHIFT_SORT_ORDER) & 1:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' sort_order = ')
            repr_parts.append(repr(self.sort_order))
        
        # url_host_names
        if (serialisation_flags >> SERIALISATION_SHIFT_URL_HOST_NAMES) & 1:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' url_host_names = ')
            repr_parts.append(repr(self.url_host_names))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = self._serialisation_flags
        
        # after
        after = self.after
        if (after is not None):
            hash_value ^= hash(after)
        
        # attachment_extensions
        attachment_extensions = self.attachment_extensions
        if (attachment_extensions is not None):
            hash_value ^= hash(attachment_extensions)
        
        # attachment_names
        attachment_names = self.attachment_names
        if (attachment_names is not None):
            hash_value ^= hash(attachment_names)
        
        # author_ids
        author_ids = self.author_ids
        if (author_ids is not None):
            hash_value ^= hash(author_ids)
        
        # author_types
        author_types = self.author_types
        if (author_types is not None):
            hash_value ^= hash(author_types)
        
        # before
        before = self.before
        if (before is not None):
            hash_value ^= hash(before)
        
        # channel_ids
        channel_ids = self.channel_ids
        if (channel_ids is not None):
            hash_value ^= hash(channel_ids)
        
        # content
        content = self.content
        if (content is not None):
            hash_value ^= hash(content)
        
        # embed_providers
        embed_providers = self.embed_providers
        if (embed_providers is not None):
            hash_value ^= hash(embed_providers)
        
        # embed_types
        embed_types = self.embed_types
        if (embed_types is not None):
            hash_value ^= hash(embed_types)
        
        # has_types
        has_types = self.has_types
        if (has_types is not None):
            hash_value ^= hash(has_types)
        
        # include_nsfw_channels
        hash_value ^= self.include_nsfw_channels << 32
        
        # limit
        hash_value ^= self.limit << 33
        
        # mentioned_everyone
        hash_value ^= self.mentioned_everyone << 35
        
        # mentioned_user_ids
        mentioned_user_ids = self.mentioned_user_ids
        if (mentioned_user_ids is not None):
            hash_value ^= hash(mentioned_user_ids)
        
        # offset
        hash_value ^= self.offset << 36
        
        # pinned
        hash_value ^= self.pinned << 41
        
        # slop
        hash_value ^= self.slop << 42
        
        # sort_by
        hash_value ^= hash(self.sort_by)
        
        # sort_order
        hash_value ^= hash(self.sort_order)
        
        # url_host_names
        url_host_names = self.url_host_names
        if (url_host_names is not None):
            hash_value ^= hash(url_host_names)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # _serialisation_flags
        if self._serialisation_flags != other._serialisation_flags:
            return False
        
        # after
        if self.after != other.after:
            return False
        
        # attachment_extensions
        if self.attachment_extensions != other.attachment_extensions:
            return False
        
        # attachment_names
        if self.attachment_names != other.attachment_names:
            return False
        
        # author_ids
        if self.author_ids != other.author_ids:
            return False
        
        # author_types
        if self.author_types != other.author_types:
            return False
        
        # before
        if self.before != other.before:
            return False
        
        # channel_ids
        if self.channel_ids != other.channel_ids:
            return False
        
        # content
        if self.content != other.content:
            return False
        
        # embed_providers
        if self.embed_providers != other.embed_providers:
            return False
        
        # embed_types
        if self.embed_types != other.embed_types:
            return False
        
        # has_types
        if self.has_types != other.has_types:
            return False
        
        # include_nsfw_channels
        if self.include_nsfw_channels != other.include_nsfw_channels:
            return False
        
        # limit
        if self.limit != other.limit:
            return False
        
        # mentioned_everyone
        if self.mentioned_everyone != other.mentioned_everyone:
            return False
        
        # mentioned_user_ids
        if self.mentioned_user_ids != other.mentioned_user_ids:
            return False
        
        # offset
        if self.offset != other.offset:
            return False
        
        # pinned
        if self.pinned != other.pinned:
            return False
        
        # slop
        if self.slop != other.slop:
            return False
        
        # sort_by
        if self.sort_by is not other.sort_by:
            return False
        
        # sort_order
        if self.sort_order is not other.sort_order:
            return False
        
        # url_host_names
        if self.url_host_names != other.url_host_names:
            return False
        
        return True
    
    
    def copy(self):
        """
        Copies the message search query.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new._serialisation_flags = self._serialisation_flags
        
        # after
        new.after = self.after
        
        # attachment_extensions
        attachment_extensions = self.attachment_extensions
        if (attachment_extensions is not None):
            attachment_extensions = (*attachment_extensions,)
        new.attachment_extensions = attachment_extensions
        
        # attachment_names
        attachment_names = self.attachment_names
        if (attachment_names is not None):
            attachment_names = (*attachment_names,)
        new.attachment_names = attachment_names
        
        # author_ids
        author_ids = self.author_ids
        if (author_ids is not None):
            author_ids = (*author_ids,)
        new.author_ids = author_ids
        
        # author_types
        author_types = self.author_types
        if (author_types is not None):
            author_types = (*author_types,)
        new.author_types = author_types
        
        # before
        new.before = self.before
        
        # channel_ids
        channel_ids = self.channel_ids
        if (channel_ids is not None):
            channel_ids = (*channel_ids,)
        new.channel_ids = channel_ids
        
        # content
        new.content = self.content
        
        # embed_providers
        embed_providers = self.embed_providers
        if (embed_providers is not None):
            embed_providers = (*embed_providers,)
        new.embed_providers = embed_providers
        
        # embed_types
        embed_types = self.embed_types
        if (embed_types is not None):
            embed_types = (*embed_types,)
        new.embed_types = embed_types
        
        # has_types
        has_types = self.has_types
        if (has_types is not None):
            has_types = (*has_types,)
        new.has_types = has_types
        
        # include_nsfw_channels
        new.include_nsfw_channels = self.include_nsfw_channels
        
        # limit
        new.limit = self.limit
        
        # mentioned_everyone
        new.mentioned_everyone = self.mentioned_everyone
        
        # mentioned_user_ids
        mentioned_user_ids = self.mentioned_user_ids
        if (mentioned_user_ids is not None):
            mentioned_user_ids = (*mentioned_user_ids,)
        new.mentioned_user_ids = mentioned_user_ids
        
        # offset
        new.offset = self.offset
        
        # pinned
        new.pinned = self.pinned
        
        # slop
        new.slop = self.slop
        
        # sort_by
        new.sort_by = self.sort_by
        
        # sort_order
        new.sort_order = self.sort_order
        
        # url_host_names
        url_host_names = self.url_host_names
        if (url_host_names is not None):
            url_host_names = (*url_host_names,)
        new.url_host_names = url_host_names
        
        return new
    
    
    def copy_with(
        self,
        *,
        after = ...,
        attachment_extensions = ...,
        attachment_names = ...,
        author_ids = ...,
        author_types = ...,
        before = ...,
        channel_ids = ...,
        content = ...,
        embed_providers = ...,
        embed_types = ...,
        has_types = ...,
        include_nsfw_channels = ...,
        limit = ...,
        mentioned_everyone = ...,
        mentioned_user_ids = ...,
        offset = ...,
        pinned = ...,
        slop = ...,
        sort_by = ...,
        sort_order = ...,
        url_host_names = ...,
    ):
        """
        Copies the message search query with the given fields.
        
        Parameters
        ----------
        after : `None | DateTime`, Optional (Keyword only)
            Message creation time lower threshold.
        
        attachment_extensions : `None | str | iterable<str>`, Optional (Keyword only)
            Whether the returned messages should have attachments with these extensions.
        
        attachment_names : `None | str | iterable<str>`, Optional (Keyword only)
            Whether the returned messages should have attachments with these names.
        
        author_ids : ``None | int | iterable<int> | UserBase | iterable<UserBase>``, Optional (Keyword only)
            Whether the returned messages should be created by these users defined by their identifiers.
        
        author_types : ``None | str | iterable<str> | MessageSearchAuthorType | iterable<MessageSearchAuthorType>`` \
                , Optional (Keyword only)
            Whether the returned messages should be created by these type of users.
        
        before : `None | DateTime`, Optional (Keyword only)
            Message creation time upper threshold.
        
        channel_ids : ``None | int | iterable<int> | Channel | iterable<Channel>``, Optional (Keyword only)
            Whether the returned messages should be created in these channels defined by their identifiers.
        
        content : `None | str`, Optional (Keyword only)
            Content to search in the messages.
        
        embed_providers : `None | str | iterable<str>`, Optional (Keyword only)
            Whether the returned messages should have embeds with these providers.
        
        embed_types : ``None | str | iterable<str> | EmbedType | iterable<EmbedType>``, Optional (Keyword only)
            Whether the returned messages should have embeds with these types.
        
        has_types : ``None | str | iterable<str> | MessageSearchHasType | iterable<MessageSearchHasType>`` \
                , Optional (Keyword only)
            What type of content should the returned messages have.
        
        include_nsfw_channels : `None | bool`, Optional (Keyword only)
            Whether to include nsfw channels in the search.
        
        limit : `None | int`, Optional (Keyword only)
            The amount of messages to return.
        
        mentioned_everyone : `None | bool`, Optional (Keyword only)
            Whether the returned messages should be mentioning everyone.
        
        mentioned_user_ids : ``None | int | iterable<int> | ClientUserBase | iterable<ClientUserBase>`` \
                , Optional (Keyword only)
            Whether the returned messages should be mentioned these users by their identifiers.
        
        offset : `None | int`, Optional (Keyword only)
            Amount to offset the returned messages by.
        
        pinned : `None | bool`, Optional (Keyword only)
            Whether the returned messages should be pinned.
        
        slop : `None | int`, Optional (Keyword only)
            The maximal amount of words that can be in between each word from `content`.
        
        sort_by : ``None | str | MessageSearchSortByType``, Optional (Keyword only)
            By what to sort the returned messages.
        
        sort_order : ``None | str | MessageSearchSortOrderType``, Optional (Keyword only)
            How to order the returned messages. Depending on the `sort_by`, this field may not be respected.
        
        url_host_names : `None | str | iterable<str>`, Optional (Keyword only)
            Whether the returned messages should contain urls with these host names.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        ValueError
            - If a parameter's value is incorrect.
        TypeError
            - If a parameter's type is incorrect.
        """
        serialisation_flags = self._serialisation_flags
        
        # after
        if (after is ...):
            after = self.after
        else:
            after = validate_after(after)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_AFTER)
        
        # attachment_extensions
        if (attachment_extensions is ...):
            attachment_extensions = self.attachment_extensions
            if (attachment_extensions is not None):
                attachment_extensions = (*attachment_extensions,)
        else:
            attachment_extensions = validate_attachment_extensions(attachment_extensions)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_ATTACHMENT_EXTENSIONS)
        
        # attachment_names
        if (attachment_names is ...):
            attachment_names = self.attachment_names
            if (attachment_names is not None):
                attachment_names = (*attachment_names,)
        else:
            attachment_names = validate_attachment_names(attachment_names)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_ATTACHMENT_NAMES)
        
        # author_ids
        if (author_ids is ...):
            author_ids = self.author_ids
            if (author_ids is not None):
                author_ids = (*author_ids,)
        else:
            author_ids = validate_author_ids(author_ids)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_AUTHOR_IDS)
        
        # author_types
        if (author_types is ...):
            author_types = self.author_types
            if (author_types is not None):
                author_types = (*author_types,)
        else:
            author_types = validate_author_types(author_types)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_AUTHOR_TYPES)
        
        # before
        if (before is ...):
            before = self.before
        else:
            before = validate_before(before)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_BEFORE)
        
        # channel_ids
        if (channel_ids is ...):
            channel_ids = self.channel_ids
            if (channel_ids is not None):
                channel_ids = (*channel_ids,)
        else:
            channel_ids = validate_channel_ids(channel_ids)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_CHANNEL_IDS)
        
        # content
        if (content is ...):
            content = self.content
        else:
            content = validate_content(content)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_CONTENT)
        
        # embed_providers
        if (embed_providers is ...):
            embed_providers = self.embed_providers
            if (embed_providers is not None):
                embed_providers = (*embed_providers,)
        else:
            embed_providers = validate_embed_providers(embed_providers)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_EMBED_PROVIDERS)
        
        # embed_types
        if (embed_types is ...):
            embed_types = self.embed_types
            if (embed_types is not None):
                embed_types = (*embed_types,)
        else:
            embed_types = validate_embed_types(embed_types)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_EMBED_TYPES)
        
        # has_types
        if (has_types is ...):
            has_types = self.has_types
            if (has_types is not None):
                has_types = (*has_types,)
        else:
            has_types = validate_has_types(has_types)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_HAS_TYPES)
        
        # include_nsfw_channels
        if (include_nsfw_channels is ...):
            include_nsfw_channels = self.include_nsfw_channels
        else:
            include_nsfw_channels = validate_include_nsfw_channels(include_nsfw_channels)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_INCLUDE_NSFW_CHANNELS)
        
        # limit
        if (limit is ...):
            limit = self.limit
        else:
            limit = validate_limit(limit)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_LIMIT)
        
        # mentioned_everyone
        if (mentioned_everyone is ...):
            mentioned_everyone = self.mentioned_everyone
        else:
            mentioned_everyone = validate_mentioned_everyone(mentioned_everyone)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_MENTIONED_EVERYONE)
        
        # mentioned_user_ids
        if (mentioned_user_ids is ...):
            mentioned_user_ids = self.mentioned_user_ids
            if (mentioned_user_ids is not None):
                mentioned_user_ids = (*mentioned_user_ids,)
        else:
            mentioned_user_ids = validate_mentioned_user_ids(mentioned_user_ids)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_MENTIONED_USER_IDS)
        
        # offset
        if (offset is ...):
            offset = self.offset
        else:
            offset = validate_offset(offset)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_OFFSET)
        
        # pinned
        if (pinned is ...):
            pinned = self.pinned
        else:
            pinned = validate_pinned(pinned)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_PINNED)
        
        # slop
        if (slop is ...):
            slop = self.slop
        else:
            slop = validate_slop(slop)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_SLOP)
        
        # sort_by
        if (sort_by is ...):
            sort_by = self.sort_by
        else:
            sort_by = validate_sort_by(sort_by)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_SORT_BY)
        
        # sort_order
        if (sort_order is ...):
            sort_order = self.sort_order
        else:
            sort_order = validate_sort_order(sort_order)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_SORT_ORDER)
        
        # url_host_names
        if (url_host_names is ...):
            url_host_names = self.url_host_names
            if (url_host_names is not None):
                url_host_names = (*url_host_names,)
        else:
            url_host_names = validate_url_host_names(url_host_names)
            serialisation_flags |= (1 << SERIALISATION_SHIFT_URL_HOST_NAMES)
        
        # Construct
        new = object.__new__(type(self))
        new._serialisation_flags = serialisation_flags
        new.after = after
        new.attachment_extensions = attachment_extensions
        new.attachment_names = attachment_names
        new.author_ids = author_ids
        new.author_types = author_types
        new.before = before
        new.channel_ids = channel_ids
        new.content = content
        new.embed_providers = embed_providers
        new.embed_types = embed_types
        new.has_types = has_types
        new.include_nsfw_channels = include_nsfw_channels
        new.limit = limit
        new.mentioned_everyone = mentioned_everyone
        new.mentioned_user_ids = mentioned_user_ids
        new.offset = offset
        new.pinned = pinned
        new.slop = slop
        new.sort_by = sort_by
        new.sort_order = sort_order
        new.url_host_names = url_host_names
        return new
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a message search query from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Data to create the instance from.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self._serialisation_flags = (
            (('min_id' in data) << SERIALISATION_SHIFT_AFTER) |
            (('attachment_extension' in data) << SERIALISATION_SHIFT_ATTACHMENT_EXTENSIONS) |
            (('attachment_filename' in data) << SERIALISATION_SHIFT_ATTACHMENT_NAMES) |
            (('author_id' in data) << SERIALISATION_SHIFT_AUTHOR_IDS) |
            (('author_type' in data) << SERIALISATION_SHIFT_AUTHOR_TYPES) |
            (('max_id' in data) << SERIALISATION_SHIFT_BEFORE) |
            (('channel_id' in data) << SERIALISATION_SHIFT_CHANNEL_IDS) |
            (('content' in data) << SERIALISATION_SHIFT_CONTENT) |
            (('embed_provider' in data) << SERIALISATION_SHIFT_EMBED_PROVIDERS) |
            (('embed_type' in data) << SERIALISATION_SHIFT_EMBED_TYPES) |
            (('has' in data) << SERIALISATION_SHIFT_HAS_TYPES) |
            (('include_nsfw' in data) << SERIALISATION_SHIFT_INCLUDE_NSFW_CHANNELS) |
            (('limit' in data) << SERIALISATION_SHIFT_LIMIT) |
            (('mention_everyone' in data) << SERIALISATION_SHIFT_MENTIONED_EVERYONE) |
            (('mentions' in data) << SERIALISATION_SHIFT_MENTIONED_USER_IDS) |
            (('offset' in data) << SERIALISATION_SHIFT_OFFSET) |
            (('pinned' in data) << SERIALISATION_SHIFT_PINNED) |
            (('slop' in data) << SERIALISATION_SHIFT_SLOP) |
            (('sort_by' in data) << SERIALISATION_SHIFT_SORT_BY) |
            (('sort_order' in data) << SERIALISATION_SHIFT_SORT_ORDER) |
            (('link_hostname' in data) << SERIALISATION_SHIFT_URL_HOST_NAMES)
        )
        self.after = parse_after(data)
        self.attachment_extensions = parse_attachment_extensions(data)
        self.attachment_names = parse_attachment_names(data)
        self.author_ids = parse_author_ids(data)
        self.author_types = parse_author_types(data)
        self.before = parse_before(data)
        self.channel_ids = parse_channel_ids(data)
        self.content = parse_content(data)
        self.embed_providers = parse_embed_providers(data)
        self.embed_types = parse_embed_types(data)
        self.has_types = parse_has_types(data)
        self.include_nsfw_channels = parse_include_nsfw_channels(data)
        self.limit = parse_limit(data)
        self.mentioned_everyone = parse_mentioned_everyone(data)
        self.mentioned_user_ids = parse_mentioned_user_ids(data)
        self.offset = parse_offset(data)
        self.pinned = parse_pinned(data)
        self.slop = parse_slop(data)
        self.sort_by = parse_sort_by(data)
        self.sort_order = parse_sort_order(data)
        self.url_host_names = parse_url_host_names(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serialises the message search query.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields as their defaults should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        serialisation_flags = self._serialisation_flags
        put_after(
            self.after,
            data,
            defaults or ((serialisation_flags >> SERIALISATION_SHIFT_AFTER) & 1),
        )
        put_attachment_extensions(
            self.attachment_extensions,
            data,
            defaults or ((serialisation_flags >> SERIALISATION_SHIFT_ATTACHMENT_EXTENSIONS) & 1),
        )
        put_attachment_names(
            self.attachment_names,
            data,
            defaults or ((serialisation_flags >> SERIALISATION_SHIFT_ATTACHMENT_NAMES) & 1),
        )
        put_author_ids(
            self.author_ids,
            data,
            defaults or ((serialisation_flags >> SERIALISATION_SHIFT_AUTHOR_IDS) & 1),
        )
        put_author_types(
            self.author_types,
            data,
            defaults or ((serialisation_flags >> SERIALISATION_SHIFT_AUTHOR_TYPES) & 1),
        )
        put_before(
            self.before,
            data,
            defaults or ((serialisation_flags >> SERIALISATION_SHIFT_BEFORE) & 1),
        )
        put_channel_ids(
            self.channel_ids,
            data,
            defaults or ((serialisation_flags >> SERIALISATION_SHIFT_CHANNEL_IDS) & 1),
        )
        put_content(
            self.content,
            data,
            defaults or ((serialisation_flags >> SERIALISATION_SHIFT_CONTENT) & 1),
        )
        put_embed_providers(
            self.embed_providers,
            data,
            defaults or ((serialisation_flags >> SERIALISATION_SHIFT_EMBED_PROVIDERS) & 1),
        )
        put_embed_types(
            self.embed_types,
            data,
            defaults or ((serialisation_flags >> SERIALISATION_SHIFT_EMBED_TYPES) & 1),
        )
        put_has_types(
            self.has_types,
            data,
            defaults or ((serialisation_flags >> SERIALISATION_SHIFT_HAS_TYPES) & 1),
        )
        put_include_nsfw_channels(
            self.include_nsfw_channels,
            data,
            defaults or ((serialisation_flags >> SERIALISATION_SHIFT_INCLUDE_NSFW_CHANNELS) & 1),
        )
        put_limit(
            self.limit,
            data,
            defaults or ((serialisation_flags >> SERIALISATION_SHIFT_LIMIT) & 1),
        )
        put_mentioned_everyone(
            self.mentioned_everyone,
            data,
            defaults or ((serialisation_flags >> SERIALISATION_SHIFT_MENTIONED_EVERYONE) & 1),
        )
        put_mentioned_user_ids(
            self.mentioned_user_ids,
            data,
            defaults or ((serialisation_flags >> SERIALISATION_SHIFT_MENTIONED_USER_IDS) & 1),
        )
        put_offset(
            self.offset,
            data,
            defaults or ((serialisation_flags >> SERIALISATION_SHIFT_OFFSET) & 1),
        )
        put_pinned(
            self.pinned,
            data,
            defaults or ((serialisation_flags >> SERIALISATION_SHIFT_PINNED) & 1),
        )
        put_slop(
            self.slop,
            data,
            defaults or ((serialisation_flags >> SERIALISATION_SHIFT_SLOP) & 1),
        )
        put_sort_by(
            self.sort_by,
            data,
            defaults or ((serialisation_flags >> SERIALISATION_SHIFT_SORT_BY) & 1),
        )
        put_sort_order(
            self.sort_order,
            data,
            defaults or ((serialisation_flags >> SERIALISATION_SHIFT_SORT_ORDER) & 1),
        )
        put_url_host_names(
            self.url_host_names,
            data,
            defaults or ((serialisation_flags >> SERIALISATION_SHIFT_URL_HOST_NAMES) & 1),
        )
        return data

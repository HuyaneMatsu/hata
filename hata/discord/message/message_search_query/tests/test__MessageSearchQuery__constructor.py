import vampytest

from datetime import datetime as DateTime, timezone as TimeZone

from ....embed import EmbedType

from ..message_search_query import MessageSearchQuery
from ..preinstanced import (
    MessageSearchAuthorType, MessageSearchHasType, MessageSearchSortByType, MessageSearchSortOrderType
)


def _assert_fields_set(message_search_query):
    """
    Asserts whether every attributes of the given instance are set.
    
    Parameters
    ----------
    message_search_query : ``MessageSearchQuery``
        The instance to check.
    """
    vampytest.assert_instance(message_search_query, MessageSearchQuery)
    vampytest.assert_instance(message_search_query._serialisation_flags, int)
    vampytest.assert_instance(message_search_query.after, DateTime, nullable = True)
    vampytest.assert_instance(message_search_query.attachment_extensions, tuple, nullable = True)
    vampytest.assert_instance(message_search_query.attachment_names, tuple, nullable = True)
    vampytest.assert_instance(message_search_query.author_ids, tuple, nullable = True)
    vampytest.assert_instance(message_search_query.author_types, tuple, nullable = True)
    vampytest.assert_instance(message_search_query.before, DateTime, nullable = True)
    vampytest.assert_instance(message_search_query.channel_ids, tuple, nullable = True)
    vampytest.assert_instance(message_search_query.content, str, nullable = True)
    vampytest.assert_instance(message_search_query.embed_providers, tuple, nullable = True)
    vampytest.assert_instance(message_search_query.embed_types, tuple, nullable = True)
    vampytest.assert_instance(message_search_query.has_types, tuple, nullable = True)
    vampytest.assert_instance(message_search_query.include_nsfw_channels, bool)
    vampytest.assert_instance(message_search_query.limit, int)
    vampytest.assert_instance(message_search_query.mentioned_everyone, bool)
    vampytest.assert_instance(message_search_query.mentioned_user_ids, tuple, nullable = True)
    vampytest.assert_instance(message_search_query.offset, int)
    vampytest.assert_instance(message_search_query.pinned, bool)
    vampytest.assert_instance(message_search_query.slop, int)
    vampytest.assert_instance(message_search_query.sort_by, MessageSearchSortByType)
    vampytest.assert_instance(message_search_query.sort_order, MessageSearchSortOrderType)
    vampytest.assert_instance(message_search_query.url_host_names, tuple, nullable = True)


def test__MessageSearchQuery__new__no_fields():
    """
    Tests whether ``MessageSearchQuery.__new__`` works as intended.
    
    Case: no fields given.
    """
    message_search_query = MessageSearchQuery()
    _assert_fields_set(message_search_query)
    
    vampytest.assert_eq(message_search_query._serialisation_flags, 0)


def test__MessageSearchQuery__new__all_fields():
    """
    Tests whether ``MessageSearchQuery.__new__`` works as intended.
    
    Case: all fields given.
    """
    after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    attachment_extensions = ['apng', 'png']
    attachment_names = ['okuu', 'orin']
    author_ids = [202601050000, 202601050001]
    author_types = [MessageSearchAuthorType.bot, MessageSearchAuthorType.user]
    before = DateTime(2016, 4, 14, tzinfo = TimeZone.utc)
    channel_ids = [202601050002, 202601050003]
    content = 'pat'
    embed_providers = ['kaenbyou', 'utsuho']
    embed_types = [EmbedType.image, EmbedType.video]
    has_types = [MessageSearchHasType.image, MessageSearchHasType.video]
    include_nsfw_channels = True
    limit = 20
    mentioned_everyone = True
    mentioned_user_ids = [202601050004, 202601050005]
    offset = 30
    pinned = True
    slop = 3
    sort_by = MessageSearchSortByType.relevance
    sort_order = MessageSearchSortOrderType.ascending
    url_host_names = ['komeiji', 'scarlet']
    
    message_search_query = MessageSearchQuery(
        after = after,
        attachment_extensions = attachment_extensions,
        attachment_names = attachment_names,
        author_ids = author_ids,
        author_types = author_types,
        before = before,
        channel_ids = channel_ids,
        content = content,
        embed_providers = embed_providers,
        embed_types = embed_types,
        has_types = has_types,
        include_nsfw_channels = include_nsfw_channels,
        limit = limit,
        mentioned_everyone = mentioned_everyone,
        mentioned_user_ids = mentioned_user_ids,
        offset = offset,
        pinned = pinned,
        slop = slop,
        sort_by = sort_by,
        sort_order = sort_order,
        url_host_names = url_host_names,
    )
    _assert_fields_set(message_search_query)
    
    vampytest.assert_eq(message_search_query._serialisation_flags, (1 << 21) - 1)
    vampytest.assert_eq(message_search_query.after, after)
    vampytest.assert_eq(message_search_query.attachment_extensions, tuple(attachment_extensions))
    vampytest.assert_eq(message_search_query.attachment_names, tuple(attachment_names))
    vampytest.assert_eq(message_search_query.author_ids, tuple(author_ids))
    vampytest.assert_eq(message_search_query.author_types, tuple(author_types))
    vampytest.assert_eq(message_search_query.before, before)
    vampytest.assert_eq(message_search_query.channel_ids, tuple(channel_ids))
    vampytest.assert_eq(message_search_query.content, content)
    vampytest.assert_eq(message_search_query.embed_providers, tuple(embed_providers))
    vampytest.assert_eq(message_search_query.embed_types, tuple(embed_types))
    vampytest.assert_eq(message_search_query.has_types, tuple(has_types))
    vampytest.assert_eq(message_search_query.include_nsfw_channels, include_nsfw_channels)
    vampytest.assert_eq(message_search_query.limit, limit)
    vampytest.assert_eq(message_search_query.mentioned_everyone, mentioned_everyone)
    vampytest.assert_eq(message_search_query.mentioned_user_ids, tuple(mentioned_user_ids))
    vampytest.assert_eq(message_search_query.offset, offset)
    vampytest.assert_eq(message_search_query.pinned, pinned)
    vampytest.assert_eq(message_search_query.slop, slop)
    vampytest.assert_is(message_search_query.sort_by, sort_by)
    vampytest.assert_is(message_search_query.sort_order, sort_order)
    vampytest.assert_eq(message_search_query.url_host_names, tuple(url_host_names))

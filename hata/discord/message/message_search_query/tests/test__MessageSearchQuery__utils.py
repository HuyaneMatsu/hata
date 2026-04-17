import vampytest

from datetime import datetime as DateTime, timezone as TimeZone

from ....embed import EmbedType

from ..message_search_query import MessageSearchQuery
from ..preinstanced import (
    MessageSearchAuthorType, MessageSearchHasType, MessageSearchSortByType, MessageSearchSortOrderType
)

from .test__MessageSearchQuery__constructor import _assert_fields_set


def test__MessageSearchQuery__copy():
    """
    Tests whether ``MessageSearchQuery.copy`` works as intended.
    """
    after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    attachment_extensions = ['apng', 'png']
    attachment_names = ['okuu', 'orin']
    author_ids = [202601050036, 202601050037]
    author_types = [MessageSearchAuthorType.bot, MessageSearchAuthorType.user]
    before = DateTime(2016, 4, 14, tzinfo = TimeZone.utc)
    channel_ids = [202601050038, 202601050039]
    content = 'pat'
    embed_providers = ['kaenbyou', 'utsuho']
    embed_types = [EmbedType.image, EmbedType.video]
    has_types = [MessageSearchHasType.image, MessageSearchHasType.video]
    include_nsfw_channels = True
    limit = 20
    mentioned_everyone = True
    mentioned_user_ids = [202601050040, 202601050041]
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
    copy = message_search_query.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, message_search_query)
    vampytest.assert_eq(copy, message_search_query)


def test__MessageSearchQuery__copy_with__no_fields():
    """
    Tests whether ``MessageSearchQuery.copy_with`` works as intended.
    
    Case: no fields given.
    """
    after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    attachment_extensions = ['apng', 'png']
    attachment_names = ['okuu', 'orin']
    author_ids = [202601050036, 202601050037]
    author_types = [MessageSearchAuthorType.bot, MessageSearchAuthorType.user]
    before = DateTime(2016, 4, 14, tzinfo = TimeZone.utc)
    channel_ids = [202601050038, 202601050039]
    content = 'pat'
    embed_providers = ['kaenbyou', 'utsuho']
    embed_types = [EmbedType.image, EmbedType.video]
    has_types = [MessageSearchHasType.image, MessageSearchHasType.video]
    include_nsfw_channels = True
    limit = 20
    mentioned_everyone = True
    mentioned_user_ids = [202601050040, 202601050041]
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
    copy = message_search_query.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, message_search_query)
    vampytest.assert_eq(copy, message_search_query)


def test__MessageSearchQuery__copy_with__all_fields():
    """
    Tests whether ``MessageSearchQuery.copy_with`` works as intended.
    
    Case: no fields given.
    """
    old_after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    old_attachment_extensions = ['apng', 'png']
    old_attachment_names = ['okuu', 'orin']
    old_author_ids = [202601050042, 202601050043]
    old_author_types = [MessageSearchAuthorType.bot, MessageSearchAuthorType.user]
    old_before = DateTime(2016, 4, 14, tzinfo = TimeZone.utc)
    old_channel_ids = [202601050044, 202601050045]
    old_content = 'pat'
    old_embed_providers = ['kaenbyou', 'utsuho']
    old_embed_types = [EmbedType.image, EmbedType.video]
    old_has_types = [MessageSearchHasType.image, MessageSearchHasType.video]
    old_include_nsfw_channels = True
    old_limit = 20
    old_mentioned_everyone = True
    old_mentioned_user_ids = [202601050046, 202601050047]
    old_offset = 30
    old_pinned = True
    old_slop = 3
    old_sort_by = MessageSearchSortByType.relevance
    old_sort_order = MessageSearchSortOrderType.ascending
    old_url_host_names = ['komeiji', 'scarlet']
    
    new_after = DateTime(2016, 5, 13, tzinfo = TimeZone.utc)
    new_attachment_extensions = ['avif', 'gif']
    new_attachment_names = ['koishi', 'satori']
    new_author_ids = [202601050048, 202601050049]
    new_author_types = [MessageSearchAuthorType.bot, MessageSearchAuthorType.user]
    new_before = DateTime(2016, 4, 15, tzinfo = TimeZone.utc)
    new_channel_ids = [202601050050, 202601050051]
    new_content = 'hug'
    new_embed_providers = ['mountain', 'tengu']
    new_embed_types = [EmbedType.gift, EmbedType.gifv]
    new_has_types = [MessageSearchHasType.link, MessageSearchHasType.poll]
    new_include_nsfw_channels = False
    new_limit = 19
    new_mentioned_everyone = False
    new_mentioned_user_ids = [202601050052, 202601050053]
    new_offset = 29
    new_pinned = False
    new_slop = 4
    new_sort_by = MessageSearchSortByType.creation
    new_sort_order = MessageSearchSortOrderType.descending
    new_url_host_names = ['inubashiri', 'shameimaru']
    
    message_search_query = MessageSearchQuery(
        after = old_after,
        attachment_extensions = old_attachment_extensions,
        attachment_names = old_attachment_names,
        author_ids = old_author_ids,
        author_types = old_author_types,
        before = old_before,
        channel_ids = old_channel_ids,
        content = old_content,
        embed_providers = old_embed_providers,
        embed_types = old_embed_types,
        has_types = old_has_types,
        include_nsfw_channels = old_include_nsfw_channels,
        limit = old_limit,
        mentioned_everyone = old_mentioned_everyone,
        mentioned_user_ids = old_mentioned_user_ids,
        offset = old_offset,
        pinned = old_pinned,
        slop = old_slop,
        sort_by = old_sort_by,
        sort_order = old_sort_order,
        url_host_names = old_url_host_names,
    )
    copy = message_search_query.copy_with(
        after = new_after,
        attachment_extensions = new_attachment_extensions,
        attachment_names = new_attachment_names,
        author_ids = new_author_ids,
        author_types = new_author_types,
        before = new_before,
        channel_ids = new_channel_ids,
        content = new_content,
        embed_providers = new_embed_providers,
        embed_types = new_embed_types,
        has_types = new_has_types,
        include_nsfw_channels = new_include_nsfw_channels,
        limit = new_limit,
        mentioned_everyone = new_mentioned_everyone,
        mentioned_user_ids = new_mentioned_user_ids,
        offset = new_offset,
        pinned = new_pinned,
        slop = new_slop,
        sort_by = new_sort_by,
        sort_order = new_sort_order,
        url_host_names = new_url_host_names,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, message_search_query)
    vampytest.assert_ne(copy, message_search_query)
    
    vampytest.assert_eq(copy._serialisation_flags, (1 << 21) - 1)
    vampytest.assert_eq(copy.after, new_after)
    vampytest.assert_eq(copy.attachment_extensions, tuple(new_attachment_extensions))
    vampytest.assert_eq(copy.attachment_names, tuple(new_attachment_names))
    vampytest.assert_eq(copy.author_ids, tuple(new_author_ids))
    vampytest.assert_eq(copy.author_types, tuple(new_author_types))
    vampytest.assert_eq(copy.before, new_before)
    vampytest.assert_eq(copy.channel_ids, tuple(new_channel_ids))
    vampytest.assert_eq(copy.content, new_content)
    vampytest.assert_eq(copy.embed_providers, tuple(new_embed_providers))
    vampytest.assert_eq(copy.embed_types, tuple(new_embed_types))
    vampytest.assert_eq(copy.has_types, tuple(new_has_types))
    vampytest.assert_eq(copy.include_nsfw_channels, new_include_nsfw_channels)
    vampytest.assert_eq(copy.limit, new_limit)
    vampytest.assert_eq(copy.mentioned_everyone, new_mentioned_everyone)
    vampytest.assert_eq(copy.mentioned_user_ids, tuple(new_mentioned_user_ids))
    vampytest.assert_eq(copy.offset, new_offset)
    vampytest.assert_eq(copy.pinned, new_pinned)
    vampytest.assert_eq(copy.slop, new_slop)
    vampytest.assert_is(copy.sort_by, new_sort_by)
    vampytest.assert_is(copy.sort_order, new_sort_order)
    vampytest.assert_eq(copy.url_host_names, tuple(new_url_host_names))

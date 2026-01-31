import vampytest

from datetime import datetime as DateTime, timezone as TimeZone

from ....embed import EmbedType
from ....utils import datetime_to_id

from ..message_search_query import MessageSearchQuery
from ..preinstanced import (
    MessageSearchAuthorType, MessageSearchHasType, MessageSearchSortByType, MessageSearchSortOrderType
)

from .test__MessageSearchQuery__constructor import _assert_fields_set


def test__MessageSearchQuery__from_data__no_fields():
    """
    Tests whether ``MessageSearchQuery.from_data`` works as intended.
    
    Case: no fields given.
    """
    data = {}
    
    message_search_query = MessageSearchQuery.from_data(data)
    _assert_fields_set(message_search_query)
    
    vampytest.assert_eq(message_search_query._serialisation_flags, 0)


def test__MessageSearchQuery__from_data__all_fields():
    """
    Tests whether ``MessageSearchQuery.from_data`` works as intended.
    
    Case: all fields given.
    """
    after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    attachment_extensions = ['apng', 'png']
    attachment_names = ['okuu', 'orin']
    author_ids = [202601050006, 202601050007]
    author_types = [MessageSearchAuthorType.bot, MessageSearchAuthorType.user]
    before = DateTime(2016, 4, 14, tzinfo = TimeZone.utc)
    channel_ids = [202601050008, 202601050009]
    content = 'pat'
    embed_providers = ['kaenbyou', 'utsuho']
    embed_types = [EmbedType.image, EmbedType.video]
    has_types = [MessageSearchHasType.image, MessageSearchHasType.video]
    include_nsfw_channels = True
    limit = 20
    mentioned_everyone = True
    mentioned_user_ids = [202601050010, 202601050011]
    offset = 30
    pinned = True
    slop = 3
    sort_by = MessageSearchSortByType.relevance
    sort_order = MessageSearchSortOrderType.ascending
    url_host_names = ['komeiji', 'scarlet']
    
    data = {
        'min_id': datetime_to_id(after),
        'attachment_extension': [*attachment_extensions],
        'attachment_filename': [*attachment_names],
        'author_id': [str(author_id) for author_id in author_ids],
        'author_type': [author_type.value for author_type in author_types],
        'max_id': datetime_to_id(before),
        'channel_id': [str(channel_id) for channel_id in channel_ids],
        'content': content,
        'embed_provider': [*embed_providers],
        'embed_type': [embed_type.value for embed_type in embed_types],
        'has': [has_type.value for has_type in has_types],
        'include_nsfw': include_nsfw_channels,
        'limit': limit,
        'mention_everyone': mentioned_everyone,
        'mentions': [str(user_id) for user_id in mentioned_user_ids],
        'offset': offset,
        'pinned': pinned,
        'slop': slop,
        'sort_by': sort_by.value,
        'sort_order': sort_order.value,
        'link_hostname': [*url_host_names],
    }
    
    message_search_query = MessageSearchQuery.from_data(data)
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


def test__MessageSearchQuery__to_data__no_fields():
    """
    Tests whether ``MessageSearchQuery.to_data`` works as intended.
    
    Case: no fields given.
    """
    expected_output = {}
    
    message_search_query = MessageSearchQuery()
    
    vampytest.assert_eq(
        message_search_query.to_data(),
        expected_output,
    )


def test__MessageSearchQuery__to_data__all_fields():
    """
    Tests whether ``MessageSearchQuery.from_data`` works as intended.
    
    Case: all fields given.
    """
    after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    attachment_extensions = ['apng', 'png']
    attachment_names = ['okuu', 'orin']
    author_ids = [202601050012, 202601050013]
    author_types = [MessageSearchAuthorType.bot, MessageSearchAuthorType.user]
    before = DateTime(2016, 4, 14, tzinfo = TimeZone.utc)
    channel_ids = [202601050014, 202601050015]
    content = 'pat'
    embed_providers = ['kaenbyou', 'utsuho']
    embed_types = [EmbedType.image, EmbedType.video]
    has_types = [MessageSearchHasType.image, MessageSearchHasType.video]
    include_nsfw_channels = True
    limit = 20
    mentioned_everyone = True
    mentioned_user_ids = [202601050016, 202601050017]
    offset = 30
    pinned = True
    slop = 3
    sort_by = MessageSearchSortByType.relevance
    sort_order = MessageSearchSortOrderType.ascending
    url_host_names = ['komeiji', 'scarlet']
    
    expected_output = {
        'min_id': datetime_to_id(after),
        'attachment_extension': [*attachment_extensions],
        'attachment_filename': [*attachment_names],
        'author_id': [str(author_id) for author_id in author_ids],
        'author_type': [author_type.value for author_type in author_types],
        'max_id': datetime_to_id(before),
        'channel_id': [str(channel_id) for channel_id in channel_ids],
        'content': content,
        'embed_provider': [*embed_providers],
        'embed_type': [embed_type.value for embed_type in embed_types],
        'has': [has_type.value for has_type in has_types],
        'include_nsfw': include_nsfw_channels,
        'limit': limit,
        'mention_everyone': mentioned_everyone,
        'mentions': [str(user_id) for user_id in mentioned_user_ids],
        'offset': offset,
        'pinned': pinned,
        'slop': slop,
        'sort_by': sort_by.value,
        'sort_order': sort_order.value,
        'link_hostname': [*url_host_names],
    }
    
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
    
    vampytest.assert_eq(
        message_search_query.to_data(),
        expected_output,
    )

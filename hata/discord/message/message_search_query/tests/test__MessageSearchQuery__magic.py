import vampytest

from datetime import datetime as DateTime, timezone as TimeZone

from ....embed import EmbedType

from ..message_search_query import MessageSearchQuery
from ..preinstanced import (
    MessageSearchAuthorType, MessageSearchHasType, MessageSearchSortByType, MessageSearchSortOrderType
)


def test__MessageSearchQuery__repr():
    """
    Tests whether ``MessageSearchQuery.__repr__`` works as intended.
    """
    after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    attachment_extensions = ['apng', 'png']
    attachment_names = ['okuu', 'orin']
    author_ids = [202601050018, 202601050019]
    author_types = [MessageSearchAuthorType.bot, MessageSearchAuthorType.user]
    before = DateTime(2016, 4, 14, tzinfo = TimeZone.utc)
    channel_ids = [202601050020, 202601050021]
    content = 'pat'
    embed_providers = ['kaenbyou', 'utsuho']
    embed_types = [EmbedType.image, EmbedType.video]
    has_types = [MessageSearchHasType.image, MessageSearchHasType.video]
    include_nsfw_channels = True
    limit = 20
    mentioned_everyone = True
    mentioned_user_ids = [202601050022, 202601050023]
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
    
    output = repr(message_search_query)
    vampytest.assert_instance(output, str)


def test__MessageSearchQuery__hash():
    """
    Tests whether ``MessageSearchQuery.__hash__`` works as intended.
    """
    after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    attachment_extensions = ['apng', 'png']
    attachment_names = ['okuu', 'orin']
    author_ids = [202601050024, 202601050025]
    author_types = [MessageSearchAuthorType.bot, MessageSearchAuthorType.user]
    before = DateTime(2016, 4, 14, tzinfo = TimeZone.utc)
    channel_ids = [202601050026, 202601050027]
    content = 'pat'
    embed_providers = ['kaenbyou', 'utsuho']
    embed_types = [EmbedType.image, EmbedType.video]
    has_types = [MessageSearchHasType.image, MessageSearchHasType.video]
    include_nsfw_channels = True
    limit = 20
    mentioned_everyone = True
    mentioned_user_ids = [202601050028, 202601050029]
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
    
    output = hash(message_search_query)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    attachment_extensions = ['apng', 'png']
    attachment_names = ['okuu', 'orin']
    author_ids = [202601050030, 202601050031]
    author_types = [MessageSearchAuthorType.bot, MessageSearchAuthorType.user]
    before = DateTime(2016, 4, 14, tzinfo = TimeZone.utc)
    channel_ids = [202601050032, 202601050033]
    content = 'pat'
    embed_providers = ['kaenbyou', 'utsuho']
    embed_types = [EmbedType.image, EmbedType.video]
    has_types = [MessageSearchHasType.image, MessageSearchHasType.video]
    include_nsfw_channels = True
    limit = 20
    mentioned_everyone = True
    mentioned_user_ids = [202601050034, 202601050035]
    offset = 30
    pinned = True
    slop = 3
    sort_by = MessageSearchSortByType.relevance
    sort_order = MessageSearchSortOrderType.ascending
    url_host_names = ['komeiji', 'scarlet']
    
    keyword_parameters = {
        'after': after,
        'attachment_extensions': attachment_extensions,
        'attachment_names': attachment_names,
        'author_ids': author_ids,
        'author_types': author_types,
        'before': before,
        'channel_ids': channel_ids,
        'content': content,
        'embed_providers': embed_providers,
        'embed_types': embed_types,
        'has_types': has_types,
        'include_nsfw_channels': include_nsfw_channels,
        'limit': limit,
        'mentioned_everyone': mentioned_everyone,
        'mentioned_user_ids': mentioned_user_ids,
        'offset': offset,
        'pinned': pinned,
        'slop': slop,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'url_host_names': url_host_names,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'after': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'attachment_extensions': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'attachment_names': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'author_ids': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'author_types': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'before': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'channel_ids': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'content': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'embed_providers': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'embed_types': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'has_types': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'include_nsfw_channels': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'limit': 19,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'mentioned_everyone': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'mentioned_user_ids': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'offset': 29,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'pinned': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'slop': 4,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'sort_by': MessageSearchSortByType.creation,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'sort_order': MessageSearchSortOrderType.descending,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'url_host_names': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__MessageSearchQuery__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``MessageSearchQuery.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    message_search_query_0 = MessageSearchQuery(**keyword_parameters_0)
    message_search_query_1 = MessageSearchQuery(**keyword_parameters_1)
    
    output = message_search_query_0 == message_search_query_1
    vampytest.assert_instance(output, bool)
    return output

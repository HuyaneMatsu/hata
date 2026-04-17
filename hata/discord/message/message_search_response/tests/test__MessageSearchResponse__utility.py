import vampytest

from ....channel import Channel, ChannelType

from ...message import Message

from ..message_search_response import MessageSearchResponse

from .test__MessageSearchResponse__constructor import _assert_fields_set


def test__MessageSearchResponse__copy():
    """
    Tests whether ``MessageSearchResponse.copy`` works as intended.
    """
    analytics_id = 12
    deep_historical_indexing_in_progress = True
    messages = [
        Message.precreate(
            202601090070,
        ),
        Message.precreate(
            202601090071,
        ),
    ]
    result_count = 6
    threads = [
        Channel.precreate(
            202601090072,
            channel_type = ChannelType.guild_thread_private,
        ),
        Channel.precreate(
            202601090073,
            channel_type = ChannelType.guild_thread_private,
        ),
    ]
    
    message_search_response = MessageSearchResponse(
        analytics_id = analytics_id,
        deep_historical_indexing_in_progress = deep_historical_indexing_in_progress,
        messages = messages,
        result_count = result_count,
        threads = threads,
    )
    
    copy = message_search_response.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, message_search_response)
    vampytest.assert_eq(copy, message_search_response)


def test__MessageSearchResponse__copy_with__no_fields():
    """
    Tests whether ``MessageSearchResponse.copy_with`` works as intended.
    
    Case: no fields given.
    """
    analytics_id = 12
    deep_historical_indexing_in_progress = True
    messages = [
        Message.precreate(
            202601090080,
        ),
        Message.precreate(
            202601090081,
        ),
    ]
    result_count = 6
    threads = [
        Channel.precreate(
            202601090082,
            channel_type = ChannelType.guild_thread_private,
        ),
        Channel.precreate(
            202601090083,
            channel_type = ChannelType.guild_thread_private,
        ),
    ]
    
    message_search_response = MessageSearchResponse(
        analytics_id = analytics_id,
        deep_historical_indexing_in_progress = deep_historical_indexing_in_progress,
        messages = messages,
        result_count = result_count,
        threads = threads,
    )
    
    copy = message_search_response.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, message_search_response)
    vampytest.assert_eq(copy, message_search_response)



def test__MessageSearchResponse__copy_with__all_fields():
    """
    Tests whether ``MessageSearchResponse.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_analytics_id = 12
    old_deep_historical_indexing_in_progress = True
    old_messages = [
        Message.precreate(
            202601090090,
        ),
        Message.precreate(
            202601090091,
        ),
    ]
    old_result_count = 6
    old_threads = [
        Channel.precreate(
            202601090092,
            channel_type = ChannelType.guild_thread_private,
        ),
        Channel.precreate(
            202601090093,
            channel_type = ChannelType.guild_thread_private,
        ),
    ]
    
    new_analytics_id = 13
    new_deep_historical_indexing_in_progress = False
    new_messages = [
        Message.precreate(
            202601090100,
        ),
        Message.precreate(
            202601090101,
        ),
    ]
    new_result_count = 7
    new_threads = [
        Channel.precreate(
            202601090102,
            channel_type = ChannelType.guild_thread_private,
        ),
        Channel.precreate(
            202601090103,
            channel_type = ChannelType.guild_thread_private,
        ),
    ]
    
    message_search_response = MessageSearchResponse(
        analytics_id = old_analytics_id,
        deep_historical_indexing_in_progress = old_deep_historical_indexing_in_progress,
        messages = old_messages,
        result_count = old_result_count,
        threads = old_threads,
    )
    
    copy = message_search_response.copy_with(
        analytics_id = new_analytics_id,
        deep_historical_indexing_in_progress = new_deep_historical_indexing_in_progress,
        messages = new_messages,
        result_count = new_result_count,
        threads = new_threads,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, message_search_response)
    vampytest.assert_ne(copy, message_search_response)

    vampytest.assert_eq(copy.analytics_id, new_analytics_id)
    vampytest.assert_eq(copy.deep_historical_indexing_in_progress, new_deep_historical_indexing_in_progress)
    vampytest.assert_eq(copy.messages, tuple(new_messages))
    vampytest.assert_eq(copy.result_count, new_result_count)
    vampytest.assert_eq(copy.threads, tuple(new_threads))

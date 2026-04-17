import vampytest

from ....channel import Channel, ChannelType

from ...message import Message

from ..message_search_response import MessageSearchResponse

from .test__MessageSearchResponse__constructor import _assert_fields_set


def test__MessageSearchResponse__from_data():
    """
    Tests whether ``MessageSearchResponse.from_data`` works as intended.
    """
    analytics_id = 12
    deep_historical_indexing_in_progress = True
    messages = [
        Message.precreate(
            202601090010,
        ),
        Message.precreate(
            202601090011,
        ),
    ]
    result_count = 6
    threads = [
        Channel.precreate(
            202601090012,
            channel_type = ChannelType.guild_thread_private,
        ),
        Channel.precreate(
            202601090013,
            channel_type = ChannelType.guild_thread_private,
        ),
    ]
    
    input_data = {
        'analytics_id': format(analytics_id, '0>32x'),
        'doing_deep_historical_index': deep_historical_indexing_in_progress,
        'messages': [[message.to_data(include_internals = True)] for message in messages],
        'total_results': result_count,
        'threads': [channel.to_data(include_internals = True) for channel in threads],
        'members': [],
    }
    
    message_search_response = MessageSearchResponse.from_data(input_data)
    _assert_fields_set(message_search_response)
    
    vampytest.assert_eq(message_search_response.analytics_id, analytics_id)
    vampytest.assert_eq(message_search_response.deep_historical_indexing_in_progress, deep_historical_indexing_in_progress)
    vampytest.assert_eq(message_search_response.messages, tuple(messages))
    vampytest.assert_eq(message_search_response.result_count, result_count)
    vampytest.assert_eq(message_search_response.threads, tuple(threads))



def test__MessageSearchResponse__to_data():
    """
    Tests whether ``MessageSearchResponse.to-data`` works as intended.
    """
    analytics_id = 12
    deep_historical_indexing_in_progress = True
    messages = [
        Message.precreate(
            202601090020,
        ),
        Message.precreate(
            202601090021,
        ),
    ]
    result_count = 6
    threads = [
        Channel.precreate(
            202601090022,
            channel_type = ChannelType.guild_thread_private,
        ),
        Channel.precreate(
            202601090023,
            channel_type = ChannelType.guild_thread_private,
        ),
    ]
    
    expected_output = {
        'analytics_id': format(analytics_id, '0>32x'),
        'doing_deep_historical_index': deep_historical_indexing_in_progress,
        'messages': [[message.to_data(defaults = True, include_internals = True)] for message in messages],
        'total_results': result_count,
        'threads': [channel.to_data(defaults = True, include_internals = True) for channel in threads],
        'members': [],
    }
    
    message_search_response = MessageSearchResponse(
        analytics_id = analytics_id,
        deep_historical_indexing_in_progress = deep_historical_indexing_in_progress,
        messages = messages,
        result_count = result_count,
        threads = threads,
    )
    
    vampytest.assert_eq(
        message_search_response.to_data(defaults = True),
        expected_output,
    )

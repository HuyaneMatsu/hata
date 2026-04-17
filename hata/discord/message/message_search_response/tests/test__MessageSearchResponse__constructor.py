import vampytest

from ....channel import Channel, ChannelType

from ...message import Message

from ..message_search_response import MessageSearchResponse


def _assert_fields_set(message_search_response):
    """
    Asserts whether the given instance has all of its fields set.
    
    Parameters
    ----------
    message_search_response : ``MessageSearchResponse``
        The instance to check.
    """
    vampytest.assert_instance(message_search_response, MessageSearchResponse)
    vampytest.assert_instance(message_search_response.analytics_id, int)
    vampytest.assert_instance(message_search_response.deep_historical_indexing_in_progress, bool)
    vampytest.assert_instance(message_search_response.messages, tuple, nullable = True)
    vampytest.assert_instance(message_search_response.result_count, int)
    vampytest.assert_instance(message_search_response.threads, tuple, nullable = True)


def test__MessageSearchResponse__new__no_fields():
    """
    Tests whether ``MessageSearchResponse.__new__`` works as intended.
    
    Case: no fields given.
    """
    message_search_response = MessageSearchResponse()
    _assert_fields_set(message_search_response)


def test__MessageSearchResponse__new__all_fields():
    """
    Tests whether ``MessageSearchResponse.__new__`` works as intended.
    
    Case: all fields given.
    """
    analytics_id = 12
    deep_historical_indexing_in_progress = True
    messages = [
        Message.precreate(
            202601090000,
        ),
        Message.precreate(
            202601090001,
        ),
    ]
    result_count = 6
    threads = [
        Channel.precreate(
            202601090002,
            channel_type = ChannelType.guild_thread_private,
        ),
        Channel.precreate(
            202601090003,
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
    _assert_fields_set(message_search_response)
    
    vampytest.assert_eq(message_search_response.analytics_id, analytics_id)
    vampytest.assert_eq(message_search_response.deep_historical_indexing_in_progress, deep_historical_indexing_in_progress)
    vampytest.assert_eq(message_search_response.messages, tuple(messages))
    vampytest.assert_eq(message_search_response.result_count, result_count)
    vampytest.assert_eq(message_search_response.threads, tuple(threads))

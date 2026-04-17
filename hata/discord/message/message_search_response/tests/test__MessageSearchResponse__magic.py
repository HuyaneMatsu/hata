import vampytest

from ....channel import Channel, ChannelType

from ...message import Message

from ..message_search_response import MessageSearchResponse


def test__MessageSearchResponse__repr():
    """
    Tests whether ``MessageSearchResponse.__repr__`` works as intended.
    """
    analytics_id = 12
    deep_historical_indexing_in_progress = True
    messages = [
        Message.precreate(
            202601090040,
        ),
        Message.precreate(
            202601090041,
        ),
    ]
    result_count = 6
    threads = [
        Channel.precreate(
            202601090042,
            channel_type = ChannelType.guild_thread_private,
        ),
        Channel.precreate(
            202601090043,
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
    
    output = repr(message_search_response)
    vampytest.assert_instance(output, str)


def test__MessageSearchResponse__hash():
    """
    Tests whether ``MessageSearchResponse.__hash__`` works as intended.
    """
    analytics_id = 12
    deep_historical_indexing_in_progress = True
    messages = [
        Message.precreate(
            202601090050,
        ),
        Message.precreate(
            202601090051,
        ),
    ]
    result_count = 6
    threads = [
        Channel.precreate(
            202601090052,
            channel_type = ChannelType.guild_thread_private,
        ),
        Channel.precreate(
            202601090053,
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
    
    output = hash(message_search_response)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    analytics_id = 12
    deep_historical_indexing_in_progress = True
    messages = [
        Message.precreate(
            202601090060,
        ),
        Message.precreate(
            202601090061,
        ),
    ]
    result_count = 6
    threads = [
        Channel.precreate(
            202601090062,
            channel_type = ChannelType.guild_thread_private,
        ),
        Channel.precreate(
            202601090063,
            channel_type = ChannelType.guild_thread_private,
        ),
    ]
    
    keyword_parameters = {
        'analytics_id': analytics_id,
        'deep_historical_indexing_in_progress': deep_historical_indexing_in_progress,
        'messages': messages,
        'result_count': result_count,
        'threads': threads,
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
            'analytics_id': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'deep_historical_indexing_in_progress': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'messages': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'result_count': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'threads': None,
        },
        False,
    )

@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__MessageSearchResponse__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``MessageSearchResponse.__eq__`` works as intended.
    
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
    message_search_response_0 = MessageSearchResponse(**keyword_parameters_0)
    message_search_response_1 = MessageSearchResponse(**keyword_parameters_1)
    
    output = message_search_response_0 == message_search_response_1
    vampytest.assert_instance(output, bool)
    return output

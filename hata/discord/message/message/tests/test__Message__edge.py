import vampytest

from ...message import Message


def test__Message__edge__different_intent():
    """
    Tests a ``Message`` creation edge case. We receive 2 payloads for the same message. First has no message content
    intent while the second has. The message references an other one, meaning that the second payload should update the
    referenced message's content fields too.
    """
    data_0 = {
        'channel_id': '790028318237261864',
        'content': '',
        'embeds': [],
        'guild_id': '388267636661682178',
        'id': '1120816663890247842',
        'message_reference': {
            'channel_id': '790028318237261864',
            'guild_id': '388267636661682178',
            'message_id': '1120813468514263151'
        },
        'referenced_message': {
            'channel_id': '790028318237261864',
            'content': '',
            'embeds': [],
            'id': '1120813468514263151',
            'message_reference': {
                'channel_id': '790028318237261864',
                'guild_id': '388267636661682178',
                'message_id': '1120806435316572180'
            },
            'type': 19
        },
        'type': 19
    }
    
    data_1 = {
        'guild_id': '388267636661682178',
        'id': '1120816663890247842',
        'message_reference': {
            'channel_id': '790028318237261864',
            'guild_id': '388267636661682178',
            'message_id': '1120813468514263151'
        },
        'referenced_message': {
            'channel_id': '790028318237261864',
            'content': 'Ayaya',
            'embeds': [
                {
                    'title': 'aya',
                    'type': 'rich'
                }
            ],
            'message_reference': {
                'channel_id': '790028318237261864',
                'guild_id': '388267636661682178',
                'message_id': '1120806435316572180'
            },
            'type': 19
        },
        'type': 19
    }
    
    message_0 = Message.from_data(data_0)
    message_1 = Message.from_data(data_1)
    
    vampytest.assert_is_not(message_0.referenced_message, None)
    vampytest.assert_is_not(message_0.referenced_message.embeds, None)

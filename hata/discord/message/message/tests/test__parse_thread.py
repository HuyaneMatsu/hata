import vampytest

from ....channel import Channel, ChannelType

from ..fields import parse_thread


def test__parse_thread__0():
    """
    Tests whether ``parse_thread`` works as intended.
    
    Case: nothing.
    """
    for input_data in (
        {},
        {'thread': None},
    ):
        output = parse_thread(input_data)
        vampytest.assert_is(output, None)


def test__parse_thread__1():
    """
    Tests whether ``parse_thread`` works as intended.
    
    Case: Entity present.
    """
    channel_id = 202304300013
    guild_id = 202304300014
    name = 'More ENS'
    channel_type = ChannelType.guild_thread_private
    
    input_data = {
        'thread': {
            'id': str(channel_id),
            'name': name,
            'type': channel_type.value,
        },
    }
    
    output = parse_thread(input_data, guild_id)
    
    vampytest.assert_instance(output, Channel)
    vampytest.assert_eq(output.id, channel_id)
    vampytest.assert_eq(output.guild_id, guild_id)
    vampytest.assert_eq(output.name, name)
    vampytest.assert_is(output.type, channel_type)

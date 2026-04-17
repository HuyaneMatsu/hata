import vampytest

from ..guild_widget_channel import GuildWidgetChannel

from .test__GuildWidgetChannel__constructor import _assert_fields_set


def test__GuildWidgetChannel__from_data__0():
    """
    Tests whether ``GuildWidgetChannel.from_data`` works as intended.
    
    Case: all fields given.
    """
    channel_id = 202305180001
    name = 'East'
    position = 11
    
    data = {
        'id': str(channel_id),
        'name': name,
        'position': position,
    }
    
    widget_channel = GuildWidgetChannel.from_data(data)
    _assert_fields_set(widget_channel)

    vampytest.assert_eq(widget_channel.id, channel_id)
    vampytest.assert_eq(widget_channel.name, name)
    vampytest.assert_eq(widget_channel.position, position)


def test__GuildWidgetChannel__to_data__0():
    """
    Tests whether ``GuildWidgetChannel.to_data`` works as intended.
    
    Case: Include defaults.
    """
    channel_id = 202305180002
    name = 'East'
    position = 11
    
    widget_channel = GuildWidgetChannel(
        channel_id = channel_id,
        name = name,
        position = position,
    )
    
    expected_output = {
        'id': str(channel_id),
        'name': name,
        'position': position,
    }
    
    vampytest.assert_eq(
        widget_channel.to_data(defaults = True),
        expected_output,
    )

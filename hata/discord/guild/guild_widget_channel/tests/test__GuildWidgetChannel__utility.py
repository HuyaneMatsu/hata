import vampytest

from ..guild_widget_channel import GuildWidgetChannel

from .test__GuildWidgetChannel__constructor import _assert_fields_set


def test__GuildWidgetChannel__copy():
    """
    Tests whether ``GuildWidgetChannel.copy`` works as intended.
    """
    channel_id = 202305180010
    name = 'East'
    position = 11
    
    widget_channel = GuildWidgetChannel(
        channel_id = channel_id,
        name = name,
        position = position,
    )
    
    copy = widget_channel.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(widget_channel, copy)

    vampytest.assert_eq(widget_channel, copy)


def test__GuildWidgetChannel__copy_with__0():
    """
    Tests whether ``GuildWidgetChannel.copy_with`` works as intended.
    
    Case: no fields given.
    """
    channel_id = 202305180011
    name = 'East'
    position = 11
    
    widget_channel = GuildWidgetChannel(
        channel_id = channel_id,
        name = name,
        position = position,
    )
    
    copy = widget_channel.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(widget_channel, copy)

    vampytest.assert_eq(widget_channel, copy)


def test__GuildWidgetChannel__copy_with__1():
    """
    Tests whether ``GuildWidgetChannel.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_channel_id = 202305180012
    old_name = 'East'
    old_position = 11
    
    new_channel_id = 202305180013
    new_name = 'Far'
    new_position = 42
    
    widget_channel = GuildWidgetChannel(
        channel_id = old_channel_id,
        name = old_name,
        position = old_position,
    )
    
    copy = widget_channel.copy_with(
        channel_id = new_channel_id,
        name = new_name,
        position = new_position,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(widget_channel, copy)

    vampytest.assert_ne(widget_channel, copy)

    vampytest.assert_eq(copy.id, new_channel_id)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.position, new_position)

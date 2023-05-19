import vampytest

from ..guild_widget_channel import GuildWidgetChannel


def _assert_fields_set(widget_channel):
    """
    Checks whether every attribute is set of the given guild widget channel.
    
    Parameters
    ----------
    widget_channel : ``GuildWidgetChannel``
        The field to check.
    """
    vampytest.assert_instance(widget_channel, GuildWidgetChannel)
    vampytest.assert_instance(widget_channel.id, int)
    vampytest.assert_instance(widget_channel.name, str)
    vampytest.assert_instance(widget_channel.position, int)


def test__GuildWidgetChannel__new__0():
    """
    Tests whether ``GuildWidgetChannel.__new__`` works as intended.
    
    Case: No fields given.
    """
    widget_channel = GuildWidgetChannel()
    _assert_fields_set(widget_channel)


def test__GuildWidgetChannel__new__1():
    """
    Tests whether ``GuildWidgetChannel.__new__`` works as intended.
    
    Case: All fields given.
    """
    channel_id = 202305180000
    name = 'East'
    position = 11
    
    widget_channel = GuildWidgetChannel(
        channel_id = channel_id,
        name = name,
        position = position,
    )
    _assert_fields_set(widget_channel)
    
    vampytest.assert_eq(widget_channel.id, channel_id)
    vampytest.assert_eq(widget_channel.name, name)
    vampytest.assert_eq(widget_channel.position, position)
